# transcription.py
from flask import request, jsonify
import numpy as np
import librosa
import whisper
from .translation import translate_text
from .audio import text_to_audio

def transcribe_audio():
    # Assuming that the audio file, output format, and output language are sent in the request
    audio_file = request.files['audio']
    output_format = request.form['output_format']
    output_lang = request.form['output_lang']
    # Read the audio file into a NumPy array
    audio_np, sr = librosa.load(audio_file, sr=None)
    # Load the Whisper model
    model = whisper.load_model("base") #large
    # Transcribe the audio
    result = model.transcribe(audio_np)
    # Extract the transcribed text from the result
    transcribed_text = result['text']
    if result['language'] != output_lang:
        # Translate the transcription to the selected output language
        transcribed_text = translate_text(transcribed_text, output_lang)
    # If the selected output format is audio, convert the transcription to audio
    # and return it
    if output_format == 'audio':
        audio_output = text_to_audio(transcribed_text, output_lang)
        return jsonify({'transcription': audio_output, 'language': output_lang})
    # If the selected output format is text, return the transcription as is
    else:
        return jsonify({'transcription': transcribed_text, 'language': output_lang})