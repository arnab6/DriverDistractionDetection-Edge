# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
from random import random
import sys
import signal
import threading
import time
from azure.iot.device import IoTHubModuleClient, Message
import os
import io 
import json
from datetime import datetime
import random

Config_file_path = "/app/project-10/SimulatorConfig.json"
SimulatorConfig = None 
sensorList = ["StearingRotationFrequecySensor", "AccelatorPressureSensor"]

module_client = IoTHubModuleClient.create_from_edge_environment()
print ("Azure IoT Client Created...")
module_client.connect()
print ("Azure IoT Client Conected...")


def readconfig():
    
    
    """
    This method , reads and validate config file, in case the file is corrupt of missing, it will create an file automatically 
    with default settings 

    """
    
    global SimulatorConfig
   
    try:

        with open(Config_file_path,'r',encoding='utf-8') as r:
     
                SimulatorConfig = json.load(r)
                if type (SimulatorConfig["SetSimulatorAlertStatus"] ) == bool and type (SimulatorConfig["SimulateInterval"] ) == int :

                    print("validated simulator configfile sucessfully")

                else: 
                    raise Exception("The validation of simulator configfile is failed ")
            
    except Exception as e:
        
        print("The class lable json file failed with Exception : {}".format(e) )
        print ("Either file is missing or is not readable or format is wrong, creating file...")
        
        json_string = { "SetSimulatorAlertStatus" : False , "SimulateInterval" : 5 }
        with open(Config_file_path, 'w') as outfile:
            json.dump(json_string, outfile)
        
        print ("Sucessfully createdfile now trying to read again.. ")
        readconfig()


def create_alert_iot_message(SensorType,Alert):
    
    """
    Create IoT alert json payload, based on the sensor data received. 
    
    """
    
    if Alert :
        
        return {
            "alertType": True , 
            "SensorType": SensorType,
            "timeStamp" : str(datetime.now())
            }
    else :
        
        return {
                "alertType": False , 
                "Sensortype":"None" , 
                "timeStamp" : str(datetime.now())
                }

def create_telemetry_iot_message(message):

    """
    Creates the IoT telemetry message 
    """
    
    message["timestamp"] = str(datetime.now())
    return message


def create_simulated_message(GenerateAlertState):

    """
    This method is the sensor simulator method, based on desired simulator , it will create an simulate values 
    in similar range.

    """
    if GenerateAlertState : 
       
       return  {sensorList[0] : 0 , sensorList[1] : random.randint(0,15) }

    else:

        return  {sensorList[0] : random.randint(5,8) , sensorList[1] : random.randint(200,980) }


def check_alert(message):

    """
    This method is the alert checker, checks the threshold and validates 

    """
    
    if message ["StearingRotationFrequecySensor"] >= 5 and message ["AccelatorPressureSensor"] > 100 :

        return False
    else :

        return True

def send_message(message_json,output):
     
    """
    This method creates the azure iot message payload and sends to the Module output 

    """ 
    formatted_iot_message = Message(json.dumps(message_json))
    module_client.send_message_to_output(formatted_iot_message, output )
    print("Message Sent to {} , the message is {} ".format(output,formatted_iot_message))


def simulate ():

    """
    This is an infinite loop that runs always reads the config to check the latest desired status, 
    finally creates a simulated sensor values, creates alert  & telemetry payload & send that to alert module 
    
    """

    while True:

        readconfig()
        
        DesriredAlertState = SimulatorConfig["SetSimulatorAlertStatus"] 
        DesriredDataInterval = SimulatorConfig["SimulateInterval"]

        SimulatedData = create_simulated_message(DesriredAlertState)
        AlertStatus = check_alert(SimulatedData)
        
        AlertIoTMessage = create_alert_iot_message( Alert= AlertStatus, SensorType= sensorList)
        TelemetryIoTMessage = create_telemetry_iot_message(SimulatedData)

        send_message(AlertIoTMessage,"output1")
        send_message(TelemetryIoTMessage,"output2")

        time.sleep(DesriredDataInterval)

        print("\n") 


def main():
    simulate()
        

if __name__ == "__main__":
    
    main()
