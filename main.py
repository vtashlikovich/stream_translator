import openai
import os
from dotenv import load_dotenv
import assemblyai as aai
import deepl
from pydub import AudioSegment
from pydub.playback import play
import time

load_dotenv()

READ_TRANSLATION = True

translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
aai.settings.api_key = os.environ["ASSEMBLY_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

client = None
if READ_TRANSLATION:
    client = openai.OpenAI()

def on_open(session_opened: aai.RealtimeSessionOpened):
    "This function is called when the connection has been established."
    print("Session ID:", session_opened.session_id)

def gen_speech_file(speech_file_path, text):
    st = time.time()
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(speech_file_path)
    print('to speech for:', (time.time() - st), 'sec')
    return speech_file_path


def play_audio(speech_file_path):
    audio_clip = AudioSegment.from_mp3(speech_file_path)
    play(audio_clip)


def on_data(transcript: aai.RealtimeTranscript):
    "This function is called when a new transcript has been received."

    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        result = translator.translate_text(transcript.text, target_lang="PL")
        print(transcript.text, end="\r\n")
        print("PL: " + result.text)

        if READ_TRANSLATION:
            speech_file_path = "speech.mp3"
            gen_speech_file(speech_file_path, result.text)
            play_audio(speech_file_path)
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    "This function is called when the connection has been closed."

    print("An error occured:", error)

def on_close():
    "This function is called when the connection has been closed."

    print("Closing Session")


transcriber = aai.RealtimeTranscriber(
    on_data=on_data,
    on_error=on_error,
    sample_rate=44_100,
    on_open=on_open, # optional
    on_close=on_close, # optional
    )

# Start the connection
transcriber.connect()

# Open a microphone stream
microphone_stream = aai.extras.MicrophoneStream()

# Press CTRL+C to abort
transcriber.stream(microphone_stream)

transcriber.close()

