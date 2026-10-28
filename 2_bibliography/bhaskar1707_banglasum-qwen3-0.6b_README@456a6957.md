---
language: bn
license: apache-2.0
base_model: Qwen/Qwen3-0.6B
tags:
- summarization
- bengali
- qlora
- peft
- lora
- xlsum
- trl
datasets:
- csebuetnlp/xlsum
---

# BanglaSum-Qwen3-0.6B — Bengali News Summarization

A LoRA adapter fine-tuned from [`Qwen/Qwen3-0.6B`](https://huggingface.co/Qwen/Qwen3-0.6B) for **abstractive Bengali news summarization**, trained on the full Bengali configuration of [XL-Sum v2.0](https://huggingface.co/datasets/csebuetnlp/xlsum).

Fine-tuning was performed with 4-bit QLoRA via [TRL](https://github.com/huggingface/trl) `SFTTrainer` + [PEFT](https://github.com/huggingface/peft), on a single NVIDIA Tesla T4 (16 GB) in Google Colab, resumed across multiple sessions via checkpointing.

- [Model Details](#model-details)
- [Dataset](#dataset)
- [Training Setup](#training-setup)
- [Evaluation — Before vs. After Fine-tuning](#evaluation--before-vs-after-fine-tuning)
  - [Qualitative Examples](#qualitative-examples)
- [Usage](#usage)
- [Limitations](#limitations)
- [Citation / Acknowledgements](#citation--acknowledgements)

## Model Details

- **Base model:** [`Qwen/Qwen3-0.6B`](https://huggingface.co/Qwen/Qwen3-0.6B)
- **Fine-tuning method:** QLoRA (4-bit NF4 + LoRA, r=16, alpha=32, all attention + MLP projections)
- **Trainable parameters:** 10,092,544 (2.62% of 385,941,504 total)
- **Framework:** TRL `SFTTrainer` + PEFT + bitsandbytes
- **Dataset:** [`csebuetnlp/xlsum`](https://huggingface.co/datasets/csebuetnlp/xlsum) — Bengali configuration, XL-Sum v2.0, full dataset
- **Task:** Bengali news article → abstractive summary
- **Hardware:** Google Colab, NVIDIA Tesla T4 (16 GB)

## Dataset

| Split      | Samples |
| ---------- | ------- |
| Train      | 8,102   |
| Validation | 1,012   |
| Test       | 1,012   |

![Split sizes](plots/split_sizes.png)

Qwen3's tokenizer inflates Bengali text substantially — a typical article can expand to several thousand tokens (see distribution below). To guarantee every training example keeps its full reference summary within the model's context window, articles are lead-truncated to 600 tokens before the prompt is built.

![Raw article token length distribution](plots/raw_token_length_distributions.png)
![Post-truncation token length distribution](plots/token_length_distributions.png)

## Training Setup

| Setting                  | Value                                        |
| ------------------------- | --------------------------------------------- |
| LoRA rank (r) / alpha       | 16 / 32                                       |
| Trainable parameters        | 10,092,544 (2.62%)                            |
| Learning rate                | 2e-4, cosine schedule                          |
| Effective batch size          | 16 (per-device batch × gradient accumulation) |
| Max sequence length            | 1,024 tokens                                  |
| Epochs                       | 3 (1,521 total optimizer steps)                |
| Optimizer                    | `paged_adamw_8bit`                             |
| Compute precision              | bfloat16                                      |
| Peak GPU memory                | 4.17 GB / 16 GB                               |
| Training                     | Resumed across multiple Colab sessions via checkpointing |

![Train vs. validation loss](plots/train_vs_validation_loss.png)
![Total training time](plots/total_training_time.png)

Full per-step logs: [`results/training_log_history.csv`](results/training_log_history.csv).

## Evaluation — Before vs. After Fine-tuning

Evaluated on a **fixed subset of 100 samples** from the held-out test split (never seen during training), using **deterministic (greedy) generation** for a fair before/after comparison. Exact sample IDs: [`results/eval_sample_ids.json`](results/eval_sample_ids.json).

| Metric   | Base Qwen3-0.6B | BanglaSum-Qwen3-0.6B | Improvement |
| -------- | ---------------- | ---------------------- | ----------- |
| ROUGE-1  | 0.0638            | 0.1230                  | +0.0592     |
| ROUGE-2  | 0.0177            | 0.0345                  | +0.0168     |
| ROUGE-L  | 0.0577            | 0.1108                  | +0.0531     |
| BLEU     | 1.2486            | 1.6751                  | +0.4265     |

![Before vs after metrics](plots/before_vs_after.png)

Full numeric results: [`results/final_metrics_export.json`](results/final_metrics_export.json), [`results/metric_comparison.csv`](results/metric_comparison.csv).

### Qualitative Examples

**✅ Success case** (`news-39127107`)
> **Article:** ভারতের অন্য অঞ্চলেও কোক, পেপসি নিষিদ্ধ করার দাবি জানাচ্ছেন কর্মীরা। স্থানীয় পণ্যের ব্যবহার নিশ্চিত করার জন্যই এই উদ্যোগ গ্রহণ করেছে ব্যবসায়ীরা...
> **Reference:** ভারতের দক্ষিণাঞ্চলীয় রাজ্য তামিলনাডুর ব্যবসায়ীরা সেখানে কোকা-কোলা ও পেপসি বিক্রি নিষিদ্ধ ঘোষণা করেছে।
> **Base model:** *(degenerates into a bulleted list echoing the article instead of summarizing)*
> **Fine-tuned:** ভারতের তামিলনাডু রাজ্যে কোকা-কোলা ও পেপসি নিষিদ্ধ করার দাবি জানাচ্ছেন কর্মীরা।

**❌ Failure case — hallucination** (`news-46679946`)
> **Article:** ইতালিতে অবৈধভাবে খৎনা করানো নিয়ে অনেকের উদ্বেগ রয়েছে। জানা গেছে, মৃত শিশুটির ভাইকেও একই সাথে খৎনা করানো হয়...
> **Reference:** ইতালিতে অভিবাসীদের এক কেন্দ্রে একটি দু'বছরের শিশুর খৎনা করানোর সময় অতিরিক্ত রক্তক্ষরণ শুরু হবার ফলে ছেলেটি মারা গেছে।
> **Fine-tuned:** ইতালির এক ব্যক্তি খৎনা করার জন্য নিজের সন্তানের ভাইকে গ্রেফতার করেছেন।
>
> *The fine-tuned model invents an arrest that isn't in the source article — a clear hallucination, not a paraphrase of the actual event (a child's death during circumcision).*

**❌ Failure case — repetition** (`news-45332030`)
> **Article:** কেবল কোটিপতি হলেই এসব খাবারের স্বাদ নেয়া যাবে তা নয়। কিন্তু আপনাকে অনেক টাকা জমাতে হবে!...
> **Reference:** জাফরানের নাম যদি শুনে থাকেন, এটাও নিশ্চয়ই জানেন যে এটি বিশ্বের সবচেয়ে দামী মশলার একটি...
> **Fine-tuned:** আপনি কোন খাবার জমাতে হবেন? কোন খাবার জমাতে হবেন? কোন খাবার জমাতে হবেন?
>
> *A clear degenerate-repetition failure — the model loops the same phrase instead of producing content, despite `repetition_penalty=1.1` at generation time.*

Full predictions (all 100 evaluated samples): [`results/final_predictions_export.csv`](results/final_predictions_export.csv).

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch

BASE_MODEL_ID = "Qwen/Qwen3-0.6B"
ADAPTER_ID = "bhaskar1707/banglasum-qwen3-0.6b"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16,
)

tokenizer = AutoTokenizer.from_pretrained(ADAPTER_ID)
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_ID, quantization_config=bnb_config, device_map="auto", torch_dtype=torch.bfloat16,
)
model = PeftModel.from_pretrained(base_model, ADAPTER_ID)
model.eval()

instruction = "নিচের বাংলা সংবাদটির একটি সংক্ষিপ্ত ও তথ্যসমৃদ্ধ সারাংশ তৈরি করুন।"
article = "..."  # your Bengali news article

messages = [{"role": "user", "content": f"{instruction}\n\nসংবাদ:\n{article}"}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.inference_mode():
    output_ids = model.generate(**inputs, max_new_tokens=96, do_sample=False, repetition_penalty=1.1)

summary = tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print(summary)
```

## Limitations

- Qwen3-0.6B has limited native Bengali pretraining coverage; hallucination and degenerate repetition (see failure cases above) are more common than with larger multilingual models.
- Articles are lead-truncated to 600 tokens before summarization — very long articles may lose information beyond that point.
- Evaluated on a fixed 100-sample subset drawn from the same XL-Sum distribution as training; out-of-distribution news sources/styles aren't separately benchmarked.
- Absolute ROUGE/BLEU scores are low in a domain-specific way — a 0.6B model on Bengali is not expected to match large-model summarization quality; the meaningful signal here is the consistent relative improvement over the base model.

## Citation / Acknowledgements

- Base model: [`Qwen/Qwen3-0.6B`](https://huggingface.co/Qwen/Qwen3-0.6B) (Qwen Team)
- Dataset: [`csebuetnlp/xlsum`](https://huggingface.co/datasets/csebuetnlp/xlsum) (Hasan et al., XL-Sum)
- Fine-tuning framework: [TRL](https://github.com/huggingface/trl) + [PEFT](https://github.com/huggingface/peft) + [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes)

Fine-tuned by **Bhaskar Pal**