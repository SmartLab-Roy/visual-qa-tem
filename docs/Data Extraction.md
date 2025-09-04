# Data Extraction
<img width="3654" height="2547" alt="5-copy2" src="https://github.com/user-attachments/assets/7e45c56d-bcbb-4ff2-831b-1dd85bf7a62b" />

## PDF Processing Pipeline for Figure-Caption Extraction
Our pipeline processes scientific PDF documents to extract figure-caption pairs for dataset creation:

### Phase 1: Figure-Caption Detection
Automatically detect and locate figure-caption sections within PDF documents

Process:

- PDF Input: Scientific papers containing figures and captions
- YOLO Detection: Identify figure-caption regions in PDF pages
- Segmentation: Extract individual figure-caption sections from detected areas

### Phase 2: Figure and Caption Segmentation
Separate figures from their corresponding captions and classify content

Process:

- Detection: Use YOLO to identify individual figures and caption text within each section
- Segmentation & Classification:

  - Extract individual figure images
  - Extract corresponding caption text
  - Establish figure-caption correspondence

#### Output:

- Figure Dataset: Individual TEM images extracted from publications
- Caption Dataset: Corresponding descriptive text for each figure
- CSV Correspondence: Structured data linking figures to their captions

This pipeline enables the creation of comprehensive TEM image datasets with rich textual descriptions from scientific literature.

**Implementation Details:**
- Complete pipeline available at [src/TEM_project/main.ipynb](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/src/TEM_project/main.ipynb)
- 2YOLO model preprocessing implementation can be found in [src/TEM_project/TEM_project_function/vision_crop.py](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/src/TEM_project/TEM_project_function/vision_crop.py)
  
⚠️ **Important**:
- We trained custom YOLO models specifically for these tasks (training data not provided due to copyright considerations).
- You must provide your own trained YOLO files (.pt format)
- Models are TEM-specific - retrain on your own dataset for other domains
