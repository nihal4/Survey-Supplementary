---
language:
- bn
- en
library_name: transformers
tags:
- rag
- bengali
- customer-support
---

# SPEAKLAR-RAG-1.7B

This is a standalone full checkpoint for retrieval-augmented customer-support responses.

It is intended for retrieval-augmented customer-support responses. Supply concise, relevant retrieved evidence rather than a full policy document. The model was tested with Bengali evidence and produces Bengali answers.

## Load

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "munzurul/SPEAKLAR-RAG-1.7B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
```

## Important

This model should not be used as the source of truth for changing business facts. Retrieve relevant knowledge first, then use the retrieved evidence as model context. Validate prices, calculations, and policy-critical responses in application code.
