---
base_model: Qwen/Qwen3-1.7B
library_name: peft
pipeline_tag: text-generation
tags:
- qwen3
- lora
- qlora
- peft
- maasathi
- maternal-health
- classifier
language:
- bn
- en
license: apache-2.0
---

# MaaSathi Qwen3-1.7B Query Classifier LoRA

LoRA adapter fine-tuned from `Qwen/Qwen3-1.7B` for MaaSathi maternal-health query classification.

This repository contains the PEFT/LoRA adapter, not a merged full model.

## Task

The model receives a MaaSathi user query and returns strict JSON classification fields such as:

- `query_language`
- `query_type`
- `urgency`
- `mother_intent`
- `medical_entities`

## Before Finetuning

```json
{
  "model": "Qwen/Qwen3-1.7B",
  "rows": 311,
  "json_valid": 0.9807073954983923,
  "urgency_acc": 0.8263665594855305,
  "type_acc": 0.0,
  "lang_acc": 0.0,
  "emergency_total": 56,
  "emergency_recall": 0.4642857142857143
}
```

## After Finetuning

```json
{
  "model: "maasathi-qwen3-1-7b-query-classifier-lora"
  "rows": 311,
  "json_valid": 1.0,
  "urgency_acc": 0.9871382636655949,
  "type_acc": 0.9742765273311897,
  "lang_acc": 0.9839228295819936,
  "emergency_total": 56,
  "emergency_recall": 0.9821428571428571
}
```

## Safety Note

This model is a classifier component only. It must not replace deterministic emergency triage rules or clinical judgment.
