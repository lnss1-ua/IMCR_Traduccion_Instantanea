from flask import Flask, request, render_template
import os, signal
from funcionalidades.transcription import transcribe_audio

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    return transcribe_audio()


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
    app.run(debug=True, threaded=True)