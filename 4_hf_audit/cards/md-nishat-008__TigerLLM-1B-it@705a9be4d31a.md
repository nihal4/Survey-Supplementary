---
language:
- bn
- en
license: cc-by-4.0
library_name: transformers
pipeline_tag: text-generation
tags:
- bengali
- bangla
- gemma3
- instruction-tuned
- tigerllm
datasets:
- md-nishat-008/Bangla-Instruct
---

<div align="center">

# 🐯 TigerLLM-1B-it

**A compact Bangla instruction-tuned LLM from the TigerLLM family (ACL 2025)**

[![ACL 2025](https://img.shields.io/badge/ACL_2025-Paper-blue?style=for-the-badge)](https://aclanthology.org/2025.acl-short.69/)
[![TigerLLM-12B-it](https://img.shields.io/badge/🤗_TigerLLM--12B--it-orange?style=for-the-badge)](https://huggingface.co/md-nishat-008/TigerLLM-12B-it)
[![TigerCoder-1B](https://img.shields.io/badge/🤗_TigerCoder--1B-orange?style=for-the-badge)](https://huggingface.co/md-nishat-008/TigerCoder-1B)
[![Bangla-Instruct](https://img.shields.io/badge/🤗_Bangla--Instruct-yellow?style=for-the-badge)](https://huggingface.co/datasets/md-nishat-008/Bangla-Instruct)
[![Bangla-TextBook](https://img.shields.io/badge/🤗_Bangla--TextBook-yellow?style=for-the-badge)](https://huggingface.co/datasets/md-nishat-008/Bangla-TextBook)

Nishat Raihan, Marcos Zampieri · George Mason University

</div>

> [!WARNING]
> **The LLaMA-based TigerLLM 1B is deprecated.** The 1B model in the ACL 2025 paper was built on LLaMA 3.2. Those checkpoints are obsolete and no longer maintained. This repository hosts the Gemma 3 version of TigerLLM-1B-it, which scores **2–4% higher than the LLaMA-based 1B** on the benchmarks below.
>
> **TigerLLM-9B-it is deprecated too.** For the larger model, use [TigerLLM-12B-it](https://huggingface.co/md-nishat-008/TigerLLM-12B-it), which scores 5–10% higher than the 9B model.

## Model summary

TigerLLM-1B-it is a small Bangla instruction-following model. It answers questions, explains, rewrites, summarizes and translates in Bangla, and it is light enough for a laptop GPU or a CPU. It introduces itself as TigerLLM and knows who built it.

| | |
|---|---|
| Architecture | `Gemma3ForCausalLM` (Gemma 3, 1B) |
| Parameters | 1.0B |
| Precision | BF16, one `model.safetensors` file (about 1.9 GiB) |
| Context length | 32,768 tokens (from `config.json`) |
| Languages | Bangla (primary), English |
| Fine-tuning data | [Bangla-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Instruct) |
| License | CC BY 4.0 |

## Benchmarks

Scores on six Bangla benchmarks, from Table 2 of the [TigerLLM paper (ACL 2025)](https://aclanthology.org/2025.acl-short.69/).

| Model | MMLU-bn | PangBench-bn | BanglaQuaD | mHumanEval-bn | BEnQA | BanglaRQA |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-3.5 | 0.55 | 0.55 | 0.50 | 0.56 | 0.50 | 0.49 |
| Gemini 1.5 Flash | 0.66 | 0.57 | 0.62 | 0.58 | 0.56 | 0.61 |
| GPT-4o-mini | 0.67 | 0.62 | 0.65 | 0.56 | 0.60 | 0.60 |
| LLaMA 3.2 (11B) | 0.22 | 0.19 | 0.21 | 0.15 | 0.18 | 0.20 |
| Gemma 2 (27B) | 0.35 | 0.51 | 0.43 | 0.64 | 0.50 | 0.56 |
| Pangea (7B) | 0.18 | 0.15 | 0.17 | 0.10 | 0.14 | 0.16 |
| Titu-LLM | 0.06 | 0.19 | 0.08 | 0.02 | 0.17 | 0.21 |
| Bong-LLaMA | 0.05 | 0.12 | 0.08 | 0.02 | 0.15 | 0.13 |
| Bangla-LLaMA | 0.02 | 0.08 | 0.05 | 0.10 | 0.11 | 0.09 |
| Bangla-Gemma | 0.18 | 0.15 | 0.12 | 0.10 | 0.22 | 0.19 |
| TigerLLM 1B, LLaMA 3.2 *(deprecated)* | 0.61 | 0.55 | 0.68 | 0.61 | 0.59 | 0.62 |
| **TigerLLM-1B-it, Gemma 3 (this model)** | **+2–4%** | **+2–4%** | **+2–4%** | **+2–4%** | **+2–4%** | **+2–4%** |
| TigerLLM-9B-it *(deprecated)* | 0.72 | 0.68 | 0.70 | 0.63 | 0.65 | 0.68 |
| TigerLLM-12B-it | +5–10% | +5–10% | +5–10% | +5–10% | +5–10% | +5–10% |

The numeric rows are from the paper. This model scores 2–4% higher than the LLaMA-based TigerLLM 1B, and TigerLLM-12B-it scores 5–10% higher than TigerLLM-9B-it.

## Quick start

```bash
pip install "torch>=2.4" "transformers>=4.56" accelerate sentencepiece
```

The model needs about 2 GB of GPU memory in BF16, and it also runs on CPU or Apple Silicon (`device_map="mps"`).

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "md-nishat-008/TigerLLM-1B-it"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
    device_map="auto",
).eval()

messages = [{"role": "user", "content": "বাংলায় সহজ ভাষায় ব্যাখ্যা করুন: মেশিন লার্নিং কী এবং এটি কোথায় ব্যবহৃত হয়?"}]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

with torch.inference_mode():
    output_ids = model.generate(**inputs, max_new_tokens=256, do_sample=False, repetition_penalty=1.05)

print(tokenizer.decode(output_ids[0, inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
```

Or with a pipeline:

```python
from transformers import pipeline

chat = pipeline("text-generation", model="md-nishat-008/TigerLLM-1B-it", dtype="bfloat16")
print(chat([{"role": "user", "content": "তোমার নাম কী?"}], max_new_tokens=128)[0]["generated_text"][-1]["content"])
```

### Prompting tips

- Build prompts with `tokenizer.apply_chat_template(...)`. Do not paste special chat tokens by hand.
- Say the language, task, audience and output format in the prompt, for example: *বাংলায় ৮ম শ্রেণির শিক্ষার্থীর উপযোগী করে সালোকসংশ্লেষণ ব্যাখ্যা করুন। উত্তরটি তিনটি ছোট অনুচ্ছেদে দিন।*
- Use `do_sample=False` for reproducible output. The default generation config samples with `top_k=64` and `top_p=0.95`.
- For multi-turn chat, alternate `user` and `assistant` messages and end with the new `user` turn.

## Training

The current checkpoint was trained in two stages on top of Gemma 3 (1B): instruction tuning on Bangla-Instruct, then a short identity fine-tune.

| Identity fine-tune | Value |
|---|---|
| Data | 2,000 TigerLLM identity examples (Bangla and English) mixed with 6,000 Bangla-Instruct examples, so earlier skills are kept |
| Method | LoRA (rank 16, alpha 32) on all attention and MLP projections, merged into the weights |
| Epochs / learning rate | 2 / 1e-4, cosine schedule |
| Check | loss on 500 held-out Bangla-Instruct examples went from 1.383 to 1.356 |

<details>
<summary>Fine-tuning setup the paper reports for the LLaMA-based 1B model</summary>

| Parameter | Value |
|---|---|
| Max sequence length | 2048 |
| Batch size (train / eval) | 16 |
| Gradient accumulation steps | 4 |
| Epochs | 3 |
| Learning rate | 1e-5 |
| Weight decay | 0.02 |
| Warm-up | 10% of steps |
| Optimizer | AdamW (8-bit) |
| LR scheduler | Cosine |
| Precision | BF16 |
| Seed | 42 |

</details>

## Training data

Both datasets come from the TigerLLM paper.

- **[Bangla-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Instruct)**: native Bangla instruction-response pairs. 50 volunteers from Bangladeshi universities wrote 500 seed tasks across 10 categories (culture, academic writing, math, programming, creative writing, science, business, social issues, data analysis, translation). GPT-4 and Claude 3.5 Sonnet expanded them with self-instruct, and every pair passed filters for language, cultural sensitivity, content quality and novelty.
- **[Bangla-TextBook](https://huggingface.co/datasets/md-nishat-008/Bangla-TextBook)**: 9.9M tokens from 163 open textbooks (Grades 6–12) published by the National Curriculum and Textbook Board of Bangladesh. The paper's models used it for continual pretraining.

## Repository files

| File | Contents |
|---|---|
| `model.safetensors` | Full BF16 model weights |
| `config.json`, `generation_config.json` | Model and generation settings |
| `tokenizer.json`, `tokenizer.model`, `tokenizer_config.json`, `added_tokens.json`, `special_tokens_map.json`, `chat_template.jinja` | Tokenizer and chat format |

## Limitations

- The model can hallucinate and can produce outdated, biased, unsafe or wrong answers. A 1B model makes more of these mistakes than TigerLLM-12B-it, especially on arithmetic and multi-step reasoning.
- Quality varies across dialects, romanized Bangla, specialized domains and long inputs.
- Do not use it as the only source for medical, legal, financial or other high-stakes decisions. Keep a human in the loop.

## License

CC BY 4.0. Check the Gemma 3 terms of use and the dataset licenses before redistribution or commercial use.

## Citation

```bibtex
@inproceedings{raihan-zampieri-2025-tigerllm,
    title = "{T}iger{LLM} - A Family of {B}angla Large Language Models",
    author = "Raihan, Nishat  and
      Zampieri, Marcos",
    editor = "Che, Wanxiang  and
      Nabende, Joyce  and
      Shutova, Ekaterina  and
      Pilehvar, Mohammad Taher",
    booktitle = "Proceedings of the 63rd Annual Meeting of the {A}ssociation for {C}omputational {L}inguistics (Volume 2: Short Papers)",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.acl-short.69/",
    doi = "10.18653/v1/2025.acl-short.69",
    pages = "887--896",
    ISBN = "979-8-89176-252-7"
}
```

Questions: [md.nishat.008@gmail.com](mailto:md.nishat.008@gmail.com)
