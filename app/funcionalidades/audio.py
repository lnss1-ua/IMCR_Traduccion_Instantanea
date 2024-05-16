# audio.py
from gtts import gTTS  # Google Text-to-Speech
import base64
from io import BytesIO
import tempfile

def text_to_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        temp_filename = fp.name
    tts.save(temp_filename)
    audio_obj = BytesIO()
    with open(temp_filename, 'rb') as fp:
       audio_obj.write(fp.read())
    audio_obj.seek(0)
    audio_base64 = base64.b64encode(audio_obj.read())
    # Asegúrate de que la cadena base64 comienza con 'data:audio/mpeg;base64,'
    return 'data:audio/mpeg;base64,' + audio_base64.decode('utf-8')