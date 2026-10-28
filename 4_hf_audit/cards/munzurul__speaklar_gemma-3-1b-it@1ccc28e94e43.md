---
language:
- bn
- en
library_name: transformers
pipeline_tag: text-generation
tags:
- bengali
- voicebot
- grounded-generation
- customer-support
---

# Speaklar Gemma 3 1B IT

A Gemma 3 1B instruction model fine-tuned for grounded Bengali voice-bot conversations.

## Intended use

Provide the relevant knowledge-base context with each request. The model is trained to answer from supplied evidence, state when information is unavailable, follow Bengali voice-agent style constraints, gather essential details for orders and appointments, and safely hand off sensitive or unsupported requests.

Grounding is a product-level responsibility: retrieve the correct context, enforce output checks for important workflows, and evaluate on your real traffic before production deployment.

## Inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "munzurul/speaklar_gemma-3-1b-it"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")
messages = [{"role": "user", "content": "প্রশ্ন: আপনার সেবা কী?\n\nপ্রসঙ্গ: ..."}]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True,
                                       return_tensors="pt", return_dict=True).to(model.device)
answer_ids = model.generate(**inputs, max_new_tokens=160, do_sample=False)
print(tokenizer.decode(answer_ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True))
```

## Training data

Fine-tuned with QLoRA on a 15,000-example Bengali voice-bot behavior dataset. The set includes Bengali, English, and Banglish inputs/context; assistant outputs are Bengali-only. It covers evidence-grounded answers, abstention, calculations, order/appointment intake, payment safety, complaint intake, and human handoff.
