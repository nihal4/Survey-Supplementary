---
language: 
- bn
- en
tags:
- fill-mask
licenses:
- cc-by-nc-sa-4.0
---

# BanglishBERT

This repository contains the pretrained generator checkpoint of the model [**BanglishBERT**](). This is an [ELECTRA](https://openreview.net/pdf?id=r1xMH1BtvB) generator model pretrained with the Masked Language Modeling (MLM) objective on large amounts of Bengali and English corpora.


**Note**: This model was pretrained using a specific normalization pipeline available [here](https://github.com/csebuetnlp/normalizer).

## Using this model for MLM in `transformers` (tested on 4.11.0.dev0)

```python
from normalizer import normalize # pip install git+https://github.com/csebuetnlp/normalizer
from transformers import pipeline

fill_mask = pipeline(
    "fill-mask",
    model="csebuetnlp/banglishbert_generator",
    tokenizer="csebuetnlp/banglishbert_generator"
)

print(
    fill_mask(
        normalize(f"Paris is the {fill_mask.tokenizer.mask_token} of France.")
    )
)
```

If you use this model, please cite the following paper:

```
@inproceedings{bhattacharjee-etal-2022-banglabert,
    title     = {BanglaBERT: Lagnuage Model Pretraining and Benchmarks for Low-Resource Language Understanding Evaluation in Bangla},
    author = "Bhattacharjee, Abhik  and
      Hasan, Tahmid  and
      Mubasshir, Kazi  and
      Islam, Md. Saiful  and
      Uddin, Wasi Ahmad  and
      Iqbal, Anindya  and
      Rahman, M. Sohel  and
      Shahriyar, Rifat",
      booktitle = "Findings of the North American Chapter of the Association for Computational Linguistics: NAACL 2022",
      month = july,
    year      = {2022},
    url       = {https://arxiv.org/abs/2101.00204},
    eprinttype = {arXiv},
    eprint    = {2101.00204}
}
```

If you use the normalization module, please cite the following paper:
```
@inproceedings{hasan-etal-2020-low,
    title = "Not Low-Resource Anymore: Aligner Ensembling, Batch Filtering, and New Datasets for {B}engali-{E}nglish Machine Translation",
    author = "Hasan, Tahmid  and
      Bhattacharjee, Abhik  and
      Samin, Kazi  and
      Hasan, Masum  and
      Basak, Madhusudan  and
      Rahman, M. Sohel  and
      Shahriyar, Rifat",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.207",
    doi = "10.18653/v1/2020.emnlp-main.207",
    pages = "2612--2623",
    abstract = "Despite being the seventh most widely spoken language in the world, Bengali has received much less attention in machine translation literature due to being low in resources. Most publicly available parallel corpora for Bengali are not large enough; and have rather poor quality, mostly because of incorrect sentence alignments resulting from erroneous sentence segmentation, and also because of a high volume of noise present in them. In this work, we build a customized sentence segmenter for Bengali and propose two novel methods for parallel corpus creation on low-resource setups: aligner ensembling and batch filtering. With the segmenter and the two methods combined, we compile a high-quality Bengali-English parallel corpus comprising of 2.75 million sentence pairs, more than 2 million of which were not available before. Training on neural models, we achieve an improvement of more than 9 BLEU score over previous approaches to Bengali-English machine translation. We also evaluate on a new test set of 1000 pairs made with extensive quality control. We release the segmenter, parallel corpus, and the evaluation set, thus elevating Bengali from its low-resource status. To the best of our knowledge, this is the first ever large scale study on Bengali-English machine translation. We believe our study will pave the way for future research on Bengali-English machine translation as well as other low-resource languages. Our data and code are available at https://github.com/csebuetnlp/banglanmt.",
}
```


