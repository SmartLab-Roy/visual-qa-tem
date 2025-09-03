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
pip install requirements
```

## Document
| document | explanation |
| -------- | -------- |
|[📋 Guide](https://github.com/SmartLab-Roy/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Guide.md)|Detailed instructions        |
| [🕷️Web Crawling](https://github.com/SmartLab-Roy/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Web%20Crawling.md)    | Data collection functionality     |
| [📄PDF Processing](https://github.com/SmartLab-Roy/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/PDF%20Processing.md)    | Image & captions extraction from PDFs     |
| [🔄Data Preprocess](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/docs/Data%20Preprocessing.md)    | Preprocessing|
| [📊Model Evaluation](https://github.com/SmartLab-Roy/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Model%20Evaluation.md)    | Evaluation metrics and analysis     |

⚠️ **important**: This project requires LLaVA model integration. Please complete LLaVA installation before proceeding.

Please see on https://github.com/haotian-liu/LLaVA.git

## Hugging Face

Our fine-tuned LLaVA model for TEM image analysis is available on Hugging Face:

🤗 **Model**: [LabSmart/visual-qa-tem](https://huggingface.co/LabSmart/visual-qa-tem)

### Quick Start

```python
import torch
from PIL import Image
from transformers import LlavaForConditionalGeneration, AutoProcessor

# Load model and processor
model_id = "LabSmart/visual-qa-tem"
subfolder = "llava-7b-curriculum-final"

model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    subfolder=subfolder,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)
processor = AutoProcessor.from_pretrained(model_id)

# Load your TEM image
image = Image.open("path/to/your/tem_image.jpg")

# Prepare input
prompt = "USER: <image>\nDescribe this image.\nASSISTANT:"
inputs = processor(prompt, image, return_tensors='pt')

# Generate response
with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=512)
response = processor.decode(output[0], skip_special_tokens=True)
print(response)
```
