
# Stream translator

This app reads stream from system microphone, converts speech to text using Assembly, translates text to any language you prefer using DeepL and plays Speech of the translation audio done by OpenAI text-to-speech model.


## Installation

Install dependencies:

```bash
  python -m venv env
  source env/bin/activate
  pip install -r requirements.txt
```

Create .env file and fill in 3 keys in it, example:

```
DEEPL_API_KEY=111
OPENAI_API_KEY=222
ASSEMBLY_API_KEY=333
```

    
## Usage/Examples

Run the code to start translating:

```bash
 python main.py
```

Ctrl+C to abort the program.

Hint: do not mix mic and phones or use audo-headset for testing.

## Tuning

To output online translation only, without audio, edit the code:

```python
READ_TRANSLATION = False
```

To change target translation language, edit this line:

```python
result = translator.translate_text(transcript.text, target_lang="PL")
```

Change "PL" to any other language supported by DeepL: https://support.deepl.com/hc/en-us/articles/360019925219-Languages-included-in-DeepL-Pro

To change speaking voice, change it here:

```python
voice="nova"
```

Use any model from OpenAI: https://platform.openai.com/docs/guides/text-to-speech