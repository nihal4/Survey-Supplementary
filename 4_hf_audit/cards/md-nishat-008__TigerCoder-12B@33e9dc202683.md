---
license: cc-by-4.0
language:
- bn
- en
library_name: transformers
pipeline_tag: text-generation
tags:
- code
- bangla
- bengali
- code-generation
- gemma3
- low-resource
- tigercoder
datasets:
- md-nishat-008/Bangla-Code-Instruct
base_model:
- md-nishat-008/TigerLLM-12B-it
---

<div align="center">

# 🐯 TigerCoder-12B

**A Bangla code-generation LLM from the TigerCoder family (LREC 2026)**

[![LREC 2026](https://img.shields.io/badge/LREC_2026-Paper-blue?style=for-the-badge)](https://aclanthology.org/2026.lrec-1.238/)
[![TigerCoder-1B](https://img.shields.io/badge/🤗_TigerCoder--1B-orange?style=for-the-badge)](https://huggingface.co/md-nishat-008/TigerCoder-1B)
[![TigerLLM-12B-it](https://img.shields.io/badge/🤗_TigerLLM--12B--it-orange?style=for-the-badge)](https://huggingface.co/md-nishat-008/TigerLLM-12B-it)
[![Bangla-Code-Instruct](https://img.shields.io/badge/🤗_Bangla--Code--Instruct-yellow?style=for-the-badge)](https://huggingface.co/datasets/md-nishat-008/Bangla-Code-Instruct)
[![MBPP-Bangla](https://img.shields.io/badge/🤗_MBPP--Bangla-yellow?style=for-the-badge)](https://huggingface.co/datasets/md-nishat-008/MBPP-Bangla)

Nishat Raihan, Antonios Anastasopoulos, Marcos Zampieri · George Mason University

</div>

> [!WARNING]
> **TigerCoder-9B is deprecated.** This repository used to be `TigerCoder-9B`. The 9B checkpoints are obsolete and no longer maintained. **TigerCoder-12B** replaces them and scores **5–7% higher than the 9B model** on the benchmarks below. Old links to `TigerCoder-9B` redirect here, but please update your code to `md-nishat-008/TigerCoder-12B`.

## Model summary

TigerCoder is a family of code LLMs for Bangla. TigerCoder-12B is the larger member: you describe a programming task in Bangla and it writes the code. It was fine-tuned from [TigerLLM-12B-it](https://huggingface.co/md-nishat-008/TigerLLM-12B-it) with LoRA on [Bangla-Code-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Code-Instruct), and the LoRA weights are merged into the checkpoint, so you do not need PEFT or a separate base model to run it. It introduces itself as TigerCoder and knows who built it.

| | |
|---|---|
| Architecture | `Gemma3ForConditionalGeneration` (Gemma 3, 12B) |
| Parameters | 12.2B |
| Precision | BF16, 5 `safetensors` shards (about 22.7 GiB) |
| Base model | [TigerLLM-12B-it](https://huggingface.co/md-nishat-008/TigerLLM-12B-it) |
| Task | Code generation from Bangla prompts |
| Programming languages | Python, C++, Java, JavaScript |
| Fine-tuning data | [Bangla-Code-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Code-Instruct), 300K Bangla instruction-code pairs |
| License | CC BY 4.0 |

Only the text decoder was fine-tuned. The vision encoder comes unchanged from Gemma 3 and was not trained or tested on code or Bangla data.

## Benchmarks

Pass@K on Python tasks with Bangla prompts, from the [TigerCoder paper (LREC 2026)](https://aclanthology.org/2026.lrec-1.238/).

| Model | mHumanEval P@1 | mHumanEval P@10 | mHumanEval P@100 | MBPP P@1 | MBPP P@10 | MBPP P@100 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-3.5 | 0.56 | 0.56 | 0.59 | 0.60 | 0.62 | 0.62 |
| Gemini-Flash 2.5 | 0.58 | 0.61 | 0.62 | 0.62 | 0.62 | 0.70 |
| Gemma-3 (27B) | 0.64 | 0.65 | 0.69 | 0.69 | 0.70 | 0.70 |
| TigerLLM (9B) *(deprecated)* | 0.63 | 0.69 | 0.72 | 0.61 | 0.68 | 0.73 |
| TigerCoder-1B, paper checkpoint | 0.69 | 0.73 | 0.77 | 0.74 | 0.74 | 0.81 |
| TigerCoder-1B, current | +2–4% | +2–4% | +2–4% | +2–4% | +2–4% | +2–4% |
| TigerCoder-9B *(deprecated)* | 0.75 | 0.80 | 0.84 | 0.82 | 0.84 | 0.91 |
| **TigerCoder-12B (this model)** | **+5–7%** | **+5–7%** | **+5–7%** | **+5–7%** | **+5–7%** | **+5–7%** |

The numeric rows are from the paper. TigerCoder-12B scores 5–7% higher than TigerCoder-9B, and the current TigerCoder-1B scores 2–4% higher than the paper's TigerCoder-1B.

The paper also tested TigerCoder-9B in other programming languages (Pass@1, Bangla prompts):

| Language | mHumanEval P@1 | MBPP P@1 |
|:---|:---:|:---:|
| Python | 0.75 | 0.82 |
| C++ | 0.67 | 0.72 |
| Java | 0.62 | 0.67 |
| JavaScript | 0.57 | 0.62 |

## Quick start

```bash
pip install "torch>=2.4" "transformers>=4.57.1" "accelerate>=1.10" sentencepiece safetensors
```

A GPU with BF16 support and about 24–30 GiB of memory is recommended. For smaller GPUs, see 4-bit loading below.

```python
import torch
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration

MODEL_ID = "md-nishat-008/TigerCoder-12B"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = Gemma3ForConditionalGeneration.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="sdpa",
).eval()

# "Write a Python function that computes the factorial of a number."
messages = [{"role": "user", "content": "পাইথনে একটি ফাংশন লিখুন যা একটি সংখ্যার ফ্যাক্টরিয়াল গণনা করে।"}]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

with torch.inference_mode():
    output_ids = model.generate(**inputs, max_new_tokens=512, do_sample=False, repetition_penalty=1.05)

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
    "md-nishat-008/TigerCoder-12B",
    device_map="auto",
    quantization_config=quantization,
).eval()
```

Use the same tokenizer and chat-template code as in the quick start. NF4 cuts memory use and may change output quality slightly.

### Prompting tips

- Build prompts with `tokenizer.apply_chat_template(...)`. Do not paste special chat tokens by hand.
- Name the programming language, the function name and signature, and the expected input and output, for example: *পাইথনে একটি ফাংশন `second_largest(nums)` লিখুন যা একটি সংখ্যার তালিকা থেকে দ্বিতীয় বৃহত্তম ভিন্ন সংখ্যাটি ফেরত দেয়।*
- Use `do_sample=False` for Pass@1-style answers. For several candidate solutions (Pass@10, Pass@100), sample with `do_sample=True, temperature=0.7, top_p=0.95`.
- You can also paste code and ask, in Bangla, for an explanation, a bug fix or a translation to another programming language.

## Training

| Setting | Value |
|---|---|
| Base model | [TigerLLM-12B-it](https://huggingface.co/md-nishat-008/TigerLLM-12B-it) |
| Data | Bangla-Code-Instruct: 294,883 unique instruction-code pairs (exact duplicates and one empty row removed), plus 2,000 TigerCoder identity examples in Bangla and English |
| Method | LoRA on the decoder attention and MLP projections, merged into the weights |
| LoRA rank / alpha / dropout | 32 / 64 / 0 |
| Epochs | 1.5 (every example seen at least once), 3,047 optimizer steps |
| Max sequence length | 2,048 tokens |
| Optimizer / learning rate | AdamW, 1e-4, cosine schedule |
| Batch size | about 65K tokens per optimizer step |
| Precision | BF16 |
| Hardware | 1 × NVIDIA RTX PRO 6000 (96 GB), about 15 hours |

<details>
<summary>Training setup the paper reports for TigerCoder-9B</summary>

| Hyperparameter | Value |
|:---|:---|
| Training data | Bangla-Code-Instruct (300K examples) |
| Max sequence length | 2048 |
| Batch size (train / eval) | 32 |
| Gradient accumulation steps | 8 |
| Epochs | 3 |
| Learning rate | 1 × 10⁻⁶ |
| Weight decay | 0.04 |
| Warm-up | 15% of steps |
| Optimizer | AdamW |
| LR scheduler | Cosine |
| Precision | BF16 |
| Hardware | NVIDIA A100 (40 GB) |

</details>

## Training data

[Bangla-Code-Instruct](https://huggingface.co/datasets/md-nishat-008/Bangla-Code-Instruct) has three 100K subsets:

| Subset | Size | How it was built | Prompt origin | Code origin |
|:---|:---:|:---|:---|:---|
| SI (Self-Instruct) | 100K | 5,000 expert seeds expanded with GPT-4o | Semi-natural | Synthetic |
| Syn (Synthetic) | 100K | Generated with GPT-4o and Claude 3.5 Sonnet | Synthetic | Synthetic |
| TE (Translated) | 100K | Evol-Instruct machine-translated with NLLB-200 | Translated | Natural |

All SI and Syn code passed a syntax check (`ast.parse`) and an execution test (Python 3.13.0, 10 s timeout, 16 GB memory).

## Findings from the paper

1. **Bangla prompts hurt code LLMs.** Most models score 20 to 50+ percentage points lower on Bangla coding prompts than on the same prompts in English.
2. **Translating the prompt to English does not fix it.** Machine translation garbles programming terms: "অক্ষর" (character) becomes "letter", "চলক" (variable) becomes "clever", and "স্ট্রিং" (string) becomes "rope".
3. **Targeted data beats scale.** TigerCoder-1B beats models 27 times its size, and TigerCoder-9B led the strongest prior baselines by 11–18%.

## Repository files

| File | Contents |
|---|---|
| `model-0000{1..5}-of-00005.safetensors`, `model.safetensors.index.json` | Merged BF16 weights and shard index |
| `config.json`, `generation_config.json` | Model and generation settings |
| `tokenizer.*`, `added_tokens.json`, `special_tokens_map.json`, `chat_template.jinja` | Tokenizer and chat format |
| `processor_config.json`, `preprocessor_config.json` | Processor settings |

## Limitations

- TigerCoder is trained for Bangla code generation. On general language tasks, use [TigerLLM-12B-it](https://huggingface.co/md-nishat-008/TigerLLM-12B-it).
- The training data is synthetic or machine-translated, and may carry the biases and artifacts of the models that produced it.
- Evaluation covers MBPP-Bangla and mHumanEval-Bangla only. Production-scale coding tasks have not been benchmarked.
- Run and review generated code before you use it.

## License

CC BY 4.0. Check the Gemma 3 terms of use and the dataset licenses before redistribution or commercial use.

## Citation

```bibtex
@inproceedings{raihan-etal-2026-tigercoder,
    title = "{T}iger{C}oder: A Novel Suite of {LLM}s for Code Generation in {B}angla",
    author = "Raihan, Nishat  and
      Anastasopoulos, Antonios  and
      Zampieri, Marcos",
    editor = "Piperidis, Stelios  and
      Bel, N{\'u}ria  and
      van den Heuvel, Henk  and
      Ide, Nancy  and
      Krek, Simon  and
      Toral, Antonio",
    booktitle = "Proceedings of the Fifteenth Language Resources and Evaluation Conference",
    month = may,
    year = "2026",
    address = "Palma de Mallorca, Spain",
    publisher = "ELRA Language Resource Association",
    url = "https://aclanthology.org/2026.lrec-1.238/",
    doi = "10.63317/5nampb63np3m",
    pages = "3044--3054"
}
```

<details>
<summary>Related work</summary>

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

```bibtex
@inproceedings{raihan-etal-2025-mhumaneval,
    title = "m{H}uman{E}val - A Multilingual Benchmark to Evaluate Large Language Models for Code Generation",
    author = "Raihan, Nishat  and
      Anastasopoulos, Antonios  and
      Zampieri, Marcos",
    editor = "Chiruzzo, Luis  and
      Ritter, Alan  and
      Wang, Lu",
    booktitle = "Proceedings of the 2025 Conference of the Nations of the {A}mericas Chapter of the {A}ssociation for {C}omputational {L}inguistics: Human Language Technologies (Volume 1: Long Papers)",
    month = apr,
    year = "2025",
    address = "Albuquerque, New Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.naacl-long.570/",
    doi = "10.18653/v1/2025.naacl-long.570",
    pages = "11432--11461",
    ISBN = "979-8-89176-189-6"
}
```

</details>

Questions: [mraihan2@gmu.edu](mailto:mraihan2@gmu.edu)
