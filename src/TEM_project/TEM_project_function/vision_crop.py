# === YOLO object detection ===
from ultralytics import YOLO

# === Image classification ===
import torch
from torchvision import models, transforms

# === Image I/O and processing ===
import numpy as np
from PIL import Image
import cv2

# === Project configuration (custom paths, weights, settings) ===
from TEM_project_function import config

# vision_crop.py (module-level cache)
_yolo_crop_model = YOLO(config.CROP_IMAGES) # Load YOLO model for figure-region detection (path is defined in config.CROP_IMAGES)
_yolo_desc_model = YOLO(config.IMAGE_DESCRIPTION) # Load YOLO model for classifying figure components (e.g., TEM image vs. caption)
_yolo_tem_model = YOLO(config.TEM_IMAGE_CROP) # Load YOLO model trained specifically for extracting TEM sub-regions

# === Crop target regions from an image using YOLO (e.g., figure panel detector) ===
def crop_images(image):
    """
    Detect and crop high-confidence regions (class 0) from the input image using a YOLO model.

    Args:
        image (np.ndarray): Input image (expected RGB, will be converted to BGR internally for YOLO)

    Returns:
        List[np.ndarray]: List of cropped image regions corresponding to valid detections
    """
    return_images = []

    
    model = _yolo_crop_model

    # Convert image from RGB to BGR format if necessary (YOLO expects BGR format for OpenCV input)
    if image.ndim == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Perform object detection (disable verbose output)
    results = model(image, verbose=False)

    # Extract detection results
    boxes = results[0].boxes.xyxy.tolist()  # Bounding boxes (x1, y1, x2, y2)
    scores = results[0].boxes.conf.tolist() # Confidence scores
    classes = results[0].boxes.cls.tolist() # Detected class indices

    # Loop through each detection
    for box, score, cls in zip(boxes, scores, classes):
        # Only keep detections of class 0 with high confidence ( > 0.9 )
        if cls == 0 and score > 0.9:
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Crop the detected region from the image
            crop_object = image[y1:y2, x1:x2]
            return_images.append(crop_object)

    return return_images

# === Extract the main TEM region and its corresponding description from a cropped image ===
def image_description(crop_image):
    """
    Use YOLO to identify and extract:
    1. The largest detected TEM region (class 0)
    2. The largest detected description region (class 1)

    Args:
        crop_image (np.ndarray): Input cropped image (usually from figure layout)

    Returns:
        best_TEM_image (np.ndarray or None): Largest detected TEM sub-image
        best_description_image (np.ndarray or None): Largest detected caption/description sub-image
    """
    best_TEM_image = None
    best_description_image = None

    largest_area_TEM = 0           # Tracks the largest TEM region area
    largest_area_description = 0   # Tracks the largest description region area

    
    model = _yolo_desc_model

    # Convert to BGR if in RGB format (YOLO requires BGR when using OpenCV)
    if crop_image.ndim == 3 and crop_image.shape[2] == 3:
        crop_image = cv2.cvtColor(crop_image, cv2.COLOR_RGB2BGR)

    # Run YOLO inference (suppress terminal output)
    results = model(crop_image, verbose=False)
    boxes = results[0].boxes.xyxy.tolist()  # Bounding boxes
    scores = results[0].boxes.conf.tolist() # Confidence scores
    classes = results[0].boxes.cls.tolist() # Class indices (0 = TEM, 1 = caption)

    # Iterate over all detected boxes
    for box, score, cls in zip(boxes, scores, classes):
        x1, y1, x2, y2 = box

        # Clip coordinates to image boundaries
        x1 = max(0, int(x1))
        y1 = max(0, int(y1))
        x2 = min(crop_image.shape[1], int(x2))
        y2 = min(crop_image.shape[0], int(y2))

        # Compute area of the detection
        area = (x2 - x1) * (y2 - y1)

        # If it's a TEM region and largest seen so far → update
        if cls == 0 and area > largest_area_TEM:
            largest_area_TEM = area
            best_TEM_image = crop_image[y1:y2, x1:x2]

        # If it's a caption/description and largest seen so far → update
        elif cls == 1 and area > largest_area_description:
            largest_area_description = area
            best_description_image = crop_image[y1:y2, x1:x2]

    return best_TEM_image, best_description_image


# === Crop all valid sub-TEM images from a larger TEM image using YOLO ===
def tem_images_crop(image):
    """
    Detect and extract multiple high-confidence TEM sub-regions from a larger TEM image.

    Args:
        image (np.ndarray): Input image (usually a full TEM region)

    Returns:
        List[np.ndarray]: List of cropped sub-TEM images
    """
    return_images = []

    model = _yolo_tem_model

    # Convert image from RGB to BGR if needed (YOLO via OpenCV expects BGR)
    if image.ndim == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Run object detection (suppress verbose output)
    results = model(image, verbose=False)
    boxes = results[0].boxes.xyxy.tolist()
    scores = results[0].boxes.conf.tolist()
    classes = results[0].boxes.cls.tolist()

    # Iterate through each detected object
    for box, score, cls in zip(boxes, scores, classes):
        # Only consider class 0 (TEM sub-image) with high confidence
        if cls == 0 and score > 0.7:
            x1, y1, x2, y2 = map(int, box)
            crop_object = image[y1:y2, x1:x2]
            return_images.append(crop_object)

    return return_images


# === Unified classifier for TEM sub-images ===
def TEM_classifier(image: np.ndarray) -> str:
    """
    Performs two-stage classification for a given TEM sub-image:
    1. Binary classification: 'None' vs 'NotNone'
    2. If classified as 'NotNone', further classify into 5 categories:
       ['CTEM', 'Diffraction', 'HR-TEM', 'SEM', 'STEM']

    Args:
        image (np.ndarray): Input image in RGB or BGR format.

    Returns:
        str: One of the labels: 'None', 'CTEM', 'Diffraction', 'HR-TEM', 'SEM', 'STEM'
    """
    binary_classifier = config.BINARY_CLASSIFIER
    five_class_classifier = config.FIVE_CLASS_CLASSIFIER

    # === Static model cache to avoid reloading ===
    if not hasattr(TEM_classifier, "device"):
        TEM_classifier.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Define preprocessing pipeline (Resize → ToTensor → Normalize)
        TEM_classifier.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.5]*3, [0.5]*3)
        ])

        # === Load Binary Classifier: None vs NotNone ===
        binary_model = models.resnet18(pretrained=False)
        binary_model.fc = torch.nn.Linear(binary_model.fc.in_features, 2)
        binary_model.load_state_dict(torch.load(binary_classifier, map_location=TEM_classifier.device))
        TEM_classifier.binary_model = binary_model.to(TEM_classifier.device).eval()

        # === Load 5-Class Classifier: CTEM, Diffraction, etc. ===
        five_model = models.resnet18(pretrained=False)
        five_model.fc = torch.nn.Linear(five_model.fc.in_features, 5)
        five_model.load_state_dict(torch.load(five_class_classifier, map_location=TEM_classifier.device))
        TEM_classifier.five_model = five_model.to(TEM_classifier.device).eval()

        TEM_classifier.binary_labels = ['None', 'NotNone']
        TEM_classifier.five_labels = ['CTEM', 'Diffraction', 'HR-TEM', 'SEM', 'STEM']

    # === Preprocess input image ===
    if image.ndim == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(image)
    input_tensor = TEM_classifier.transform(pil_img).unsqueeze(0).to(TEM_classifier.device)

    # === Stage 1: Binary Classification ===
    with torch.no_grad():
        out_bin = TEM_classifier.binary_model(input_tensor)
        pred_bin = torch.argmax(out_bin, dim=1).item()
        if TEM_classifier.binary_labels[pred_bin] == 'None':
            return 'None'

    # === Stage 2: 5-Class Classification (only if NotNone) ===
    with torch.no_grad():
        out_five = TEM_classifier.five_model(input_tensor)
        pred_five = torch.argmax(out_five, dim=1).item()
        return TEM_classifier.five_labels[pred_five]

        