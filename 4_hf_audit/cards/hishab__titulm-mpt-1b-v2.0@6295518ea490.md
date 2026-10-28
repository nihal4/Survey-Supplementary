---
datasets:
- togethercomputer/RedPajama-Data-V2
- uonlp/CulturaX
- wikipedia
language:
- en
- bn
license: apache-2.0
pipeline_tag: text-generation
library_name: transformers
---

# TituLM-1B-ENBN-V1 
TituLM-1B-ENBN-V1 is a large language model specifically trained for generating and understanding English and Bangla text. Utilizing a decoder-style transformer architecture, this model has been extensively trained on a dataset comprising __43.19__ billion Bangla, English and codes tokens. This model is the part of iterative train and release Bilingual LLM from Hishab.

The training process was managed using the robust framework provided by MosaicML's [llm-foundry](https://github.com/mosaicml/llm-foundry) repository. Throughout the training phase, titulm-1b-bn-v1 underwent a total of 59 iterations, allowing for iterative refinements and optimization.
Notable training configs:

- n_nead: 16
- n_layers: 24
- max_sequence_length: 2048
- vocab_size: 72000
- attn_impl: flash
- Trained on 8 H100 GPU on GCP


## Datasets
Datasets comprise Bangla, English, and Codes data. We mixed Bangla data with English Redpajama (C4, Github, StackExchange, Book, Arxiv, Wikipedia) data.

Token-wise distribution will be added soon below.

| Data chunk     | Language | Token count(Billion) |
|----------------|----------|-------------|
| Redpajama Arxiv        | English  | 2.12 |
| Redpajama Book        | English   | 2.02     |
| Redpajama Wikipedia       | English  | 2.03        |
| Redpajama Github Code | English | 2.24 |
| Redpajama StackExchange | English | 1.47 |
| Redpajama Common crawl | English | 12.74 |
| Redpajama C4 | English | 6.57 |
| Bangla (culturax, books, news, Wikipedia, Banglapedia) | Bangla | ~14 |
| Total | | 43.19|

## How to Use
The basic use cases to generate text using this model are simple. Follow the below code to generate text using this model.

Install the following library before running the code:

```sh
pip install transformers
pip install einops
pip install accelerate
```

```py
import transformers
from transformers import pipeline

model_name = 'hishab/titulm-1b-enbn-v1'

config = transformers.AutoConfig.from_pretrained(model_name, trust_remote_code=True)
config.max_seq_len = 2048

model = transformers.AutoModelForCausalLM.from_pretrained(
  model_name,
  config=config,
  trust_remote_code=True
)

tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)

pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, device='cuda:0')
# for Bangla
bn_output = pipe('আমি বাংলায় গান',
            max_new_tokens=100,
            do_sample=True,
            use_cache=True)

print(bn_output)
# for English
en_output = pipe('Bangla language plays',
            max_new_tokens=100,
            do_sample=True,
            use_cache=True)

print(en_output)
```

## Citation
```bash
@misc{hishab_2024_titulm_1b_enbn_v1,
  author = {Hishab Technologies Ltd.},
  title = {TituLM-1B-ENBN-V1},
  year = {2024},
  publisher = {HuggingFace Models},
  howpublished = {https://huggingface.co/hishab/titulm-1b-enbn-v1},
}
```

Code: https://github.com/hishab-nlp/titulm