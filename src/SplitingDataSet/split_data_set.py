#spliting the the data into train and test & validation
import splitfolders
import os


#input dataset path 
input_dataset_folder = ""

#splitted dataset path 
processed_destination_folder= ""


def get_recursive_file_count(path):
    
    """
    This method counts the number of file recursively on given path

    """

    noOfFiles = 0
    noOfDir = 0
    
    try :
        for base, dirs, files in os.walk(path):
            print('Looking in : ',base)
            for directories in dirs:
                noOfDir += 1
            for Files in files:
                noOfFiles += 1
        
        return noOfFiles
   
    except Exception as err :
        print("Exception caught in get_recursive_file_count , the exception is {} ".format(err))

def validate_spliting():    

    """
    This method validate the spliting done by the lib 'splitfolders' 

    """
    number_of_image_per_class = {}
    image_distributuion_class = {}


    number_of_image_per_class ["train"] = get_recursive_file_count(os.path.join(processed_destination_folder,"train"))
    number_of_image_per_class ["validation"] = get_recursive_file_count(os.path.join(processed_destination_folder,"val"))
    number_of_image_per_class ["test"] = get_recursive_file_count(os.path.join(processed_destination_folder,"test"))

    total_images = number_of_image_per_class ["train"] + number_of_image_per_class ["validation"] + number_of_image_per_class ["test"]

    image_distributuion_class ["train"] = (number_of_image_per_class ["train"]  / total_images) *100
    image_distributuion_class ["validation"] = (number_of_image_per_class ["validation"]  / total_images) *100
    image_distributuion_class ["test"] = (number_of_image_per_class ["test"]  / total_images) *100


    print(number_of_image_per_class)
    print(image_distributuion_class)



splitfolders.ratio(input=input_dataset_folder,output=processed_destination_folder,seed=42,ratio=(0.7,0.15,0.15)) # this method splits the dataset into part 

validate_spliting()