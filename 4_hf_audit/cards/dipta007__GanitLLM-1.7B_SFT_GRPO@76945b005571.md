---
library_name: transformers
license: apache-2.0
base_model: Qwen/Qwen3-1.7B
pipeline_tag: text-generation
language:
  - bn
  - en
tags:
  - math
  - bengali
  - reasoning
  - grpo
datasets:
  - dipta007/Ganit
---

# GanitLLM-1.7B_SFT_GRPO

<p align="center">
  <a href="https://arxiv.org/abs/2601.06767">
    <img src="https://img.shields.io/badge/%F0%9F%94%A5_Accepted_at-ACL_2026_(Findings)_%F0%9F%94%A5-b12a00?style=for-the-badge&labelColor=ffb300" alt="Accepted at ACL 2026 (Findings)">
  </a>
</p>

[![ACL 2026 (Findings)](https://img.shields.io/badge/ACL%202026-Findings-blue)](https://arxiv.org/abs/2601.06767)
[![Paper](https://img.shields.io/badge/arXiv-2601.06767-red)](https://arxiv.org/abs/2601.06767)
[![Project Page](https://img.shields.io/badge/Project-Page-green)](https://dipta007.github.io/GanitLLM/)
[![Dataset](https://img.shields.io/badge/HuggingFace-Dataset-yellow)](https://huggingface.co/datasets/dipta007/Ganit)
[![Models](https://img.shields.io/badge/HuggingFace-Models-orange)](https://huggingface.co/collections/dipta007/ganitllm)
[![GitHub](https://img.shields.io/badge/GitHub-Code-blue)](https://github.com/dipta007/GanitLLM)

## Highlights

**GanitLLM-1.7B_SFT_GRPO** is a compact Bengali mathematical reasoning model trained with SFT followed by standard GRPO. Key improvements over the base Qwen3-1.7B model:

- **+38.4 accuracy** on Bn-MGSM benchmark (15.2 → 53.6)
- **+52.8 accuracy** on Bn-MSVAMP benchmark (14.1 → 66.9)
- **88.32% Bengali reasoning** (vs 19.64% for base model)
- **81.6% fewer tokens** in generated solutions (1124 → 207 words)

## Model Overview

| Property | Value |
|----------|-------|
| **Model Type** | Causal Language Model |
| **Base Model** | Qwen/Qwen3-1.7B |
| **Parameters** | 1.7B |
| **Training** | SFT + GRPO |
| **Context Length** | 4,096 tokens |
| **Language** | Bengali, English |

## Training Details

This model was trained using a two-stage pipeline:

1. **Supervised Fine-Tuning (SFT)**: Trained on GANIT-SFT (~11k examples) to ground reasoning in Bengali
2. **GRPO**: Standard reinforcement learning with random sampling on GANIT-RLVR (~7.3k examples)

### Reward Functions
- **Format Reward**: Validates `<think>` and `<answer>` tag structure
- **Correctness Reward**: +2.0 for Bengali answer match, +1.0 for English match
- **Bengali Reasoning Reward**: Ensures >80% Bengali text in reasoning

## Quickstart

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "dipta007/GanitLLM-1.7B_SFT_GRPO"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

problem = "একটি দোকানে ১২টি আপেল আছে। যদি ৫টি আপেল বিক্রি হয়, তাহলে কতটি আপেল বাকি থাকবে?"

prompt = f"""A conversation takes place between the user and the assistant. The user asks a question, and the assistant solves the problem. Please reason step by step in Bengali, and put your final answer in the <answer> </answer> tags.

Question: {problem}"""

messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(**model_inputs, max_new_tokens=2048, temperature=0.7)
output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
response = tokenizer.decode(output_ids, skip_special_tokens=True)
print(response)
```

### Using vLLM

```bash
vllm serve dipta007/GanitLLM-1.7B_SFT_GRPO --max-model-len 4096
```

## Performance

| Model | Bn-MGSM | Bn-MSVAMP | Avg. Words | Bengali % |
|-------|---------|-----------|------------|-----------|
| Qwen3-1.7B (base) | 15.20 | 14.10 | 1124 | 19.64% |
| **GanitLLM-1.7B_SFT_GRPO** | **53.60** | **66.90** | **207** | **88.32%** |

## Related Models

| Model | Parameters | Training | Link |
|-------|------------|----------|------|
| GanitLLM-4B_SFT_GRPO | 4B | SFT + GRPO | [Link](https://huggingface.co/dipta007/GanitLLM-4B_SFT_GRPO) |
| GanitLLM-1.7B_SFT_CGRPO | 1.7B | SFT + CGRPO | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT_CGRPO) |
| **GanitLLM-1.7B_SFT_GRPO** | 1.7B | SFT + GRPO | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT_GRPO) |
| GanitLLM-1.7B_CGRPO | 1.7B | CGRPO | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_CGRPO) |
| GanitLLM-0.6B_SFT_GRPO | 0.6B | SFT + GRPO | [Link](https://huggingface.co/dipta007/GanitLLM-0.6B_SFT_GRPO) |

## Citation

```bibtex
@inproceedings{dipta2026ganitllm,
  title={GanitLLM: Difficulty-Aware Bengali Mathematical Reasoning through Curriculum-GRPO},
  author={Shubhashis Roy Dipta and Khairul Mahbub and Nadia Najjar},
  booktitle={Findings of the Association for Computational Linguistics: ACL 2026},
  year={2026},
  eprint={2601.06767},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2601.06767},
}
```

## License

This model is released under the Apache 2.0 License.
