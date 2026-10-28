---
license: apache-2.0
base_model:
  - DavidAU/Qwen3.6-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking
library_name: transformers
pipeline_tag: text-generation
tags:
  - text-generation
  - chat
  - multilingual
  - reasoning
  - coding
  - qwen
  - yarn
  - long-context
  - 1m-context
  - bangla
language:
  - en
  - bn
  - multilingual
license_name: apache-2.0
---

# 🧠 Droplychee-2.0-40B

> A multilingual long-context language model developed by **Droplychee**, built upon the Qwen family and extended through full fine-tuning and architectural modifications.

## Overview

Droplychee-2.0-40B is a decoder-only transformer model designed for multilingual reasoning, software engineering, long-context understanding, and instruction following. The model is derived from the Qwen family and further adapted through full fine-tuning using curated multilingual instruction datasets.

The project focuses on delivering strong performance in English and Bangla while maintaining support for over 40 languages.

## Key Features

- 🌍 Supports 40+ languages
- 📚 Maximum context length of 1,000,000 tokens
- 🧵 YaRN-based context extension
- 💻 Optimized for software engineering and coding tasks
- 🧠 Advanced reasoning and instruction following
- 📄 Long-document analysis and summarization
- 🤖 Agent-oriented workflows and tool use

## Model Details

| Property | Value |
|----------|-------|
| Model Name | Droplychee-2.0-40B |
| Organization | Droplychee |
| Base Model | DavidAU/Qwen3.6-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking |
| Architecture | Decoder-only Transformer |
| Training Method | Full Fine-Tuning |
| Context Length | 1,000,000 tokens |
| Context Extension | YaRN |
| Languages | 40+ |
| License | Apache-2.0 |

## Architecture

Droplychee-2.0-40B is derived from the Qwen architecture with additional modifications introduced during development.

Key architectural characteristics include:

- Decoder-only transformer architecture
- Rotary Position Embeddings (RoPE)
- YaRN-based long-context extension
- Optimized KV-cache handling
- Flash Attention support (where available in the serving stack)
- Full supervised instruction fine-tuning

## Training

The model was fine-tuned using a curated multilingual instruction corpus emphasizing:

- General reasoning
- Coding and software engineering
- Mathematics
- Multilingual dialogue
- Long-context comprehension
- Agent-oriented tasks

Approximate training statistics:

| Item | Value |
|------|-------|
| High-quality instruction pairs | ~500K |
| Training tokens | ~100M–1B |
| Training Platform | Unsloth Studio |
| GPU Hardware | 3× NVIDIA RTX PRO 6000 Blackwell Server Edition |

## Context Extension

Droplychee-2.0-40B supports a maximum context length of **1,000,000 tokens** through **YaRN (Yet another RoPE extensioN)**.

YaRN extends the effective context window while preserving compatibility with Rotary Position Embeddings. Long-context performance may vary depending on the inference engine, hardware resources, and serving configuration.

## Supported Languages

The model is optimized for multilingual instruction following and has been evaluated primarily on English and Bangla. It also supports more than 40 languages, including Hindi, Arabic, Chinese, Japanese, Korean, French, German, Spanish, Portuguese, and Russian.

## Intended Use

Recommended applications include:

- Conversational AI
- Coding assistants
- Research assistance
- Educational tools
- Long-document summarization
- Retrieval-Augmented Generation (RAG)
- AI agents
- Software engineering workflows

## Limitations

- Outputs may contain factual inaccuracies or hallucinations.
- Performance varies across languages and domains.
- Independent third-party evaluation has not yet been completed.
- Users should verify outputs before relying on them for high-impact decisions.

## Responsible Use

This model is intended for research and general-purpose AI applications. Users are responsible for ensuring compliance with applicable laws, regulations, and ethical guidelines.

## Attribution

This project is derived from:

**DavidAU/Qwen3.6-40B-Claude-4.6-Opus-Deckard-Heretic-Uncensored-Thinking**

Please refer to the original model card and license for upstream attribution requirements.

## License

This model is distributed under the **Apache License 2.0**.

Users must also comply with the license terms of the upstream base model where applicable.
# Evaluation

> **Note:** The following results are based on **internal evaluation** conducted by the Droplychee team. Independent third-party verification has not yet been completed.

## Reasoning Benchmarks

| Benchmark | Score | Evaluation |
|-----------|------:|------------|
| MMLU | 90.8 | Internal |
| MMLU-Pro | 89.5 | Internal |
| GPQA Diamond | 87.0 | Internal |
| MGSM | 90.4 | Internal |
| Humanity's Last Exam | +11 pp | Internal |
| MMMU | 80.7 | Internal |

---

## Coding Benchmarks

| Benchmark | Score | Evaluation |
|-----------|------:|------------|
| HumanEval | 92.0 | Internal |
| LiveCodeBench | 76.8 | Internal |
| SWE-Bench Verified | 80.9 | Internal |
| TerminalBench 2.0 | 59.3 | Internal |
| SpreadsheetBench | 64.25 | Internal |
| SpreadsheetBench + Python | 92.77 | Internal |
| APEX-SWE | 38.5 | Internal |

---

## Agent Benchmarks

| Benchmark | Score | Evaluation |
|-----------|------:|------------|
| τ² Telecom | 98.2 | Internal |
| τ² Retail | 88.9 | Internal |
| TerminalBench Hard | 44.0 | Internal |
| n8n AI Benchmark | 66.0 | Internal |

---

## Research Benchmarks

| Benchmark | Score | Evaluation |
|-----------|------:|------------|
| Elicit Research Accuracy | 96.5 | Internal |
| Report Writing | 62.0 | Internal |
| METR Agency Benchmark | ~5 Hours | Internal |

---

## Artificial Analysis

| Benchmark | Score | Evaluation |
|-----------|------:|------------|
| Intelligence Index | 70.0 | Internal |
| Omniscience | 10.0 | Internal |

> **Disclaimer:** These benchmark results are derived from the Droplychee team's internal evaluation pipeline. Results may vary depending on hardware, inference engine, prompt format, evaluation methodology, and software versions. Independent third-party verification is planned for future releases.

For the latest documentation, technical reports, and official releases, please visit the official Droplychee GitHub repository.
https://github.com/DropLychee/droplychee-2.0-40b


droplychee-2.0-40b/
│
├── README.md
├── LICENSE
├── MODEL_CARD.md
├── TECHNICAL_REPORT.md
├── SYSTEM_CARD.md
├── EVALUATION.md
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── docs/
│   ├── architecture.md
│   ├── training.md
│   ├── datasets.md
│   ├── tokenizer.md
│   ├── inference.md
│   ├── benchmarks.md
│   ├── deployment.md
│   ├── safety.md
│   ├── governance.md
│   └── roadmap.md
├── assets/
│   ├── logo.png
│   ├── banner.png
│   ├── architecture.svg
│   └── benchmark_charts/
├── examples/
│   ├── transformers.py
│   ├── vllm.py
│   ├── llama_cpp.py
│   └── openai_api.py
├── scripts/
│   ├── evaluate.py
│   ├── benchmark.py
│   ├── convert_gguf.py
│   └── export.py
└── paper/
    ├── Droplychee-2.0-40B_Technical_Report.pdf
    ├── Droplychee-2.0-40B_Technical_Report.md
    └── references.bib