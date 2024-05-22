# translation.py
from deep_translator import GoogleTranslator
from flask import request, jsonify
from .audio import text_to_audio

def translate_text(text, src_lang, target_lang):
    try:
        translation = GoogleTranslator(source=src_lang, target=target_lang).translate(text)
        return translation
    except Exception as e:
        print(e)
        print("Failed to translate text. The text was: ", text)
        return text

def translate_request():
    # Assuming that the text, output format, and output language are sent in the request
    text = request.form['text']
    output_format = request.form['output_format']
    output_lang = request.form['output_lang']

    
    # Translate the text to the selected output language
    text = translate_text(text, 'auto', output_lang)
    
    # If the selected output format is audio, convert the transcription to audio
    # and return it
    if output_format == 'audio':
        audio_output = text_to_audio(text, output_lang)
        return jsonify({'transcription': audio_output, 'language': output_lang})
    # If the selected output format is text, return the transcription as is
    else:
        return jsonify({'transcription': text, 'language': output_lang})