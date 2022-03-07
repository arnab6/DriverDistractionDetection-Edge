from distutils.command.config import config
from email import message
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image 
import cv2
from PIL import Image
from datetime import datetime
import os 
import time
import uuid
from azure.iot.device import IoTHubModuleClient, Message
import pyfiglet


module_client = IoTHubModuleClient.create_from_edge_environment()
print ("Azure IoT Client Created...")
module_client.connect()
print ("Azure IoT Client Conected...")

config = None
class_lables = None


def read_class_lables(path):

    global class_lables
    
    global class_lables
    with open(path,'r',encoding='utf-8') as r:
        try:
            class_lables = json.load(r)
            class_lables = class_lables["classlables"]
        except Exception as e:
            print("The class lable json file failed with Exception : {}".format(e) )


def init():
   
    global config
    with open("config.json",'r',encoding='utf-8') as r:
        try:
            config = json.load(r)
        except Exception as e:
            print("The Config file load failed with Exception : {}".format(e) )

    read_class_lables(config["classlablepath"])

    predict_from_video(input_video_path  = config["input_video_location"], 
                       output_video_path = config["output_destination"],
                       tfmodel_path = config["tflite_model_path"],
                       target_fps= config["target_video_fps"]
     )


def prepare_image(file):
    img = image.load_img(file,target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded_dims)

def prepare_image_from_video_frame(file):
    cvt_image =  cv2.cvtColor(file, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(cvt_image)
    im_resized = im_pil.resize((224, 224))
    img_array = image.img_to_array(im_resized)
    image_array_expanded = np.expand_dims(img_array, axis = 0)

    return tf.keras.applications.mobilenet_v2.preprocess_input(image_array_expanded)


def create_iot_message(class_index):
    
    if class_index == 0 :
        
        return {
            "alertType": False , 
            "classLable": class_lables[class_index],
            "timeStamp" : str(datetime.now())
            }
    else :
        
        return {
                "alertType": True , 
                "classLable": class_lables[class_index] , 
                "timeStamp" : str(datetime.now())
                }
    

def send_message(index):
     
    message_json  = create_iot_message(index)
    formatted_iot_message = Message(json.dumps(message_json))
    module_client.send_message_to_output(formatted_iot_message, "output")

def predict_from_live_feed():
    print ("This feature is not availbe yet ")


def predict_from_video(input_video_path, 
                      output_video_path, 
                      tfmodel_path, 
                      target_fps 
                      ):


    predicted_image_array = []

    # Load the TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path = tfmodel_path)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    image_writer_config = {
       
        "font"  : cv2.FONT_HERSHEY_SIMPLEX,
        "org"  :(50, 50),
        "fontScale" : 0.6,
        "color" : (255, 0, 0),
        "thickness" : 2

    }

    cap = cv2.VideoCapture(input_video_path)

    #finding number of frames in a video 
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

    video_FPS = cap.get(cv2.CAP_PROP_FPS)

    print ("Total Frames in the video is :- {}".format (video_length))
    print ("FPS in the video is :- {}".format(video_FPS))

    frame_skip_index = int (video_FPS / target_fps)

    
    start_time = datetime.now() 
    print("The Video Processing strated at : {}".format(start_time))

    video_frame_count = 0 
   
    while cap.isOpened():
        
        #print("Processing Frame :- {}".format(i))
        sucess, imgOrignal=cap.read()

        if sucess == False:
            break

        if video_frame_count%frame_skip_index == 0 : 

            frame_input = prepare_image_from_video_frame(imgOrignal)
            #print (imgOrignal.shape)
            
            interpreter.set_tensor(input_details[0]['index'], frame_input)

            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])
            #print(output_data.argmax())

            predicted_level = "The prediction is :- " +  class_lables[output_data.argmax()]
            #print(predicted_level)

            written_image  = cv2.putText(imgOrignal, predicted_level , image_writer_config["org"], 
                                        image_writer_config["font"], 
                                        image_writer_config["fontScale"],
                                        image_writer_config["color"], 
                                        image_writer_config["thickness"], 
                                        cv2.LINE_AA
                                        )
            
            #img_name = str(i)+"-pred_images.jpg"
            #print(written_image.shape)
            #cv2.imwrite(img_name, written_image)
            
            predicted_image_array.append(written_image)
            send_message(output_data.argmax())
        
        video_frame_count = video_frame_count +1
    
    end_time = datetime.now() 
    print("The Video Ended strated at : {}".format(end_time))

    total_time = end_time - start_time  

    print("Total time took for processing : {}".format(total_time.total_seconds()))
    print ("Processed total {} frames ".format(len(predicted_image_array)))
    print("Each frame took : {} sec to process ".format( total_time.total_seconds() / len(predicted_image_array) ))

    
    print("saving the predicted images to a video file at {}  location in the host system".format(output_video_path))
    # save the frames to video
    predicated_image_width = predicted_image_array[0].shape[1] #bigger
    predicated_image_height = predicted_image_array[0].shape[0] #smaller

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path,fourcc, target_fps, (predicated_image_width,predicated_image_height))


    for eachPredictedImages in predicted_image_array:
        out.write(eachPredictedImages)
    
    out.release()
    print("Done Saving.. ")



if __name__ == "__main__":
    
    print (pyfiglet.figlet_format("Welcome To Prediction Module...."))
    init()
    #print (config)
    #print(class_lables)


