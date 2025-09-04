# visual-qa-tem
Automated pipeline for constructing visual question-answering datasets from microscopy literature to enable LLM interpretation of scientific images.

## Install

1.Clone this repository and navigate to main folder
```bash
git clone https://github.com/SmartLab-Roy/visual-qa-tem.git
cd visual-qa-tem
```
2. install Package
```bash
conda create -n  vqa-tem python=3.10 -y
conda activate vqa-tem

pip install --upgrade pip
pip install requirements.txt
```

## Documentation
Follow these steps sequentially for complete pipeline implementation:

| Step | document | explanation |
|------| -------- | -------- |
| 1 | [🕷️Web Crawling](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/docs/Web%20Crawling.md)    | Collect scientific papers from online sources     |
| 2 | [📄Data Extraction](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/docs/Data%20Extraction.md)    | Extract figures and captions from PDF documents     |
| 3 | [🔄Data Preprocessing](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/docs/Data%20Preprocessing.md)    | Process and classify TEM images & Caption Reconstruction Using OCR|
| 4 |[📋Data distillation](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/docs/Data%20distillation.md)|Generate high-quality QA pairs using GPT      |
| 5 | **Model Training** | Follow [LLaVA LoRA Training Scripts](https://github.com/haotian-liu/LLaVA/blob/main/scripts/v1_5/finetune_task_lora.sh) |
| 6 | **Model Inference** | Follow [LLaVA Inference Scripts](https://github.com/haotian-liu/LLaVA/blob/main/llava/serve/cli.py) |
| 7 | [📊Model Evaluation](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/docs/Model%20Evaluation.md)   | Assess model performance with comprehensive metrics     |

⚠️ **important**: This project requires LLaVA model integration. Please complete LLaVA installation before proceeding with steps 5-6. See [LLaVA Installation Guide](https://github.com/haotian-liu/LLaVA.git)

## Hugging Face

Our fine-tuned LLaVA model for TEM image analysis is available on Hugging Face:

🤗 **Model**: [LabSmart/visual-qa-tem](https://huggingface.co/LabSmart/visual-qa-tem)

### Download Model
```python
from huggingface_hub import snapshot_download
import os

# Download the model to local directory
model_path = snapshot_download(
    repo_id="LabSmart/visual-qa-tem",
    cache_dir="./models",  # Local cache directory
    resume_download=True
)

print(f"Model downloaded to: {model_path}")
```
### Quick Start

Reference [LLaVA](https://github.com/haotian-liu/LLaVA.git) for environment setup and CLI inference:

```
python -m llava.serve.cli \
    --model-path "model_path from the download output"\
    --image-file "path/to/your/tem_image.jpg" \
    --load-4bit
```
