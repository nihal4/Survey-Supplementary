---
language:
  - mni
  - en
  - bn
license: apache-2.0
tags:
  - manipuri
  - meitei-mayek
  - meiteilon
  - bengali-script
  - indic
  - low-resource
  - foundation-model
  - smollm
  - causal-lm
pipeline_tag: text-generation
library_name: transformers
base_model: HuggingFaceTB/SmolLM-135M
pretty_name: ManipuriGPT 135M Base v1.0
---

# ManipuriGPT-135M-Base-v1.0

Official immutable open foundation model release for **ManipuriGPT**.

## Model Summary
- **Architecture**: SmolLM-135M Causal LM (135 Million Parameters)
- **Tokenizer**: `ManipuriGPT-Tokenizer-v1.0` (8,000 vocabulary size, 0 `<unk>` emissions)
- **Training Corpus**: `ManipuriGPT-Corpus-v1.0`
- **Training Epochs**: 3.0 (13,596 steps)
- **Final Train Loss**: `3.6246`
- **Final Eval Loss**: `4.2799`
- **Meitei Mayek Perplexity**: `133.14`

## How to Use in Python

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "nanskong/ManipuriGPT-135M-Base-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)

prompt = "ꯑꯩ"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=64, do_sample=True, top_k=50, temperature=0.7)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Model Lineage & Hierarchy
```text
ManipuriGPT-135M-Base-v1.0  (Immutable Pretrained Foundation Model)
        │
        ├── ManipuriGPT-135M-SFT-v1.0   (Instruction Fine-Tuned)
        ├── ManipuriGPT-135M-SFT-v2.0   (Multi-task / Reasoning)
        ├── ManipuriGPT-135M-DPO-v1.0   (Direct Preference Optimization)
        └── ManipuriGPT-135M-Chat-v1.0  (Conversational Assistant)
```

## Immutability Guarantee
This directory is locked as the baseline foundation release. All downstream fine-tuning (SFT, DPO, RLHF) will build upon this model without overwriting base weights.
