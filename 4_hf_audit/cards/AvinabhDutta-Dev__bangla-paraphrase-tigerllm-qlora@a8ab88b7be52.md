---
license: cc-by-4.0
base_model: md-nishat-008/TigerLLM-1B-it
tags:
  - bengali
  - bangla
  - paraphrase-generation
  - causal-lm
  - qlora
  - merged
  - text-generation
datasets:
  - csebuetnlp/BanglaParaphrase
language:
  - bn
library_name: transformers
pipeline_tag: text-generation
widget:
  - text: "নিচের বাক্যটি ভিন্নভাবে, একই অর্থ বজায় রেখে লিখুন। ইউনিভার্সিটির ল্যাবে কাজ করতেন।"
    example_title: "Short sentence"
  - text: "নিচের বাক্যটি ভিন্নভাবে, একই অর্থ বজায় রেখে লিখুন। কিন্তু আসলেই কি সবাই অভাগা?"
    example_title: "Question form"
model-index:
  - name: bangla-paraphrase-tigerllm-qlora
    results:
      - task:
          type: text-generation
        dataset:
          name: BanglaParaphrase
          type: csebuetnlp/BanglaParaphrase
          split: test
        metrics:
          - name: BLEU
            type: bleu
            value: 18.69
          - name: ROUGE-L
            type: rouge_l
            value: 0.466
          - name: BERTScore F1
            type: bertscore
            value: 0.942
          - name: PINC
            type: pinc
            value: 0.777
---

# Bengali Paraphrase Benchmark - TigerLLM (QLoRa)

A [QLoRA](https://arxiv.org/abs/2305.14314) fine-tune of [md-nishat-008/TigerLLM-1B-it](https://huggingface.co/md-nishat-008/TigerLLM-1B-it) for **Bengali paraphrase generation**, trained on the [BanglaParaphrase](https://huggingface.co/datasets/csebuetnlp/BanglaParaphrase) dataset. The LoRA adapter has been **merged into the base weights** — this is a complete, standalone model; no separate adapter loading is required.

This model is one of four architectures compared in a broader study, **"Beyond BLEU: Evaluating Automated Metric Reliability for Bengali Paraphrase Generation"** ([GitHub repo](https://github.com/AvinabhDutta-Dev/bangla-paraphrase-benchmark)), which benchmarks full fine-tuning vs. QLoRA and validates standard automated metrics (BLEU, ROUGE-L, BERTScore, PINC) against an LLM-as-a-judge.

> **TL;DR:** Matches full-fine-tuned BanglaT5 on BLEU/BERTScore while training only ~5% of the parameters (13M vs. 247M).

## Model Details

| | |
|---|---|
| Base model | `md-nishat-008/TigerLLM-1B-it` |
| Architecture | Causal decoder-only LM (Gemma-based) |
| Fine-tuning method | QLoRA (4-bit base, LoRA r=16, α=32) — **merged into base weights for this release** |
| Trainable parameters at training time | ~13.0M (LoRA adapter only) |
| Training data | BanglaParaphrase, 100,000-pair subset |
| Max sequence length | 160 tokens |
| Effective batch size | 32 |
| Trained on | Google Colab (free-tier T4 GPU) |
| License | CC-BY-4.0 (matches base model — attribution required) |

*Trained on a single free-tier Colab T4 GPU; exact carbon footprint not tracked, but compute was intentionally minimized to demonstrate low-resource feasibility for a low-resource-language task.*

## Intended Use

Generating Bengali paraphrases of an input sentence — e.g., data augmentation for downstream Bengali NLP tasks, or research on low-resource paraphrase generation and parameter-efficient fine-tuning. Evaluated only on the BanglaParaphrase test distribution; not evaluated on other domains, dialects, or languages.

## Out-of-Scope Use

- Not intended for languages other than Bengali, or for code-mixed/transliterated text.
- Not intended for high-stakes or unreviewed automated use — this study's own LLM-judge evaluation found hallucination and meaning-reversal cases (see Limitations), so outputs should be reviewed before use in any context where semantic accuracy matters.
- Not a general-purpose Bengali instruction-following or chat model — although built on an instruction-tuned base, this checkpoint is fine-tuned specifically for sentence-level paraphrasing and has not been evaluated for other tasks.

## How to Use

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "AvinabhDutta-Dev/bangla-paraphrase-tigerllm-qlora"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

text = "এই বাড়িতে সাধারণত কোনো ঝগড়াঝাঁটি হয় না।"
messages = [{"role": "user", "content": f"Paraphrase this Bengali sentence: {text}"}]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
output_ids = model.generate(inputs, max_new_tokens=160, do_sample=False)
print(tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True))
```

## Sample Outputs

Real outputs from this model on the held-out test set, judged 5/5 for both meaning preservation and fluency by the study's LLM-judge evaluation:

| Source | Generated |
|---|---|
| ইউনিভার্সিটির ল্যাবে কাজ করতেন। | তিনি বিশ্ববিদ্যালয়ের ল্যাবে কাজ করতেন। |
| ইউটিউব দেখে আমি প্রথম এই ব্যাগ তৈরি শিখি। | আমি ইউটিউব দেখে প্রথম ব্যাগটা তৈরি করি। |

## Evaluation Results

Evaluated on the full, held-out BanglaParaphrase test set (23,332 examples), using the same pipeline and test data across all four models in this study.

| Metric | Score |
|---|---|
| BLEU | 18.69 |
| ROUGE-L | 0.466 |
| BERTScore (F1, BanglaBERT) | 0.942 |
| PINC (lexical novelty vs. source) | 0.777 |

Notably, TigerLLM matched or exceeded the full-fine-tune models on most metrics while updating only **~13M parameters (~5% of the model's total 664M parameters)** during training — a strong result for parameter-efficient fine-tuning on this task.

### LLM-as-a-Judge Validation

A 400-pair, four-model symmetric subset (100 examples per model, identical sources) was independently scored by Gemini 3.5 Flash-Lite on semantic meaning preservation and fluency (1–5 scale), with a binary meaning-reversal flag.

| Metric | Score |
|---|---|
| Mean judge meaning-preservation score | 4.47 / 5 |
| Mean judge fluency score | 4.77 / 5 |

**Error breakdown (out of 100 judged examples):**

| Category | Count |
|---|---|
| Valid paraphrase | 91 |
| Hallucination / semantic drift | 6 |
| Meaning reversal | 3 |
| Severe disfluency | 0 |

## Related Models (this study)

- [BanglaT5 (full fine-tune)](https://huggingface.co/AvinabhDutta-Dev/bangla-paraphrase-banglat5)
- [IndicBARTSS (full fine-tune)](https://huggingface.co/AvinabhDutta-Dev/bangla-paraphrase-indicbartss)
- [Qwen2.5-1.5B (QLoRA)](https://huggingface.co/AvinabhDutta-Dev/bangla-paraphrase-qwen2.5-qlora)

## Limitations

- Trained on a 100K-example subset (not the full ~420K available training pairs) and evaluated with greedy decoding, for compute tractability.
- Training ran across multiple resumed Colab sessions due to free-tier GPU quota limits; total GPU-compute time is not precisely reconstructable from training logs (see the parent study's methodology notes).
- BLEU/ROUGE-L are known to correlate only weakly with actual paraphrase quality (see the parent study's Notebook 07); BERTScore and the LLM-judge results are more informative for assessing this model.

- **Reproducibility:** Trained on a fixed 100,000-pair subset of BanglaParaphrase with a documented train/val/test split (see `processed_data/metadata.json` in the [GitHub repo](https://github.com/AvinabhDutta-Dev/bangla-paraphrase-benchmark)); decoding was fully deterministic (greedy, `do_sample=False`), so generation outputs are reproducible given the same checkpoint and inputs.

## Citation

If you use this model, please cite both the original TigerLLM/BanglaParaphrase work and this study:

```bibtex
@inproceedings{raihan-zampieri-2025-tigerllm,
  title = "{T}iger{LLM} - A Family of {B}angla Large Language Models",
  author = "Raihan, Nishat and Zampieri, Marcos",
  booktitle = "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)",
  year = "2025",
  publisher = "Association for Computational Linguistics",
  url = "https://aclanthology.org/2025.acl-short.69/"
}

@misc{banglaparaphrase2022,
  title={BanglaParaphrase: A High-Quality Bengali Paraphrase Dataset},
  author={Akil, Ajwad and others},
  year={2022}
}
```

See the [project GitHub repository](https://github.com/AvinabhDutta-Dev/bangla-paraphrase-benchmark) for the full paper, code, and citation for this study.

## Framework Versions

- Transformers 5.13.1
- PEFT 0.19.1 (used during training; adapter merged into base weights for this release)

---
license: cc-by-4.0
---
