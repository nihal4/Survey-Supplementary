---
library_name: transformers
base_model: Qwen/Qwen2.5-1.5B-Instruct
license: apache-2.0
language:
- bn
- en
tags:
- mathematics
- bangla
- bengali
- education
- lora
- qwen2.5
- baamr-bench
pipeline_tag: text-generation
datasets:
- mdhamidhosen/BaAMR-Math-12K
---

# BaAMR-Math-12K merged model — Qwen2.5-1.5B-Instruct

A LoRA adapter for `Qwen/Qwen2.5-1.5B-Instruct` fine-tuned on **BaAMR-Math-12K**, a bilingual (Bangla + English) mathematics dataset of 12,000 records covering all 61 chapters of the NCTB Classes 6–10 mathematics textbooks (2026 editions), each record grounded to a textbook page in both editions. It supersedes the 577-record pilot adapter `mdhamidhosen/baamr-math-qwen2.5-1.5b-lora-pilot-577`.

The model answers a secondary-school mathematics problem in the language of the question, shows its steps, and ends with `Answer: …` / `উত্তর: …`.

## Training

| | |
|---|---|
| Base model | `Qwen/Qwen2.5-1.5B-Instruct` |
| Method | LoRA (bf16 base); r=16, α=32, dropout 0.05 on q/k/v/o/gate/up/down; completion-only loss |
| Data | BaAMR-Math-12K `train` split: 9,600 records, 50% Bangla / 50% English |
| Schedule | 2 epochs, 8 × 4 = 32 sequences per optimiser step, AdamW lr 0.0001, cosine, 5% warm-up |
| Hardware | Tesla T4 (Google Colab), bf16 emulated; 600 optimiser steps in 8.3 h |
| Selection | lowest validation loss on a 400-record subset of `validation`, every 100 steps |
| Best checkpoint | step 100, validation loss 0.4179 |
| Final training loss | 0.0025498466566205025 |

## Evaluation — held-out `test` split

1,200 records (100 item families × 6 cells × 2 languages) that share **no template** with training: whole skill templates were held out, so no numeric variant of any training item is in the test set. Greedy decoding, graded with the BaAMR-Bench bilingual grader (Bengali digits folded, fractions compared numerically, MCQ letters accepted).

| model | accuracy (5×2 grid) | Bangla | English | robust acc. bn | robust acc. en |
|---|---|---|---|---|---|
| zero-shot base `Qwen/Qwen2.5-1.5B-Instruct` | 48.60% | 32.17% | 66.17% | 12.00% | 33.00% |
| **this adapter** | **49.60%** | 41.67% | 58.50% | 24.00% | 35.00% |

*Robust accuracy* = fraction of families answered correctly on **all five** cells (original, numeric, varname, distractor, reorder) within a language.

Accuracy by language × perturbation:

| lang | original | numeric | varname | distractor | reorder | framing |
|---|---|---|---|---|---|---|
| bn | 41.00% | 42.00% | 37.00% | 43.00% | 39.00% | 48.00% |
| en | 58.00% | 58.00% | 57.00% | 61.00% | 60.00% | 57.00% |

By question type:

| type | n | accuracy |
|---|---|---|
| conceptual | 60 | 48.33% |
| error_identification | 168 | 44.05% |
| mathematical_reasoning | 96 | 13.54% |
| mcq | 288 | 52.08% |
| multi_step | 48 | 33.33% |
| short_answer | 240 | 67.92% |
| true_false | 156 | 55.13% |
| word_problem | 144 | 48.61% |

By class:

| class | n | accuracy |
|---|---|---|
| 10 | 240 | 41.67% |
| 6 | 240 | 46.67% |
| 7 | 240 | 70.42% |
| 8 | 240 | 40.83% |
| 9 | 240 | 50.83% |

Per-record generations and the metrics files are in `evaluation/`. Note the training log: validation loss was lowest at step 100 and rose afterwards (0.42 → 0.59), so this run is over-trained; a v2 recipe (1 epoch, lr 5e-5, early stopping) is planned as `…-lora-12k-v2`.

## Usage

```python
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(base)
model = AutoModelForCausalLM.from_pretrained(base, dtype=torch.bfloat16, device_map="auto")
model = PeftModel.from_pretrained(model, "mdhamidhosen/baamr-math-qwen2.5-1.5b-lora-12k").eval()

messages = [
    {"role": "system", "content": "তুমি বাংলাদেশের মাধ্যমিক শিক্ষার্থীদের একজন গণিত শিক্ষক। সমস্যাটি ধাপে ধাপে সমাধান করো এবং শেষ লাইনে 'উত্তর: ...' আকারে চূড়ান্ত উত্তর দাও।"},
    {"role": "user", "content": "প্রশ্নটির উত্তর দাও।\nএকটি সমকোণী ত্রিভুজের লম্ব বাহু দুটি 5 সেমি ও 12 সেমি; অতিভুজ h ধরি। h নির্ণয় করো।"},
]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(model.device)
out = model.generate(**inputs, max_new_tokens=256, do_sample=False)
print(tok.decode(out[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

English system prompt used in training: *"You are a mathematics tutor for Bangladeshi secondary students. Solve the problem step by step and give the final answer on the last line as 'Answer: ...'."*

## Limitations

* Trained on template-generated problems (2–4 reasoning steps, secondary-school scope); not a general maths model, not evaluated on GSM8K-style or olympiad problems.
* The dataset was audited automatically (2,000/2,000 independent re-solves) but has **not** been reviewed by independent mathematics teachers or bilingual annotators.
* A 1.5B model: expect arithmetic slips on longer multi-step items; see the language table for the Bangla–English gap.
* Not for high-stakes use; verify answers.

## Dataset

BaAMR-Math-12K — 12,000 records, 1,000 item families, 206 templates, 61 chapters; splits 9,600 / 1,200 / 1,200 by whole template. Part of *BaAMR-Bench: A Bangla–English Benchmark for Robust Algorithmic and Mathematical Reasoning in Large Language Models* (2026).


> Merged full bf16 model; the adapter-only version is `mdhamidhosen/baamr-math-qwen2.5-1.5b-lora-12k`.
