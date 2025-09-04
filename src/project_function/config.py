import os

# === Get absolute path to current config file directory ===
current_dir = os.path.dirname(os.path.abspath(__file__))

# === Dataset Path Settings ===
# All paths are relative to this config file location
PDF_PATH = os.path.join(current_dir, "../../TEM_DATAS/TEM_pdfs")  # Raw input PDFs
PDF_IMAGE_PATH = os.path.join(current_dir, "../../TEM_DATAS/LLaVA Dataset/PDF_images")  # Converted PDF page images
TEM_IMAGE_PATH = os.path.join(current_dir, "../../TEM_DATAS/LLaVA Dataset/TEM_images")  # Cropped TEM sub-images
DESCRIPTION_PATH = os.path.join(current_dir, "../../TEM_DATAS/LLaVA Dataset/TEM_descriptions")  # Cropped captions

# === YOLO Model Weights ===
CROP_IMAGES = os.path.join(current_dir, "vision_model", "crop_images.pt")             # For detecting main panels
IMAGE_DESCRIPTION = os.path.join(current_dir, "vision_model", "image_description.pt") # For splitting TEM vs caption
TEM_IMAGE_CROP = os.path.join(current_dir, "vision_model", "TEM_image_crop.pt")       # For cropping sub-TEM structures

# === Classification Models (ResNet-based) ===
BINARY_CLASSIFIER = os.path.join(current_dir, "vision_model", "binary_classifier.pth")    # None vs NotNone classifier
FIVE_CLASS_CLASSIFIER = os.path.join(current_dir, "vision_model", "five_class_classifier.pth")  # 5-way TEM classifier


# === CSV Output Path ===
CSV_PATH = os.path.join(current_dir, "../tem_images_description.csv")  # Metadata logging

if __name__ == '__main__':
    print(current_dir)