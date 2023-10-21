import os
from PIL import Image

def count_files(folder_path):
    no_of_files  = 0
    dict_file_name = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path,file_name)
        if os.path.isfile(file_path):
            no_of_files += 1
            dict_file_name[file_name] = file_path
            # ls_file_name.append(file_name)
    return no_of_files, dict_file_name
    
def check_folder(resized_folder_path : str):
    if not os.path.exists(resized_folder_path):
        # If it doesn't exist, create the "Resized" folder
        os.makedirs(resized_folder_path)
    else:
        # If it exists, delete all files in it
        for filename in os.listdir(resized_folder_path):
            file_path = os.path.join(resized_folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

def resize_image(image_dict : dict, resized_folder_path : str, desired_height : int):
    new_height = desired_height
    for file_name, file_path in image_dict.items():
        output_folder = os.path.join(resized_folder_path,file_name)

        img = Image.open(file_path)

        original_width, original_height = img.size
        new_width = int(new_height * original_width/original_height)

        img = img.resize((new_width,new_height), Image.BICUBIC)

        img.save(output_folder)