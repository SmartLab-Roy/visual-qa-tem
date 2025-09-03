
import sys
import os
import glob
dataset_path = "tem_crop_dataset/dataset/dataset"
annotated_file_list = []
i = 0
with open(dataset_path + "/train.txt") as fh:
    for line in fh:
        i += 1
        file_path = line.strip()
        annotated_file_list.append(file_path.rsplit("/", 1)[1][:-4])
print(f"Finish reading through the file list. Totally {i} files.")

def remove_unannotated_image(image_path, annotated_file_list):
    
    kept = 0
    delete = 0
    if not os.path.exists(image_path):
        print("image_path does not exist.")
        return 
    else:
        dir = os.listdir(image_path)
        for file in dir:  
            print(file[:-4])
            if file[:-4] not in annotated_file_list:
                print("remove: ", image_path + "/" + file)
                delete += 1
                os.remove(image_path + "/" + file)
            else:
                kept += 1
    print(f"Finish removing unannotated images. Totally {kept} files are kept, and {delete} files are unannotated and deleted.")

remove_unannotated_image("tem_crop_dataset\\unlabel_images_copy", annotated_file_list)