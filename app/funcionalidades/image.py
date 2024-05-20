from flask import request, jsonify
import easyocr
import os
from .translation import translate_text
from .audio import text_to_audio


class DetectFromImage:
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['en', 'es'], gpu=False)

    def detect_text(self):
        # Assuming that the audio file, output format, and output language are sent in the request
        image_file = request.files['image']
        output_format = request.form['output_format']
        output_lang = request.form['output_lang']

        # Store File
        image_file.seek(0)
        temp_path = f"./{image_file.filename}"
        image_file.save(temp_path)
        
        # Detect text from image
        result = self.reader.readtext(temp_path, detail=0)
        os.remove(temp_path)

        # Process the detected text from the result
        detected_text = ' | '.join(result)

        # Translate the transcription to the selected output language
        detected_text = translate_text(detected_text, 'auto', output_lang)

        # If the selected output format is audio, convert the transcription to audio
        # and return it
        if output_format == 'audio':
            audio_output = text_to_audio(detected_text, output_lang)
            return jsonify({'transcription': audio_output, 'language': output_lang})
        # If the selected output format is text, return the transcription as is
        else:
            return jsonify({'transcription': detected_text, 'language': output_lang})