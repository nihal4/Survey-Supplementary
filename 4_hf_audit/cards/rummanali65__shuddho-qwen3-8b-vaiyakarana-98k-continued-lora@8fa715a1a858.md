---
library_name: peft
base_model: Qwen/Qwen3-8B
base_model_relation: adapter
datasets:
- Vacaspati/Vaiyakarana
language:
- bn
license: apache-2.0
tags:
- lora
- peft
- bangla
- grammar-correction
- spelling-correction
- shuddho
- continued-training
pipeline_tag: text-generation
---

# Shuddho Qwen3-8B Vaiyakarana 98K Continued LoRA

A continued LoRA adapter for Bangla grammar, spelling,
punctuation, spacing and writing correction.

## Base model

Qwen/Qwen3-8B

## Continued from

rummanali65/shuddho-qwen3-8b-vaiyakarana-83k-continued-lora

## Cumulative training path

- V1: 10K examples
- V2: additional 20K examples
- V3: additional 23K training rows
- V4: additional 30K examples
- V5: additional 15K examples

Total cumulative training exposure: approximately 98K examples.

## Important

This repository contains the LoRA adapter only.

For inference, load Qwen/Qwen3-8B first and then attach this
adapter using PEFT.
