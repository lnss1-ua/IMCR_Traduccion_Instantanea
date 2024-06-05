import numpy as np
import tensorflow as tf
from PIL import Image
import argparse
import json

def read_dict(file_path):
    with open(file_path, "r") as f:
        dic = json.load(f)
    return dic

def main(image_path):
    # Load the TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
     # Normalize the image to [0, 1]
    img_array = img_array / 255.0
    img_array = img_array.astype(np.float32)

    prediction_fn = interpreter.get_signature_runner("serving_default")

    # Get the output tensor
    output_data = prediction_fn(inputs=img_array)

    # Define a list of class labels (replace with your actual class labels)
    # Get list of classes
    label_index = read_dict(f"sign_to_prediction_index_map.json")
    index_label = dict([(label_index[key], key) for key in label_index])

    # Postprocess the output (map to class labels)
    # print("Output prediction:", output_data)
    sign = np.argmax(output_data["outputs"])
    # print("Index:", sign)
    # print(f"Predicted label: {index_label[sign]}")
    return jsonify('predicted_label': {index_label[sign]})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify an image using a TFLite model.")
    parser.add_argument("image_path", type=str, help="Path to the image to be classified.")
    args = parser.parse_args()
    main(args.image_path)
