---
license: apache-2.0
base_model: Qwen/Qwen2.5-1.5B-Instruct
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
  - name: bangla-paraphrase-qwen2.5-qlora
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
            value: 12.71
          - name: ROUGE-L
            type: rouge_l
            value: 0.377
          - name: BERTScore F1
            type: bertscore
            value: 0.923
          - name: PINC
            type: pinc
            value: 0.773
---

# bangla-paraphrase-qwen2.5-qlora

> **TL;DR:** A cautionary tale in this study — highest BLEU/ROUGE-L/BERTScore of all four models, but also the highest hallucination rate (22/100) under LLM-judge review. The clearest evidence in this project for why automated metrics alone are insufficient for evaluating paraphrase quality.

A [QLoRA](https://arxiv.org/abs/2305.14314) fine-tune of [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) for **Bengali paraphrase generation**, trained on the [BanglaParaphrase](https://huggingface.co/datasets/csebuetnlp/BanglaParaphrase) dataset. The LoRA adapter has been **merged into the base weights** — this is a complete, standalone model; no separate adapter loading is required.

This model is one of four architectures compared in a broader study, **"Beyond BLEU: Evaluating Automated Metric Reliability for Bengali Paraphrase Generation"** ([GitHub repo](https://github.com/AvinabhDutta-Dev/bangla-paraphrase-benchmark)), which benchmarks full fine-tuning vs. QLoRA and validates standard automated metrics (BLEU, ROUGE-L, BERTScore, PINC) against an LLM-as-a-judge. This model achieved the **highest BLEU/ROUGE-L/BERTScore among all four**, but also the **most hallucination errors** under LLM-judge review — see Limitations and Sample Outputs below.

## Model Details

| | |
|---|---|
| Base model | `Qwen/Qwen2.5-1.5B-Instruct` |
| Architecture | Causal decoder-only LM |
| Fine-tuning method | QLoRA (4-bit base, LoRA r=16, α=32) — **merged into base weights for this release** |
| Trainable parameters at training time | ~18.5M (LoRA adapter only) |
| Training data | BanglaParaphrase, 100,000-pair subset |
| Max sequence length | 512 tokens |
| Effective batch size | 16 |
| Early stopping | Stopped at step 2,700 (43% of planned 6,250 steps); validation loss re-confirmed on the full 5K validation set (0.411) |
| Trained on | Google Colab (free-tier T4 GPU) |
| License | Apache 2.0 (matches base model) |

*Trained on a single free-tier Colab T4 GPU with early stopping (43% of planned steps); despite the reduced training budget, this model achieved the highest surface-overlap metrics of the four — though not the most semantically reliable, see Evaluation Results.*

## Intended Use

Generating Bengali paraphrases of an input sentence — e.g., data augmentation for downstream Bengali NLP tasks, or research on low-resource paraphrase generation and parameter-efficient fine-tuning. Evaluated only on the BanglaParaphrase test distribution; not evaluated on other domains, dialects, or languages.

## Out-of-Scope Use

- Not intended for languages other than Bengali, or for code-mixed/transliterated text.
- **Not suitable for unreviewed automated use.** This model had the highest hallucination rate of all four models studied (22/100 judged examples) — see Sample Outputs for a real failure case. Do not deploy outputs from this model without human review in any context where factual or semantic accuracy matters.
- Not a general-purpose Bengali instruction-following or chat model — although built on an instruction-tuned base, this checkpoint is fine-tuned specifically for sentence-level paraphrasing and has not been evaluated for other tasks.

## How to Use

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "AvinabhDutta-Dev/bangla-paraphrase-qwen2.5-qlora"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

text = "এই বাড়িতে সাধারণত কোনো ঝগড়াঝাঁটি হয় না।"
messages = [{"role": "user", "content": f"Paraphrase this Bengali sentence: {text}"}]
inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
output_ids = model.generate(inputs, max_new_tokens=160, do_sample=False)
print(tokenizer.decode(output_ids[0][inputs.shape[-1]:], skip_special_tokens=True))
```

## Sample Outputs

Real outputs from this model on the held-out test set — one strong example and one genuine failure case, both from the study's LLM-judge evaluation, shown here deliberately for transparency rather than only showcasing favorable results:

**Good paraphrase (judge: meaning 5/5, fluency 5/5):**

| Source | Generated |
|---|---|
| কিন্তু আসলেই কি সবাই অভাগা? | কিন্তু সবাই কি অভাগা? |

**Hallucination failure case (judge: meaning 1/5, fluency 2/5):**

| Source | Generated |
|---|---|
| কিছু সরকারি কর্মকর্তা আছে যারা আমার কাছ থেকে প্রতিবছর গরু নিতো। | আমাদের প্রতিবছর গরু নিতে হবে কিছু সরকারি কর্মকর্তা। |

*Judge's assessment: "The generated text distorts the original meaning completely and has poor grammar."* The source describes officials taking cows from the speaker; the generated output garbles both the grammar and the direction of the action.

## Evaluation Results

Evaluated on the full, held-out BanglaParaphrase test set (23,332 examples), using the same pipeline and test data across all four models in this study.

| Metric | Score |
|---|---|
| BLEU | 12.71 |
| ROUGE-L | 0.377 |
| BERTScore (F1, BanglaBERT) | 0.923 |
| PINC (lexical novelty vs. source) | 0.773 |

For context: a 70B-class zero-shot LLM baseline reported on this same dataset in prior work scores in the 10–12 BLEU range — this fine-tuned 1.5B model performs comparably despite being over an order of magnitude smaller, using only ~18.5M trainable parameters (~1.2% of the model's total).

### LLM-as-a-Judge Validation

A 400-pair, four-model symmetric subset (100 examples per model, identical sources) was independently scored by Gemini 3.5 Flash-Lite on semantic meaning preservation and fluency (1–5 scale), with a binary meaning-reversal flag.

| Metric | Score |
|---|---|
| Mean judge meaning-preservation score | 3.72 / 5 |
| Mean judge fluency score | 3.84 / 5 |

**Error breakdown (out of 100 judged examples):**

| Category | Count |
|---|---|
| Valid paraphrase | 69 |
| Hallucination / semantic drift | 22 |
| Meaning reversal | 4 |
| Severe disfluency | 5 |

## Related Models (this study)

- [BanglaT5 (full fine-tune)](https://huggingface.co/AvinabhDutta-Dev/bangla-paraphrase-banglat5)
- [IndicBARTSS (full fine-tune)](https://huggingface.co/AvinabhDutta-Dev/bangla-paraphrase-indicbartss)
- [TigerLLM-1B (QLoRA)](https://huggingface.co/AvinabhDutta-Dev/bangla-paraphrase-tigerllm-qlora)

## Limitations

- **This model had the highest hallucination rate of all four models in the study (22/100 judged examples)**, despite scoring best on automated overlap metrics (BLEU, ROUGE-L, BERTScore). See Sample Outputs above for a real, representative failure case. This is a concrete illustration of why this study cross-validates automated metrics against LLM-judge scoring: strong surface-overlap metrics do not guarantee semantic reliability.
- Training-time validation loss was originally logged against a reduced 500-example subset for eval-frequency efficiency; a full-5K re-evaluation confirmed this was an accurate proxy (0.4113 vs. 0.4109).
- Trained on a 100K-example subset (not the full ~420K available training pairs) and evaluated with greedy decoding, for compute tractability.
- BLEU/ROUGE-L are known to correlate only weakly with actual paraphrase quality; this model is the clearest example of that gap in this study — high overlap scores, but the highest semantic-error rate under human-proxy review.

- **Reproducibility:** Trained on a fixed 100,000-pair subset of BanglaParaphrase with a documented train/val/test split (see `processed_data/metadata.json` in the [GitHub repo](https://github.com/AvinabhDutta-Dev/bangla-paraphrase-benchmark)); decoding was fully deterministic (greedy, `do_sample=False`), so generation outputs are reproducible given the same checkpoint and inputs.

## Citation

If you use this model, please cite both the original Qwen2.5/BanglaParaphrase work and this study:

```bibtex
@misc{qwen2.5,
  title = {Qwen2.5: A Party of Foundation Models},
  url = {https://qwenlm.github.io/blog/qwen2.5/},
  author = {Qwen Team},
  month = {September},
  year = {2024}
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
license: apache-2.0
---
