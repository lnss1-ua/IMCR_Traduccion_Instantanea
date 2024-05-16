# translation.py
from googletrans import Translator

def translate_text(text, target_lang):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except TypeError:
        print("Failed to translate text. The text was: ", text)
        return text
    except AttributeError:
        print("Failed to translate text. The text was: ", text)
        return text