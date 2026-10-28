---
license: apache-2.0
base_model: Qwen/Qwen3-8B
language:
- en
- bn
library_name: transformers
pipeline_tag: text-generation
tags:
- trl
- sft
- tool-calling
- function-calling
- agent
- on-device
- eyla
- bangla
- qwen3
---

# Eyla · Qwen3-8B Tools v2

A compact, **on-device tool-calling model** for [Eyla](https://github.com/Adiuk24) — a Bangladesh-first, offline, agentic AI operating system. It is a full supervised fine-tune of **Qwen3-8B** that emits structured tool calls from natural-language intent in **English, Bangla (বাংলা), and Banglish**, and is small and fast enough to run locally (4-bit ≈ 4.3 GB, ~5 s/turn on Apple Silicon).

The approach follows *compiling tools & procedures into the weights* (arXiv:2605.22502): the model is trained to know Eyla's tools and their call format directly, so at inference it needs only a short system prompt and **no tool schemas** in context — it decides which tool to call from intent.

## Model details

- **Developed by:** Adioris / Eyla
- **Model type:** Decoder-only LLM, SFT for agentic tool-calling
- **Base model:** [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B)
- **Languages:** English, Bangla, Banglish (code-switched Bangla/English)
- **License:** Apache-2.0 (inherits Qwen3-8B)
- **Format:** `safetensors` (bf16). On-device serving uses a 4-bit quantization.

## Intended use

- **On-device agent brain / tool-router** inside an agent harness that parses tool calls and executes them (file read/write, shell, web search/fetch, memory, etc.).
- Offline, privacy-preserving assistant workflows where sending data to the cloud is not an option.
- Bangla-first products that need tool-calling from Bengali or Banglish requests.

### Tool-call format

The model emits calls as:

```
<tool_call>{"name": "file_read", "arguments": {"path": "/path/to/file"}}</tool_call>
```

Example — the user names no tool; the model infers it:

```
User: What is on my shopping list? The file is /tmp/shopping.md
Model: <tool_call>{"name": "file_read", "arguments": {"path": "/tmp/shopping.md"}}</tool_call>
```

Tool names follow Eyla's registry (`file_read`, `file_write`, `web_search`, `web_fetch`, `shell_exec`, `memory_recall`, …); a harness can alias common variants (`read_file` → `file_read`, `terminal` → `shell_exec`).

## How to get started

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("Adiuk/eyla-qwen3-8b-tools-v2")
model = AutoModelForCausalLM.from_pretrained("Adiuk/eyla-qwen3-8b-tools-v2", torch_dtype="bfloat16", device_map="auto")

msgs = [
    {"role": "system", "content": "You are Eyla, an offline assistant with tools. Emit tool calls as <tool_call>{\"name\":...,\"arguments\":{...}}</tool_call>."},
    {"role": "user", "content": "read the file notes.txt"},
]
inputs = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to(model.device)
out = model.generate(inputs, max_new_tokens=256, do_sample=False)
print(tok.decode(out[0][inputs.shape[1]:], skip_special_tokens=True))
```

For fast local inference, quantize to 4-bit (e.g. MLX or GGUF) and serve behind an OpenAI-compatible endpoint.

## Training

- **Method:** full-parameter SFT (TRL `SFTTrainer`).
- **Data:** ~5.3k tool-calling conversations (train) + ~0.6k validation, spanning English / Bangla / Banglish action requests mapped to Eyla tools.
- **Hyperparameters:** 3 epochs · lr 2e-5 (cosine, warmup 0.03) · batch 4 · `adamw_bnb_8bit` · bf16 · max_len 2048 · gradient checkpointing.
- **Hardware:** 1× H100.

## Evaluation

Measured **end-to-end inside the Eyla agent harness** (headless, one request at a time) on an 8-task live tool-reliability eval — implicit file read/write, explicit tool use, multi-step, a factual (no-tool) task, and a Bangla file-read:

| Metric | Result |
|---|---|
| Tasks passed | **5 / 8** |
| Latency | **~5 s / task** (4-bit, Apple Silicon) |
| Size (4-bit) | ~4.3 GB |

Strengths: reliable tool **emission** and format, strong on explicit tool use, multi-step counting, and read tasks; **fast** and **light**. It is best used as the tool-caller within an agent loop rather than as a standalone chat model.

## Bias, risks, and limitations

- **Small model.** Implicit tool selection for out-of-distribution or vague requests is less reliable than a large cloud model; use it inside a harness with validation, approval gates for dangerous tools, and error-feedback retries.
- **Coding-agent tendencies.** Trained on developer-style traces, it can over-prefer `shell_exec`/exploration for simple tasks and occasionally rewrite a provided file path — mitigate with a path-repair guard and tool-scoping in the harness.
- **Safety.** Tool execution must be gated by the host application (permission modes, approval for destructive/outward actions). The model does not enforce safety on its own.

## About Eyla

Eyla is an offline, cross-platform agentic AI OS focused on Bangladesh — running capable assistants fully on-device (16–24 GB consumer hardware) with Bangla as a first-class language.

## Citation

Approach inspired by compiling tools/procedures into model weights (arXiv:2605.22502). Built on Qwen3-8B (Qwen team, Apache-2.0).

```
@misc{eyla-qwen3-8b-tools-v2,
  title  = {Eyla · Qwen3-8B Tools v2 — on-device tool-calling (EN/BN/Banglish)},
  author = {Adioris / Eyla},
  year   = {2026},
  howpublished = {\url{https://huggingface.co/Adiuk/eyla-qwen3-8b-tools-v2}}
}
```

## Author & research

- 🌐 Website: [arifadito.com](https://arifadito.com)
- 💻 GitHub: [github.com/Adiuk24](https://github.com/Adiuk24)
- 📄 Eyla identity paper: [arXiv:2604.00009](https://arxiv.org/abs/2604.00009)
- 🔧 Rust ML training verification tooling: [gradient-flow-arbiter](https://github.com/Adiuk24/gradient-flow-arbiter)
