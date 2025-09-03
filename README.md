# visual-qa-tem
Automated pipeline for constructing visual question-answering datasets from microscopy literature to enable LLM interpretation of scientific images.

## Install

1.Clone this repository and navigate to main folder
```bash
git clone https://github.com/ChongRenTu/visual-qa-tem.git
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
|[📋 Guide](https://github.com/ChongRenTu/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Guide.md)|Detailed instructions        |
| [🕷️Web Crawling](https://github.com/ChongRenTu/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Web%20Crawling.md)    | Data collection functionality     |
| [📄PDF Processing](https://github.com/ChongRenTu/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/PDF%20Processing.md)    | PDF extraction and preprocessing     |
| [🔄Data Transformation](https://github.com/ChongRenTu/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Data%20Transformation.md)    | Training format conversion     |
| [📊Model Evaluation](https://github.com/ChongRenTu/visual-qa-tem/blob/7e270f0901d44a7d68925c9c831b04addeaa5e07/docs/Model%20Evaluation.md)    | Evaluation metrics and analysis     |

⚠️ **important**: This project requires LLaVA model integration. Please complete LLaVA installation before proceeding.

Please see on https://github.com/haotian-liu/LLaVA.git

