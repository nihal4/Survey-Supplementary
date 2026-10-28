---
license: mit
library_name: transformers
pipeline_tag: text-generation
language:
  - bn
  - en
tags:
  - bengali
  - bangla
  - bilingual
  - llama
  - slm
  - base-model
  - mit-0
datasets:
  - wikimedia/wikipedia
  - ai4bharat/IndicCorpV2
  - HuggingFaceFW/fineweb-edu
---

# Kotha-S1 (~100M Base Model)

**Md. Wahid · Kotha Lab**

Kotha-S1 is a 99.9M parameter bilingual (Bengali and English) base language model trained from scratch on a custom LLaMA-style architecture. It serves as the foundation for [logicwahid/Kotha-S1-Instruct](https://huggingface.co/logicwahid/Kotha-S1-Instruct) and is designed for research, custom fine-tuning, and deployment on edge devices or standard CPUs.

## Model Specifications
- **Architecture:** LLaMA (RMSNorm, RoPE, SwiGLU)
- **Parameters:** 99,943,040 (~100M)
- **Tokenizer:** Custom bilingual tokenizer (32,000 vocab)
- **Languages:** Bengali (বাংলা) & English
- **License:** MIT-0 (No Attribution)

## Usage (Text Completion)

As a pretrained base model, Kotha-S1 completes text continuations rather than following chat instructions directly. For chat or question-answering, use [Kotha-S1-Instruct](https://huggingface.co/logicwahid/Kotha-S1-Instruct).

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

repo_id = "logicwahid/Kotha-S1"
tok = AutoTokenizer.from_pretrained(repo_id)
model = AutoModelForCausalLM.from_pretrained(repo_id, torch_dtype=dtype).to(device)

prompt = "বাংলাদেশের রাজধানী ঢাকা একটি "
inputs = tok(prompt, return_tensors="pt").to(device)

out = model.generate(
    **inputs,
    max_new_tokens=60,
    do_sample=True,
    top_p=0.85,
    temperature=0.4,
    repetition_penalty=1.15
)
print(tok.decode(out[0], skip_special_tokens=True))