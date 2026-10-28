---
base_model: unsloth/qwen2.5-3b-instruct-unsloth-bnb-4bit
tags:
- text-generation
- conversational
- emotional-ai
- mental-health
- multilingual
- bengali
- unsloth
- qwen2
- transformers
language:
- en
- bn
license: apache-2.0
datasets:
- Amod/mental_health_counseling_conversations
- iamshnoo/alpaca-cleaned-bengali
library_name: transformers
pipeline_tag: text-generation
---

# Arete OSS 3B 🧠❤️

An emotionally intelligent AI that actually listens.

Built by **[Iseer & Co.](https://iseer.co)** - Making AI that understands humans, not just language.

## What makes Arete different?

Most AI assistants optimize for being "smart." Arete optimizes for being **empathetic**.

- 🇧🇩 Speaks **English and Bengali** fluently
- 💬 Trained on real emotional support conversations
- 🎯 Recognizes when you're struggling and responds with care
- 🌍 Understands cultural context (especially South Asian family dynamics)

**3 billion parameters. Infinite empathy.**

## Try it

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("inanxr/Arete-OSS-3B")
tokenizer = AutoTokenizer.from_pretrained("inanxr/Arete-OSS-3B")

prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Respond with empathy and understanding to the following message.

### Input:
I'm feeling overwhelmed and don't know what to do.

### Response:
"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))