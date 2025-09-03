# Data Preprocessing
<img width="6000" height="3375" alt="6" src="https://github.com/user-attachments/assets/7f3159e8-e3a2-4e49-974b-e8f3e3ddef02" />

### Caption Reconstruction Using OCR
#### Phase 1 caption OCR processing 
We utilize two OCR engines to extract different types of text from caption images:

- Pix2Text: For LaTeX-formatted mathematical expressions and formulas
- EasyOCR: For general descriptive text recognition

For caption image OCR processing, refer to our implementation in [scripts/caption_OCR.ipynb](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/scripts/caption_OCR.ipynb)

#### GPT-Powered Caption Enhancement 
After extracting raw text from caption images, we employ GPT-3.5 Turbo to perform two critical tasks:

- Caption Reconstruction: Transform the extracted OCR text (both LaTeX-formatted and descriptive) into coherent, well-structured captions that maintain scientific accuracy while improving readability.
- Content Classification: Automatically categorize caption content into predefined categories to enable systematic organization.

For implementation details of the GPT processing pipeline, refer to [scripts/data distillation.ipynb](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/scripts/data%20distillation.ipynb)

---
### Images Preprocessing for segmentation & classification 
Our preprocessing pipeline consists of two main components to prepare TEM images for analysis:
#### Phase 1: TEM Image Segmentation with YOLO

Use YOLO (You Only Look Once) object detection model Automatically segment parent TEM images into smaller, focused child images

Process:
- Input: Original TEM parent images
- Detection: Identify regions of interest within the larger image
- Output: Multiple child images containing individual structures or features


#### Phase 2: TEM Image Classification with ResNet-18

Use ResNet-18 convolutional neural network to classify TEM images into distinct microscopy categories

Classification Categories:
- STEM: Scanning Transmission Electron Microscopy
- CTEM: Conventional Transmission Electron Microscopy
- HR-TEM: High-Resolution Transmission Electron Microscopy
- Diffraction: Electron diffraction patterns

Process: Multi-class classification to automatically sort images by microscopy technique

This preprocessing step ensures that our dataset is properly organized and that images are optimally prepared for downstream visual question answering tasks.

**Implementation Details:**
- Complete pipeline available at [src/TEM_project/main.ipynb](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/src/TEM_project/main.ipynb)
- YOLO & ResNet preprocessing implementation can be found in [src/TEM_project/TEM_project_function/vision_crop.py](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/src/TEM_project/TEM_project_function/vision_crop.py)
  
⚠️ **Important**:
- We trained custom YOLO & ResNet models specifically for these tasks (training data not provided due to 
copyright considerations).
- You must provide your own trained YOLO & ResNet model files (.pt format)
- Models are TEM-specific - retrain on your own dataset for other domains
