---
language:
- bn
- en
library_name: transformers
tags:
- merge
- mergekit
- low-resource
- mathematics
base_model:
- Qwen/Qwen2.5-1.5B
- Qwen/Qwen2.5-1.5B-Instruct
license: apache-2.0
---

# 🇧🇩 Polymath-1.5B-Bengali-Math

This model is a merge of `Qwen/Qwen2.5-1.5B` and `Qwen/Qwen2.5-1.5B-Instruct` created using the **SLERP** method.

## 🧪 Research Goal
To investigate the "Capacity Gap" in low-resource languages (like Bengali) when transferring mathematical reasoning capabilities without fine-tuning.

## 📊 Performance
- **English Math Logic:** 60% Accuracy (Retained Logic) ✅
- **Bengali Math Logic:** 0% Accuracy (Capacity Constraint Revealed) ⚠️

## 🛠️ Method
Merged using [MergeKit](https://github.com/arcee-ai/mergekit) with the following config:
- **Method:** SLERP
- **Precision:** float16
- **Parameters:** 1.5 Billion

*Created for research and educational purposes.*
