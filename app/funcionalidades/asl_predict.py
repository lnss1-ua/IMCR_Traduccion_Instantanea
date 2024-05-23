import numpy as np
import tensorflow as tf
from PIL import Image
import argparse

def load_and_preprocess_image(image_path, target_height, target_width, target_channels):
    # Load the image using PIL
    img = Image.open(image_path).convert('RGB')

    # Resize the image to the target height while maintaining aspect ratio
    aspect_ratio = img.width / img.height
    new_width = int(target_height * aspect_ratio)
    img = img.resize((new_width, target_height))

    # Convert the image to a numpy array
    img_array = np.array(img)

    # If the width is not equal to the target width, crop or pad the image to make it equal
    if img_array.shape[1] != target_width:
        if img_array.shape[1] > target_width:
            # Crop the width
            img_array = img_array[:, :target_width, :]
        else:
            # Pad the width
            padding = target_width - img_array.shape[1]
            img_array = np.pad(img_array, ((0, 0), (0, padding), (0, 0)), mode='constant', constant_values=0)

    # Normalize the image to [0, 1]
    img_array = img_array / 255.0
    img_array = img_array.astype(np.float32)

    # Add batch dimension
    # img_array = np.expand_dims(img_array, axis=0)

    return img_array

def main(image_path):
    # Load the TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Get the expected input shape
    input_shape = input_details[0]['shape']
    print("Expected input shape:", input_shape)

    # Assuming the input shape is [None, 543, 3]
    if len(input_shape) == 4:
        batch_size, height, width, channels = input_shape
    elif len(input_shape) == 3:
        height, width, channels = input_shape
    else:
        raise ValueError("Unexpected input shape: {}".format(input_shape))

    # Preprocess the image
    input_data = load_and_preprocess_image(image_path, target_height=height, target_width=width, target_channels=channels)

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Get list of classes
    label_index = read_dict(f"{CFG.data_path}sign_to_prediction_index_map.json")
    index_label = dict([(label_index[key], key) for key in label_index])

    # Postprocess the output (map to class labels)
    # print("Output prediction:", output_data)
    sign = np.argmax(output_data)
    print(f"Predicted label: {index_label[sign]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify an image using a TFLite model.")
    parser.add_argument("image_path", type=str, help="Path to the image to be classified.")
    args = parser.parse_args()
    main(args.image_path)

