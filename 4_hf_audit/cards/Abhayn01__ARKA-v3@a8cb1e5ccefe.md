---
license: apache-2.0
language:
- en
- hi
- bn
library_name: transformers
pipeline_tag: text-generation
tags:
- arka
- causal-lm
- grouped-query-attention
- custom-code
---

# ⚡ ARKA-v3

## A Custom 505M-Parameter Language Model

**Created and developed by Abhay Kumar Rudrapaul**

ARKA-v3 is a decoder-only Transformer language-model architecture using
Grouped-Query Attention (GQA), RoPE, RMSNorm, SwiGLU and tied token/output
embeddings. This recreated package contains fresh randomly initialized weights;
it must be pretrained before meaningful text generation.

## Architecture

| Specification | Value |
|---|---:|
| Parameters | 505,661,184 |
| Vocabulary | 151,665 |
| Hidden size | 1,152 |
| Layers | 22 |
| Attention heads | 18 |
| KV heads | 6 |
| Head dimension | 64 |
| FFN dimension | 3,328 |
| Maximum context | 4,096 |
| Weight tying | Yes |
| Attention | Grouped-Query Attention |
| Position encoding | RoPE |
| Activation | SwiGLU |
| Normalization | RMSNorm |

The maintained Qwen2 implementation primitives in Hugging Face Transformers are
used as the execution backend because their tensor layout matches this
architecture. ARKA-v3 has its own model type, configuration and AutoModel
registration.

## Installation

```bash
pip install -U "torch>=2.4" "transformers>=4.53" \
  "huggingface_hub>=0.27" "safetensors>=0.4.5" "accelerate>=1.2"
```

## Load

Review the repository's custom Python files before enabling remote code. For
reproducible use, pin `revision` to a trusted commit hash.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

repo_id = "Abhayn01/ARKA-v3"
revision = "PASTE_TRUSTED_COMMIT_HASH"

tokenizer = AutoTokenizer.from_pretrained(
    repo_id, revision=revision, trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
    repo_id,
    revision=revision,
    trust_remote_code=True,
    dtype=torch.float16,
)
```

## Important status

The recreated checkpoint is randomly initialized. It preserves the exact
architecture and parameter count, but it does not reconstruct previously
deleted learned weights or knowledge. Pretraining is required.

## Creator

ARKA is an independent language-model development project created and developed
by **Abhay Kumar Rudrapaul**.

