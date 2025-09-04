# Model Evaluation

We calculate evaluation scores by comparing predictions from our fine-tuned model with ground truth annotations using established metrics.

## Lexical-based Metrics

### BLEU Score
We compute BLEU scores for n-grams 1 through 4 and combine them using weighted averaging:

> $$BLEU_{combined} = 0.4 \times BLEU_1 + 0.3 \times BLEU_2 + 0.2 \times BLEU_3 + 0.1 \times BLEU_4$$

### ROUGE Score
We compute ROUGE scores for ROUGE-1, ROUGE-2, ROUGE-L, and ROUGE-Lsum, then combine them using weighted averaging:

> $$ROUGE_{combined} = \frac{ROUGE_1 + ROUGE_2 + \frac{ROUGE_L + ROUGE_{Lsum}}{2}}{3}$$

### METEOR Score
Standard METEOR evaluation for semantic similarity.

### Lexical Score
> $$S_{lexical} = 0.3 \times ROUGE_{combined} + 0.2 \times BLEU_{combined} + 0.5 \times METEOR$$

## Semantic-based Metrics

### BERT Score

```python
evaluate.load("bertscore")
model_type="microsoft/deberta-xlarge-mnli"
```

### SentenceBERT

```python
SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
```

### Semantic Score
Uses BERTScore and SentenceBERT for semantic similarity:
> $$S_{semantic} = 0.5 \times BERTScore + 0.5 \times SBERT$$

## Final Evaluation Score

**Combined Score**: We average lexical and semantic scores for comprehensive evaluation:

> $$Final\_Score = 0.5 \times S_{lexical} + 0.5 \times S_{semantic}$$

This evaluation framework provides both surface-level text similarity (lexical) and deeper meaning comparison (semantic) to assess model performance comprehensively.

## GPT 
GPT-4o was used to approximate expert evaluation along three dimensions:
1. **Terminology accuracy** (correct use of scientific terms),
2. **Reasoning logic** (validity and internal consistency),
3. **Expression quality** (fluency, completeness, professionalism).
This complemented automated metrics by capturing human-like assessment of semantic and logical quality

For Model Evaluation, refer to our implementation in [scripts/evaluation.ipynb](https://github.com/SmartLab-Roy/visual-qa-tem/blob/main/scripts/evaluation.ipynb)
