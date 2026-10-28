---
language:
- bn
- en
license: apache-2.0
library_name: transformers
pipeline_tag: text-generation
base_model: HuggingFaceTB/SmolLM2-1.7B
tags:
- banglish
- bengali
- conversational
- fine-tuned
- smollm2
- local-inference
- safety-aligned
- low-resource-languages
- code-switching
- perception-layers
- emotional-intelligence
datasets:
- sifat-febo/banglish_bench
---

# Banglish Companion: Now It Knows How You Feel

### Reads the message before it answers

A chatbot for Banglish — romanized Bengali, typed the way people actually
type it. It works out what the message is asking for, then answers.

```
you    aj mood bhalo na
model  mama mood shob change hoy! Tui ki feel korchish?
```

Built on [SmolLM2-1.7B](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B),
further trained on Banglish conversation. The layer that reads the message
ships on its own as
[banglish-ontor](https://huggingface.co/sifat-febo/banglish-ontor), which is
where to look for what it reads and how to put it in front of anything else.

&nbsp;

## Banglish e Model Card

**ei model ta ki?** — ekta Banglish chatbot. ekhon shune, bujhe.

**ki pare?** adda, khela, gaan, khabar. mon kharap er kotha shune.

**ki parbe na?** English/Bengali script na. choto model — sometimes bhul. doctor/lawyer na.

**bipod hole?** kichu message er uttor model dey na — `companion.py` age
oigulo dekhe ney, tomar kichu korte hobe na.

&nbsp;

## Use it

```bash
pip install transformers torch huggingface_hub
hf download sifat-febo/banglish-companion --local-dir banglish
python banglish/companion.py
```

That is the whole thing: it answers, then keeps talking. In your own code,
`from companion import reply` is the only import you need — it reads the
message with the `ontor` layer that ships here, checks the guard before the
model, and builds the ChatML prompt this model was trained on.

The weights are 6.8 GB (fp32) — plan for that on download and in RAM. Your
own personal computer, your CPU, nothing leaves it.

&nbsp;

**Smaller, and newer.** Same weights quantized:
[bangla-banglish-companion-gguf](https://huggingface.co/sifat-febo/bangla-banglish-companion-gguf)
for llama.cpp, from 1.06 GB, and
[bangla-banglish-companion-mlx](https://huggingface.co/sifat-febo/bangla-banglish-companion-mlx)
for Macs, 1.9 GB. There is also a newer model built on a 3B base —
[banglish-companion-3b](https://huggingface.co/sifat-febo/banglish-companion-3b)
and its [Mac build](https://huggingface.co/sifat-febo/banglish-companion-3b-mlx)
— which answers shorter and stays closer to the question.

## What the layer changes

Take the layer away and the same weights answer the same message like this:

```
You:            aj mood bhalo na
weights only:   mama mood bhalo feel kor! Jodi sad hole — ekhon karo
                kichu kore khujho. Tui ki feel korte chao? Sometimes
                just expressing emotion e kichu korba feel kore.
```

Longer, and answering a question nobody asked. The reply at the top of this
page is the same weights with the layer in front.
[Why it is small, and why it is always on →](https://huggingface.co/sifat-febo/banglish-companion/blob/main/THESIS.md)

&nbsp;

## Picked by the Author, Not Numbers

**What's published here is safetensors.** The comparison below is a record of what we did locally — not a menu of downloads.

We converted all three formats (F16, Q8_0, Q4_K_M) for our own use and checked each one against the weights it came from. We compared them by hand, on the same prompts.

Q8_0 read tightest to us: better listening behavior, less advice-dumping than F16.

&nbsp;

## Limits and what it does not answer

Some messages are answered from a file that ships here rather than by the
model, and `reply()` checks that first on every turn. Written text, no
generation, nothing for you to wire up.

&nbsp;

## Specs

| | |
|:--|:--|
| **Model** | SmolLM2-1.7B fine-tune + ~0.5M parameter perception |
| **Perception** | a small layer reads the message first — [banglish-ontor](https://huggingface.co/sifat-febo/banglish-ontor) |
| **Fixed answers** | some messages are answered from a file, not by the model |
| **Runtime** | CPU. No GPU. |
| **Published format** | safetensors |

Which one suits you depends on your machine.

| Format | GGUF Size | Note |
|:--|:--|:--|
| Q4_K_M | 1.06 GB | Smallest |
| Q8_0 | 1.82 GB | What we run locally |
| F16 | 3.42 GB | Closest to the published weights |

**Limitations:** Banglish only. May hallucinate. Not a professional advisor. Safety is best-effort; a small share of edge cases involve borderline deflections.

&nbsp;

---

| Component | Status |
|:--|:--|
| Model weights — 1.7B base + perception layers | **Open** |
| [BanglishBench](https://huggingface.co/datasets/sifat-febo/banglish_bench) (smoke test) | **Open** |
| Inference pipeline (`ontor/perceive.py`) | **Open** |
| The file that answers instead of the model | **Open** |
| Training data, pipeline and settings | Closed |

&nbsp;

## AI Disclosure

The author designed the system, chose the base models, ran all training and
measurement on the author's own machine, read the models' conversations, and
chose what to publish and what to withhold. [Claude Code](https://claude.ai)
(Anthropic) was used as a coding and writing tool under that direction.

## License

Apache 2.0

Cite the technical report, which describes how the models were built,
trained and measured: <https://doi.org/10.5281/zenodo.22371896>

```bibtex
@misc{febo2026banglishcompanion,
  author    = {Febo, Sifat},
  title     = {Banglish Companion: Small Chat Models for Romanized Bengali
               — Technical Report},
  year      = {2026},
  month     = sep,
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.5281/zenodo.22371896},
  url       = {https://doi.org/10.5281/zenodo.22371896},
  note      = {Repository: sifat-febo/banglish-companion}
}
```
