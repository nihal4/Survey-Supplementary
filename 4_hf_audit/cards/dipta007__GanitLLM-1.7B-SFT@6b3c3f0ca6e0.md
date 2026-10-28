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
  - sft
datasets:
  - dipta007/Ganit
---

# GanitLLM-1.7B_SFT

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

**GanitLLM-1.7B_SFT** is a Bengali mathematical reasoning model trained with Supervised Fine-Tuning on the GANIT dataset. This model serves as the foundation for further RL training (GRPO/CGRPO). Key improvements over the base Qwen3-1.7B model:

- **+33.60 accuracy** on Bn-MGSM benchmark (15.20 → 48.80)
- **+50.50 accuracy** on Bn-MSVAMP benchmark (14.10 → 64.60)
- **87.79% Bengali reasoning** (vs 19.64% for base model)
- **77.5% fewer words** in generated solutions (1124 → 253 words)

> **Note**: This is the SFT-only checkpoint. For best results, use the RL-enhanced versions: [GanitLLM-1.7B_SFT_CGRPO](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT_CGRPO) or [GanitLLM-1.7B_SFT_GRPO](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT_GRPO).

## Model Overview

| Property | Value |
|----------|-------|
| **Model Type** | Causal Language Model |
| **Base Model** | Qwen/Qwen3-1.7B |
| **Parameters** | 1.7B |
| **Training** | Supervised Fine-Tuning |
| **Context Length** | 4,096 tokens |
| **Language** | Bengali, English |

## Training Details

This model was trained with a single-stage pipeline:

1. **Supervised Fine-Tuning (SFT)**: Trained on GANIT-SFT (~11k examples) to ground reasoning in Bengali

### Training Data
- **Dataset**: GANIT-SFT (11,023 examples)
- **Format**: Bengali math problems with chain-of-thought reasoning
- **Structure**: `<think>` tags for reasoning, `<answer>` tags for final answer

## Quickstart

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "dipta007/GanitLLM-1.7B_SFT"

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
vllm serve dipta007/GanitLLM-1.7B_SFT --max-model-len 4096
```

## Performance

| Model | Bn-MGSM | Bn-MSVAMP | Avg. Words | Bengali % |
|-------|---------|-----------|------------|-----------|
| Qwen3-1.7B (base) | 15.20 | 14.10 | 1124 | 19.64% |
| **GanitLLM-1.7B_SFT** | **48.80** | **64.60** | **253** | **87.79%** |

## Related Models

| Model | Parameters | Training | Link |
|-------|------------|----------|------|
| GanitLLM-1.7B_SFT_CGRPO | 1.7B | SFT + CGRPO | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT_CGRPO) |
| GanitLLM-1.7B_SFT_GRPO | 1.7B | SFT + GRPO | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT_GRPO) |
| **GanitLLM-1.7B_SFT** | 1.7B | SFT | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_SFT) |
| GanitLLM-1.7B_CGRPO | 1.7B | CGRPO | [Link](https://huggingface.co/dipta007/GanitLLM-1.7B_CGRPO) |

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
