#spliting the the data into train and test & validation
import splitfolders
import os



input_dataset_folder = r"F:\Study\PGDAIML\Project-10\Latest_data_set\NewDataSet-Cropped-Light"

processed_destination_folder= r"F:\Study\PGDAIML\Project-10\Latest_data_set\Processed_data\Processed_data_from_colorLite_dataset-70-15-15"


def get_recursive_file_count(path):
    noOfFiles = 0
    noOfDir = 0
    
    for base, dirs, files in os.walk(path):
        print('Looking in : ',base)
        for directories in dirs:
            noOfDir += 1
        for Files in files:
            noOfFiles += 1
    
    return noOfFiles

def validate_spliting():    

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



#splitfolders.ratio(input=input_dataset_folder,output=processed_destination_folder,seed=42,ratio=(0.7,0.15,0.15))

validate_spliting()