---
license: mit
language:
- bn
metrics:
- google_bleu
base_model:
- google/mt5-small
pipeline_tag: text2text-generation
library_name: transformers
tags:
- grammatical-error-correction
- indic-nlp
- bangla
- bengali
- gec
---

# mt5-small-indic-gec-bangla

A multilingual Grammatical Error Correction (GEC) model fine-tuned from [mT5-small](https://huggingface.co/google/mt5-small) for **Bangla (Bengali)**. Developed as part of the BHASHA 2025 Shared Task 1: IndicGEC.

- **Developed by:** Manav Dhamecha, Gaurav Damor, Sunil Choudhary, Pruthwik Mishra
- **License:** MIT
- **Base model:** [google/mt5-small](https://huggingface.co/google/mt5-small)
- **Paper:** [Team Horizon at BHASHA Task 1](https://aclanthology.org/2025.bhasha-1.14/)
- **Repository:** [manavdhamecha77/IndicGEC2025](https://github.com/manavdhamecha77/IndicGEC2025)
- **GitHub.io:** [Multilingual IndicGEC](https://manavdhamecha77.github.io/gec/)

---

## What it does

Given a grammatically incorrect Bangla sentence, the model outputs a corrected version. It handles errors across spelling, grammar (tense, person, number, gender, case), punctuation, missing/extra words, and semantic issues.

**GLEU Score on Bangla test set: 82.69**

---

## Quick Start

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "manavdhamecha77/GEC-mT5-Small-Bangla"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

sentences = [
    "আমি স্কুলে যাই",
    "সে বাড়ি গেছিলাম",
]

inputs = ["correct this: " + s for s in sentences]

encoded = tokenizer(
    inputs,
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=128
).to(device)

outputs = model.generate(**encoded, max_length=128, num_beams=4)
corrected = tokenizer.batch_decode(outputs, skip_special_tokens=True)

for orig, corr in zip(sentences, corrected):
    print(f"Input:     {orig}")
    print(f"Corrected: {corr}\n")
```

---

## Training Details

The model was fine-tuned using a sequence-to-sequence objective on parallel noisy–clean sentence pairs. Training data was expanded from ~598 annotated pairs to ~10k pairs using a synthetic error injection pipeline that introduces realistic errors across 10 linguistic categories.

| Parameter | Value |
|---|---|
| Optimizer | AdamW |
| Learning Rate | 5e-5 |
| Batch Size | 16–32 |
| Epochs | 10–15 |
| Max Sequence Length | 128 |
| Early Stopping | Based on GLEU (dev set) |

Input format: `"correct this: <incorrect sentence>"`

---

## Evaluation

| Language | Model | GLEU |
|---|---|---|
| Bangla | mT5-small | **82.69** |

---

## Limitations

- Performance may degrade on heavy code-mixing, informal slang, or dialectal text.
- Trained primarily on formal written Bangla; may not generalize to all domains.
- Evaluation uses automatic metrics (GLEU) only; human evaluation not conducted.

---

## Citation

```bibtex
@inproceedings{dhamecha2025horizon,
  title     = {Team Horizon at {BHASHA} Task 1: Multilingual {IndicGEC} with Transformer-based Grammatical Error Correction Models},
  author    = {Dhamecha, Manav and Damor, Gaurav and Choudhary, Sunil and Mishra, Pruthwik},
  booktitle = {Proceedings of the 1st Workshop on Benchmarks, Harmonization, Annotation, and Standardization for Human-Centric AI in Indian Languages (BHASHA 2025)},
  year      = {2025},
  url       = {https://aclanthology.org/2025.bhasha-1.14/}
}
```
