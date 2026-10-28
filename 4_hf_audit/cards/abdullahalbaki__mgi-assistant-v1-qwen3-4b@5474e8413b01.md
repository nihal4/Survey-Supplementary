---
license: apache-2.0
base_model: unsloth/Qwen3-4B-Instruct-2507
language:
- en
- bn
pipeline_tag: text-generation
library_name: transformers
tags:
- unsloth
- qwen3
- lora
- sft
- rag
- bangla
- banglish
- customer-assistant
---

# MGI Assistant v1 (Qwen3-4B)

**MGI Assistant** is a bilingual (English, Bangla and Banglish) assistant for questions about **Meghna Group of Industries (MGI)** and **Meghna Aviation**: brands, products and SKUs, business verticals, economic zones, CSR, careers and contact points. It was developed by **MD Abdullah Al Baki**.

## What it does

- Answers in the user's language: English, Bangla (বাংলা) or Banglish
- Introduces itself as MGI Assistant, built by MGI AI Labs
- In RAG mode, answers only from the supplied context and ends with the source link
- Says it couldn't find the answer, and points to the right MGI contact, when the context doesn't contain it
- Does not invent prices, stock, specifications or contact details
- Politely declines questions unrelated to MGI

<p align="left">
  <img src="https://huggingface.co/abdullahalbaki/mgi-assistant-v1-qwen3-4b/resolve/main/sample.png" alt="MGI Assistant answering questions in English, Bangla and Banglish" width="700">
</p>


## Quick start

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

repo = "abdullahalbaki/mgi-assistant-v1-qwen3-4b"
tokenizer = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo, torch_dtype="auto", device_map="auto")

SYSTEM_CHAT = (
    "You are MGI Assistant, an AI assistant developed by MD Abdullah Al Baki. "
    "You help people with information about Meghna Group of Industries (MGI) — its brands, products and SKUs, "
    "business verticals, economic zones, CSR, careers — and Meghna Aviation. Be warm, professional and concise, "
    "and answer the question first. Reply in the user's language: English, Bangla, or Banglish (Bangla in Roman "
    "letters). Never invent prices, stock, specifications or contact details; if you are not sure, say so and "
    "share the right MGI contact."
)

messages = [
    {"role": "system", "content": SYSTEM_CHAT},
    {"role": "user", "content": "soyabean tel er ki ki size ase?"},
]
inputs = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
).to(model.device)
output = model.generate(**inputs, max_new_tokens=400, temperature=0.7, top_p=0.8, top_k=20, do_sample=True)
print(tokenizer.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

### Recommended: RAG mode

For factual questions, retrieve relevant chunks and use the RAG system prompt. The user turn must follow the same layout the model was trained on:

```python
SYSTEM_RAG = SYSTEM_CHAT + (
    " Use only the information in the provided context to answer. If the context does not contain the answer, "
    "say you couldn't find it and share the right contact. When you use the context, end with the source link."
)

user_turn = (
    "Context:\n"
    "[1] <retrieved chunk>\n\n"
    "[2] <retrieved chunk>\n\n"
    "Question: Meghna Aviation er koyta helicopter ase?"
)
messages = [{"role": "system", "content": SYSTEM_RAG}, {"role": "user", "content": user_turn}]
```

Use the system prompts exactly as written above. The model was trained with them, and other wording weakens its identity and grounding behaviour.

**Generation settings:** `temperature=0.7, top_p=0.8, top_k=20` (the Qwen3-Instruct defaults) for chat. Use greedy decoding (`do_sample=False`) when answers must be reproducible.

## Training

| | |
|---|---|
| Base model | `unsloth/Qwen3-4B-Instruct-2507` (trained on its 4-bit version, merged into 16-bit weights) |
| Method | QLoRA supervised fine-tuning, loss on assistant replies only (`train_on_responses_only`) |
| LoRA | r = 32, alpha = 32, dropout 0, on `q, k, v, o, gate, up, down` projections (66 M trainable parameters, 1.6%) |
| Epochs / steps | 2 epochs, 414 steps |
| Batch | 1 per device × 16 gradient accumulation = 16 |
| Optimizer | AdamW 8-bit, learning rate 2e-4, cosine schedule, 5% warmup, weight decay 0.01 |
| Max sequence length | 4096 (longest example 2,721 tokens) |
| Final loss | train 0.63, validation 1.077 (epoch 1: 1.078) |

Validation loss barely changed between epochs 1 and 2 while training loss kept falling. More epochs are unlikely to help.

### Data

3,300 training, 160 validation and 166 test conversations, built from 1,843 question-answer items taken from public content on mgi.org and meghnaaviation.com (crawled 26–27 September 2026). The splits are made by source page, so test facts never appear in training.

| Type | Train | Purpose |
|---|---|---|
| `chat` | 1,696 | Question → answer, no context |
| `rag` | 1,117 | Retrieved context (correct chunk + 1–2 distractors) → grounded answer + source link |
| `rag_none` | 142 | Context without the answer → "couldn't find it" + the right contact |
| `multiturn` | 283 | Two related questions in one conversation |
| `persona_*` | 62 | Identity, greetings, off-topic questions, prices and stock → polite redirect |

Languages: English 51%, Banglish 32%, Bangla 17%.

Quality checks on the data:
- Every number in a written answer had to appear in its source text; 20 answers failed and were dropped.
- Product, SKU, fleet and contact answers were generated directly from the parsed website data.
- Newsletter content covers business news only, with no employee personal data.

## Intended use

Customer-facing and internal information assistant for MGI and Meghna Aviation, deployed with a retrieval index over MGI's published content. Not intended for general-purpose chat, or for legal, medical or financial advice.

## License

The model weights are released under Apache 2.0, the license of the Qwen3-4B-Instruct-2507 base model. The training content was taken from MGI's public websites; confirm with MGI before redistributing the model or its outputs publicly.

## Credits

Developed by **MD Abdullah Al Baki**. Built on [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) by the Qwen team and fine-tuned with [Unsloth](https://github.com/unslothai/unsloth).
