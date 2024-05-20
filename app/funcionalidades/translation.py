# translation.py
from deep_translator import GoogleTranslator

def translate_text(text, src_lang, target_lang):
    try:
        translation = GoogleTranslator(source=src_lang, target=target_lang).translate(text)
        return translation
    except Exception as e:
        print(e)
        print("Failed to translate text. The text was: ", text)
        return text
