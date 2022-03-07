import datetime

print(str(datetime.datetime.now()))

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os
import cv2


print(str(datetime.datetime.now()))


def prepare_image(file):
    img = image.load_img(file,target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded_dims)


tflite_model_path = "mobileNetv2-model-2-Date-11-02-22_Acc-98-batch-32-dataset-70-15-15-litemodel.tflite"

print(str(datetime.datetime.now()))
# Load the TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path = tflite_model_path)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(str(datetime.datetime.now()))

print(str(datetime.datetime.now()))
image_path_leanback = "1 0040.jpg"
prepimage =  prepare_image(image_path_leanback)

input_shape = input_details[0]['shape']


input_data = prepimage

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)
print(output_data.argmax())
print(str(datetime.datetime.now()))