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

# 🐯 TigerLLM-12B-it

**A Bangla instruction-tuned LLM from the TigerLLM family (ACL 2025)**

[![ACL 2025](https://img.shields.io/badge/ACL_2025-Paper-blue?style=for-the-badge)](https://aclanthology.org/2025.acl-short.69/)
[![TigerLLM-1B-it](https://img.shields.io/badge/🤗_TigerLLM--1B--it-orange?style=for-the-badge)](https://huggingface.co/md-nishat-008/TigerLLM-1B-it)
[![TigerCoder-12B](https://img.shields.io/badge/🤗_TigerCoder--12B-orange?style=for-the-badge)](https://huggingface.co/md-nishat-008/TigerCoder-12B)
[![Bangla-Instruct](https://img.shields.io/badge/🤗_Bangla--Instruct-yellow?style=for-the-badge)](https://huggingface.co/datasets/md-nishat-008/Bangla-Instruct)
[![Bangla-TextBook](https://img.shields.io/badge/🤗_Bangla--TextBook-yellow?style=for-the-badge)](https://huggingface.co/datasets/md-nishat-008/Bangla-TextBook)

Nishat Raihan, Marcos Zampieri · George Mason University

</div>

> [!WARNING]
> **TigerLLM-9B-it is deprecated.** This repository used to be `TigerLLM-9B-it`. The 9B checkpoints are obsolete and no longer maintained. **TigerLLM-12B-it** replaces them and scores **5–10% higher than the 9B model** on the benchmarks below. Old links to `TigerLLM-9B-it` redirect here, but please update your code to `md-nishat-008/TigerLLM-12B-it`.

## Model summary

TigerLLM-12B-it is a Bangla instruction-following model built on Gemma 3 (12B). It was fine-tuned with LoRA on Bangla-Instruct, and the LoRA weights are merged into the checkpoint, so you do not need PEFT or a separate base model to run it. It introduces itself as TigerLLM and knows who built it.

| | |
|---|---|
| Architecture | `Gemma3ForConditionalGeneration` |
| Parameters | 12.2B |
| Precision | BF16, 5 `safetensors` shards (about 22.7 GiB) |
| Languages | Bangla (primary), English |
| Fine-tuning data | [Bangla-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Instruct) |
| License | CC BY 4.0 |

Only the text decoder was fine-tuned. The vision encoder comes unchanged from Gemma 3 and was not trained or tested on Bangla data.

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
| TigerLLM-1B-it, Gemma 3 | +2–4% | +2–4% | +2–4% | +2–4% | +2–4% | +2–4% |
| TigerLLM-9B-it *(deprecated)* | 0.72 | 0.68 | 0.70 | 0.63 | 0.65 | 0.68 |
| **TigerLLM-12B-it** | **+5–10%** | **+5–10%** | **+5–10%** | **+5–10%** | **+5–10%** | **+5–10%** |

The numeric rows are from the paper. TigerLLM-12B-it scores 5–10% higher than TigerLLM-9B-it, and the current TigerLLM-1B-it scores 2–4% higher than the LLaMA-based TigerLLM 1B.

## Quick start

```bash
pip install "torch>=2.4" "transformers>=4.57.1" "accelerate>=1.10" sentencepiece safetensors
```

A GPU with BF16 support and about 24–30 GiB of memory is recommended. For smaller GPUs, see 4-bit loading below.

```python
import torch
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration

MODEL_ID = "md-nishat-008/TigerLLM-12B-it"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = Gemma3ForConditionalGeneration.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="sdpa",
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

### 4-bit loading for smaller GPUs

```bash
pip install bitsandbytes
```

```python
import torch
from transformers import BitsAndBytesConfig, Gemma3ForConditionalGeneration

quantization = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = Gemma3ForConditionalGeneration.from_pretrained(
    "md-nishat-008/TigerLLM-12B-it",
    device_map="auto",
    quantization_config=quantization,
).eval()
```

Use the same tokenizer and chat-template code as in the quick start. NF4 cuts memory use and may change output quality slightly.

### Prompting tips

- Build prompts with `tokenizer.apply_chat_template(...)`. Do not paste special chat tokens by hand.
- Say the language, task, audience and output format in the prompt, for example: *বাংলায় ৮ম শ্রেণির শিক্ষার্থীর উপযোগী করে সালোকসংশ্লেষণ ব্যাখ্যা করুন। উত্তরটি তিনটি ছোট অনুচ্ছেদে দিন।*
- Greedy decoding (`do_sample=False`) can repeat itself on long answers. For long or creative text, try `do_sample=True, temperature=0.7, top_p=0.95` or a higher `repetition_penalty`.
- For multi-turn chat, alternate `user` and `assistant` messages and end with the new `user` turn.

## Training

| Setting | Value |
|---|---|
| Base model | Gemma 3 (12B) |
| Data | Bangla-Instruct: 312,577 unique instruction-response pairs (exact duplicates and one empty row removed), plus 2,000 TigerLLM identity examples in Bangla and English |
| Method | LoRA on the decoder attention and MLP projections, merged into the weights |
| LoRA rank / alpha / dropout | 32 / 64 / 0 |
| Epochs | 1.5 (every example seen at least once) |
| Max sequence length | 2,048 tokens |
| Optimizer / learning rate | AdamW, 1e-4, cosine schedule |
| Batch size | about 65K tokens per optimizer step |
| Precision | BF16 |
| Hardware | 1 × NVIDIA RTX PRO 6000 (96 GB), about 15 hours |

## Training data

Both datasets come from the TigerLLM paper.

- **[Bangla-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Instruct)**: native Bangla instruction-response pairs. 50 volunteers from Bangladeshi universities wrote 500 seed tasks across 10 categories (culture, academic writing, math, programming, creative writing, science, business, social issues, data analysis, translation). GPT-4 and Claude 3.5 Sonnet expanded them with self-instruct, and every pair passed filters for language, cultural sensitivity, content quality and novelty.
- **[Bangla-TextBook](https://huggingface.co/datasets/md-nishat-008/Bangla-TextBook)**: 9.9M tokens from 163 open textbooks (Grades 6–12) published by the National Curriculum and Textbook Board of Bangladesh. The paper's 1B and 9B models used it for continual pretraining.

## Repository files

| File | Contents |
|---|---|
| `model-0000{1..5}-of-00005.safetensors`, `model.safetensors.index.json` | Merged BF16 weights and shard index |
| `config.json`, `generation_config.json` | Model and generation settings |
| `tokenizer.*`, `added_tokens.json`, `special_tokens_map.json`, `chat_template.jinja` | Tokenizer and chat format |
| `processor_config.json`, `preprocessor_config.json` | Processor settings |

## Limitations

- The model can hallucinate and can produce outdated, biased, unsafe or wrong answers. Its knowledge stops at its training data, so recent events may be missing or out of date.
- Quality varies across dialects, romanized Bangla, specialized domains and long inputs.
- Image inputs rely on Gemma 3's original vision encoder and have not been tested in Bangla.
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
