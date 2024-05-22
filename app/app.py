from flask import Flask, request, render_template, jsonify, redirect, url_for
import os, signal, filetype
from funcionalidades.transcription import transcribe_audio
from funcionalidades.image import DetectFromImage
from funcionalidades.translation import translate_request

# source myenv/bin/activate
# import torch

# Comprueba si hay una GPU disponible y si soporta FP16
# if torch.cuda.is_available():
#     device = torch.device("cuda")
#     if device.capability() >= (7, 0):
#         dtype = torch.float16
#     else:
#         dtype = torch.float32
# else:
#     device = torch.device("cpu")
#     dtype = torch.float32

# # Crea un tensor en la GPU utilizando el tipo de datos correcto
# x = torch.tensor([1.0, 2.0, 3.0], device=device, dtype=dtype)
# hacer cambios para que use fp 16 ???

app = Flask(__name__, template_folder='templates')
image_detector = DetectFromImage()

@app.route('/')
def index():
    return redirect(url_for('text'))

@app.route('/audio')
def audio():
    return render_template('audio.html')

@app.route('/text')
def text():
    return render_template('text.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Store file
    file = request.files['audio']
    file.seek(0)
    temp_path = f"./{file.filename}"
    file.save(temp_path)

    result = jsonify({'transcription': ''})
    
    # Check Type
    try:  
        if filetype.is_audio(temp_path):
            result = transcribe_audio(temp_path)
        else:
            None
            # Show Error Message
    except Exception:
        pass

    # Delete File
    os.remove(temp_path)
    
    return result

@app.route('/translate', methods=['POST'])
def translate():
    return translate_request()

@app.route('/detect', methods=['POST'])
def detect():
    # Store file
    file = request.files['image']
    file.seek(0)
    temp_path = f"./{file.filename}"
    file.save(temp_path)

    result = jsonify({'transcription': ''})
    
    # Check Type
    try:  
        if filetype.is_image(temp_path):
            result = image_detector.detect_text(temp_path)
        else:
            None
            # Show Error Message
    except Exception:
        pass

    # Delete File
    os.remove(temp_path)
    
    return result

def shutdown_server(signum, frame):
    print('Cerrando el servidor...')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('No se puede cerrar el servidor.')
    func()

if __name__ == '__main__':
    # Handle the interrupt signal to shut down the server
    signal.signal(signal.SIGINT, shutdown_server)
    
    print("Starting the server...")
    app.run(debug=True, threaded=True, host='0.0.0.0')
