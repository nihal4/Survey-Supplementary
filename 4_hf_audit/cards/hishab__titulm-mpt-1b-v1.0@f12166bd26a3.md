---
language:
- bn
license: apache-2.0
datasets:
- uonlp/CulturaX
- wikipedia
pipeline_tag: text-generation
---

# TituLM-1B-BN-V1

TituLM-1B-BN-V1 is a large language model specifically trained for generating and understanding Bangla text. Utilizing a decoder-style transformer architecture, this model has been extensively trained on a dataset comprising 4.51 billion Bangla tokens. This model is the part of iterative train and release Bangla LLM from Hishab.

## Training
The training process was managed using the robust framework provided by MosaicML's [llm-foundry](https://github.com/mosaicml/llm-foundry) repository. Throughout the training phase, titulm-1b-bn-v1 underwent a total of 59 iterations, allowing for iterative refinements and optimization.
Notable training configs:

- n_nead: 16
- n_layers: 24
- max_sequence_length: 2048
- vocab_size: 72000
- attn_impl: flash
- Trained on 8 H100 GPU on GCP

__Training evaluation status__

- Evaluation CrossEntropy Loss

  Final loss: 3.11
  <img src="https://cdn-uploads.huggingface.co/production/uploads/5f40b34279c1ba4c353d0c7a/Mr0yAg9AfXTm15GATgSTN.png" alt="alt text" width="620" height="620">

- Language Perplexity

  Final Perplexity: 22.562
  <img src="https://cdn-uploads.huggingface.co/production/uploads/5f40b34279c1ba4c353d0c7a/B-ZC1LfFZdCTO25Twcyth.png" alt="alt text" width="620" height="620">

## Datasets
We add Bangla text datasets from several sources including

- Culturax
- Books
- Bangla Wikipedia
- Banglapedia
- News articles

Our total data size is 58 GB of deduplicated data with 4.51 billion tokens tokenized by our sentencepiece model.


## How to Use
The basic use cases to generate text using this model is simple. Follow the below code to generate text using this model.

Install the following library before running the code:

```sh
pip install transformers
pip install einops
pip install accelerate
```

```py
import transformers
from transformers import pipeline

model_name = 'hishab/titulm-1b-bn-v1'

config = transformers.AutoConfig.from_pretrained(model_name, trust_remote_code=True)
config.max_seq_len = 2048

model = transformers.AutoModelForCausalLM.from_pretrained(
  model_name,
  config=config,
  trust_remote_code=True
)

tokenizer = transformers.AutoTokenizer.from_pretrained('hishab/titulm-1b-bn-v1')

pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, device='cuda:0')
output = pipe('আমি বাংলায় গান',
            max_new_tokens=100,
            do_sample=True,
            use_cache=True)

print(output)
```


## Citation
```bash
@misc{hishab_2024_titulm_1b_bn_v1,
  author = {Hishab Technologies Ltd.},
  title = {TituLM-1B-BN-V1},
  year = {2024},
  publisher = {HuggingFace Models},
  howpublished = {https://huggingface.co/hishab/titulm-1b-bn-v1},
}
```