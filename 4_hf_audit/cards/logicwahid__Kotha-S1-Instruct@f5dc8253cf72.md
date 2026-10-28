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
  - instruct
  - mit-0
datasets:
  - databricks/databricks-dolly-15k
  - wikimedia/wikipedia
---

# Kotha-S1-Instruct (~100M)

**Md. Wahid · Kotha Lab**

Kotha-S1-Instruct is a 99.9M parameter bilingual (Bengali and English) instruction-tuned language model based on [logicwahid/Kotha-S1](https://huggingface.co/logicwahid/Kotha-S1). Built on a LLaMA-style architecture, it is designed to run on standard CPUs, edge devices, and low-resource environments.

## Model Specifications
- **Architecture:** LLaMA (RMSNorm, RoPE, SwiGLU)
- **Parameters:** 99,943,040 (~100M)
- **Tokenizer:** Custom bilingual tokenizer (32k vocab)
- **Languages:** Bengali (বাংলা) & English
- **Prompt Format:** `[INST] prompt [/INST]`
- **License:** MIT-0

## Usage

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

repo_id = "logicwahid/Kotha-S1-Instruct"
tok = AutoTokenizer.from_pretrained(repo_id)
model = AutoModelForCausalLM.from_pretrained(repo_id, torch_dtype=dtype).to(device)

prompt = "[INST] বাংলাদেশের রাজধানী কী? [/INST] "
inputs = tok(prompt, return_tensors="pt").to(device)

out = model.generate(
    **inputs,
    max_new_tokens=80,
    do_sample=True,
    top_p=0.85,
    temperature=0.3,
    repetition_penalty=1.15
)
print(tok.decode(out[0], skip_special_tokens=True))