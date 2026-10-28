---
language: bn
tags:
- bert
- bengali
- bengali-lm
- bangla
license: mit
datasets:
- common_crawl
- wikipedia
- oscar
---


# Bangla BERT Base
A long way passed. Here is our **Bangla-Bert**! It is now available in huggingface model hub. 

[Bangla-Bert-Base](https://github.com/sagorbrur/bangla-bert) is a pretrained language model of Bengali language using mask language modeling described in [BERT](https://arxiv.org/abs/1810.04805) and it's github [repository](https://github.com/google-research/bert)



## Pretrain Corpus Details
Corpus was downloaded from two main sources:

* Bengali commoncrawl corpus downloaded from [OSCAR](https://oscar-corpus.com/)
* [Bengali Wikipedia Dump Dataset](https://dumps.wikimedia.org/bnwiki/latest/)

After downloading these corpora, we preprocessed it as a Bert format. which is one sentence per line and an extra newline for new documents. 

```
sentence 1
sentence 2

sentence 1
sentence 2

```

## Building Vocab
We used [BNLP](https://github.com/sagorbrur/bnlp) package for training bengali sentencepiece model with vocab size 102025. We preprocess the output vocab file as Bert format.
Our final vocab file availabe at [https://github.com/sagorbrur/bangla-bert](https://github.com/sagorbrur/bangla-bert) and also at [huggingface](https://huggingface.co/sagorsarker/bangla-bert-base) model hub.

## Training Details
* Bangla-Bert was trained with code provided in Google BERT's github repository (https://github.com/google-research/bert)
* Currently released model follows bert-base-uncased model architecture (12-layer, 768-hidden, 12-heads, 110M parameters)
* Total Training Steps: 1 Million
* The model was trained on a single Google Cloud GPU

## Evaluation Results

### LM Evaluation Results
After training 1 million steps here are the evaluation results. 

```
global_step = 1000000
loss = 2.2406516
masked_lm_accuracy = 0.60641736
masked_lm_loss = 2.201459
next_sentence_accuracy = 0.98625
next_sentence_loss = 0.040997364
perplexity = numpy.exp(2.2406516) = 9.393331287442784
Loss for final step: 2.426227

```

### Downstream Task Evaluation Results
- Evaluation on Bengali Classification Benchmark Datasets

Huge Thanks to [Nick Doiron](https://twitter.com/mapmeld) for providing evaluation results of the classification task.
He used [Bengali Classification Benchmark](https://github.com/rezacsedu/Classification_Benchmarks_Benglai_NLP) datasets for the classification task.
Comparing to Nick's [Bengali electra](https://huggingface.co/monsoon-nlp/bangla-electra) and multi-lingual BERT, Bangla BERT Base achieves a state of the art result.
Here is the [evaluation script](https://github.com/sagorbrur/bangla-bert/blob/master/notebook/bangla-bert-evaluation-classification-task.ipynb).


| Model | Sentiment Analysis | Hate Speech Task | News Topic Task | Average |
| ----- | -------------------| ---------------- | --------------- | ------- |
| mBERT | 68.15 | 52.32 | 72.27 | 64.25 |
| Bengali Electra | 69.19 | 44.84 | 82.33 | 65.45 |
| Bangla BERT Base | 70.37 | 71.83 | 89.19 | 77.13 |

- Evaluation on [Wikiann](https://huggingface.co/datasets/wikiann) Datasets

We evaluated `Bangla-BERT-Base` with [Wikiann](https://huggingface.co/datasets/wikiann) Bengali NER datasets along with another benchmark three models(mBERT, XLM-R, Indic-BERT). </br>
`Bangla-BERT-Base` got a third-place where `mBERT` got first and `XML-R` got second place after training these models 5 epochs.

| Base Pre-trained Model | F1 Score | Accuracy |
| ----- | -------------------| ---------------- |
| [mBERT-uncased](https://huggingface.co/bert-base-multilingual-uncased) | 97.11 | 97.68 |
| [XLM-R](https://huggingface.co/xlm-roberta-base) | 96.22 | 97.03 |
| [Indic-BERT](https://huggingface.co/ai4bharat/indic-bert)| 92.66 | 94.74 |
| Bangla-BERT-Base | 95.57 | 97.49 |

All four model trained with [transformers-token-classification](https://colab.research.google.com/github/huggingface/notebooks/blob/master/examples/token_classification.ipynb) notebook.
You can find all models evaluation results [here](https://github.com/sagorbrur/bangla-bert/tree/master/evaluations/wikiann)

Also, you can check the below paper list. They used this model on their datasets.
* [DeepHateExplainer: Explainable Hate Speech Detection in Under-resourced Bengali Language](https://arxiv.org/abs/2012.14353)
* [Emotion Classification in a Resource Constrained Language Using Transformer-based Approach](https://arxiv.org/abs/2104.08613)
* [A Review of Bangla Natural Language Processing Tasks and the Utility of Transformer Models](https://arxiv.org/abs/2107.03844)


**NB: If you use this model for any NLP task please share evaluation results with us. We will add it here.** 

## Limitations and Biases

## How to Use

**Bangla BERT Tokenizer**

```py
from transformers import AutoTokenizer, AutoModel

bnbert_tokenizer = AutoTokenizer.from_pretrained("sagorsarker/bangla-bert-base")
text = "আমি বাংলায় গান গাই।"
bnbert_tokenizer.tokenize(text)
# ['আমি', 'বাংলা', '##য', 'গান', 'গাই', '।']
```


**MASK Generation**

You can use this model directly with a pipeline for masked language modeling:

```py
from transformers import BertForMaskedLM, BertTokenizer, pipeline

model = BertForMaskedLM.from_pretrained("sagorsarker/bangla-bert-base")
tokenizer = BertTokenizer.from_pretrained("sagorsarker/bangla-bert-base")
nlp = pipeline('fill-mask', model=model, tokenizer=tokenizer)
for pred in nlp(f"আমি বাংলায় {nlp.tokenizer.mask_token} গাই।"):
  print(pred)

# {'sequence': '[CLS] আমি বাংলায গান গাই । [SEP]', 'score': 0.13404667377471924, 'token': 2552, 'token_str': 'গান'}

```

## Author
[Sagor Sarker](https://github.com/sagorbrur)


## Reference
* https://github.com/google-research/bert


## Citation
If you find this model helpful, please cite.

```
@misc{Sagor_2020,
  title   = {BanglaBERT: Bengali Mask Language Model for Bengali Language Understanding},
  author  = {Sagor Sarker},
  year    = {2020},
  url    = {https://github.com/sagorbrur/bangla-bert}
}

```





