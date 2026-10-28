---
language: [en, bn]
license: apache-2.0
tags:
  - drishti
  - bangladesh
  - ai
  - drishti-ilm-x1
pipeline_tag: text-generation
---

# drishti-ilm-x1

**DRISHTI** - Bangladesh's Most Advanced AI

## Model Details
- Maintainer: DRISHTI AI Team (red1-for-hek)
- Upload method: shard-by-shard sync from source weights
- Purpose: General AI

## Usage
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("red1-for-hek/drishti-ilm-x1")
tokenizer = AutoTokenizer.from_pretrained("red1-for-hek/drishti-ilm-x1")
```

## License
Apache 2.0
