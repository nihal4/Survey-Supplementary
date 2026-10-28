---
language:
  - bn
license: cc-by-4.0
library_name: transformers
pipeline_tag: fill-mask
tags:
  - bengali
  - bangla
  - bnlm-c
  - bangla-small-model
  - bengali-efficient-model
  - bnlm
  - bluge
  - bengali-nlp
  - bnlp
  - low-resource
  - masked-language-modeling
  - pretrained
  - language-model
  - distilbert
datasets:
  - nahid-hub/B-CORE-bengali-corpus
model-index:
  - name: BnLM-C
    results: []
---

# BnLM-C: Bangla Language Model (66M)

**BnLM-C** is a 66M-parameter Bangla-specific pretrained language model, one of three models in the **BnLM** suite (**B**e**n**gali **L**anguage **M**odel) introduced alongside the **BLUGE** benchmark and **B-CORE** pretraining corpus. BnLM-F is among the smallest Bangla language models available, while ranking among the most accurate and computationally efficient — delivering state-of-the-art results at a fraction of the size and compute of multilingual alternatives. BnLM models are pretrained from scratch on Bangla text using the Masked Language Modeling (MLM) objective, and are designed for efficient, low-resource NLP without relying on large multilingual models. BnLM-C is the most compact variant in the suite, built for deployment under tighter compute and latency constraints.

See the [BLUGE collection](https://huggingface.co/collections/nahid-hub/bluge) for the full release — evaluation tasks, pretraining corpus, tokenizers, and all three BnLM variants (BnLM-F, BnLM-M, BnLM-C).

## Model Details

| | |
|---|---|
| Parameters | 66M |
| Tokenizer | Custom Bangla WordPiece, 30.5K vocabulary |
| Objective | Masked Language Modeling (MLM) |
| Max sequence length | 512 tokens |
| Pretraining data | [B-CORE](https://huggingface.co/datasets/nahid-hub/B-CORE-bengali-corpus) — 4.32B tokens, 52GB |

Despite its compact size, BnLM-F achieves state-of-the-art results across BLUGE and four cross-lingual/Indic benchmarks, while requiring 44–91% fewer FLOPs and ~2x faster inference than competitive multilingual baselines. Full training configuration and hyperparameters are available in the paper.

## Usage

### Masked language modeling (works out of the box)

This is what the pretrained model does directly, with no additional training:

```python
from transformers import pipeline

fill = pipeline("fill-mask", model="nahid-hub/BnLM-F-135m")

# The mask token is read from the tokenizer, so this works regardless of
# how the special token is spelled in this model's custom vocabulary.
mask = fill.tokenizer.mask_token
print(fill(f"আমি বাংলায় গান {mask}।"))
```

### Loading the encoder (feature extraction or custom heads)

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("nahid-hub/BnLM-F-135m")
model = AutoModel.from_pretrained("nahid-hub/BnLM-F-135m")

inputs = tokenizer("খাবারটা অসাধারণ ছিল।", return_tensors="pt")
outputs = model(**inputs)          # last_hidden_state, etc.
```

To access the MLM head instead, use `AutoModelForMaskedLM.from_pretrained("nahid-hub/BnLM-F-135m")`.

### Fine-tuning for downstream tasks

To use BnLM-F for classification (e.g. sentiment on [BLUGE-TSC](https://huggingface.co/datasets/nahid-hub/BLUGE-bengali-sentiment-classification)), load it with a task head and train it:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("nahid-hub/BnLM-F-135m")
model = AutoModelForSequenceClassification.from_pretrained(
    "nahid-hub/BnLM-F-135m",
    num_labels=3,   # e.g. 0: neutral, 1: positive, 2: negative
)

# NOTE: The classification head above is RANDOMLY INITIALIZED. Its predictions
# are meaningless until you fine-tune the model on labeled data. Loading this
# checkpoint will report `classifier`/`pre_classifier` weights as "missing"
# (newly initialized) and the MLM-head weights as "unexpected" (discarded) —
# both are expected for a base model and are not errors.
#
# Fine-tune with the Trainer API or your own loop, then save/push the result:
#     model.save_pretrained("BnLM-F-135m-tsc")
#     model.push_to_hub("nahid-hub/BnLM-F-135m-tsc")   # requires a write token
#
# Only after fine-tuning should you run inference (logits -> argmax -> label).
```

See the [Hugging Face text-classification guide](https://huggingface.co/docs/transformers/tasks/sequence_classification) for a complete training example.

## Training Data

Pretrained exclusively on [**B-CORE**](https://huggingface.co/datasets/nahid-hub/B-CORE-bengali-corpus), a 16.5M-document, 4.32-billion-token Bangla corpus built via a reproducible multi-stage pipeline achieving a 22.4% reduction in corpus volume through quality filtering and cross-corpus deduplication.


## Related Models

- [BnLM-F](https://huggingface.co/nahid-hub/BnLM-F-135m) — 135M parameters, 120K-vocabulary tokenizer



## License

Released under **CC BY 4.0**.

## Citation

If you use this model, please cite:

```bibtex
@ARTICLE{BnLM-BLUGE-B-CORE,
  author={Hossain, Nahid and Faisal Kabir, Md.},
  journal={IEEE Access}, 
  title={Efficient Monolingual Pretraining in Low-Resource Settings Through Morphology-Aware Tokenization, Principled Corpus Denoising, and Benchmark-Driven Evaluation}, 
  year={2026},
  volume={14},
  number={},
  pages={91979-92003},
  keywords={Modeling;Multilingual;Training;Cleaning;Vocabulary;Labeling;Tokenization;Computational linguistics;Pipelines;Conferences;B-CORE;BLUGE;BnLM;corpus;evaluation benchmark;pretrained models},
  doi={10.1109/ACCESS.2026.3701520}
}
```