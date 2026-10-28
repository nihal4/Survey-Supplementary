---
license: apache-2.0
license_link: https://huggingface.co/sumitsen/BanglaGptAi1.0/blob/main/LICENSE
language:
- en
- bn
pipeline_tag: text-generation
base_model:
- sumitsen/BanglaGptAi1.0
tags:
- chat
library_name: transformers
---

# BanglaGptAi1.0

## Introduction

BanglaGptAi1.0 is the First release of BanglaGptAi . 

- Significantly **more knowledge** and has greatly improved capabilities in **coding** and **mathematics**, thanks to our specialized expert models in these domains.
- Significant improvements in **instruction following**, **generating long texts** (over 8K tokens), **understanding structured data** (e.g, tables), and **generating structured outputs** especially JSON. **More resilient to the diversity of system prompts**, enhancing role-play implementation and condition-setting for chatbots.
- **Long-context Support** up to 128K tokens and can generate up to 8K tokens.
- **Multilingual support** for over 29 languages, including Bengali, English, Chinese, French, Spanish, Portuguese, German, Italian, Russian, Japanese, Korean, Vietnamese, Thai, Arabic, and more. 

**This repo contains the instruction-tuned 0.5B Qwen2.5 model**, which has the following features:
- Type: Causal Language Models
- Training Stage: Pretraining & Post-training
- Architecture: transformers with RoPE, SwiGLU, RMSNorm, Attention QKV bias and tied word embeddings
- Number of Parameters: 0.49B
- Number of Paramaters (Non-Embedding): 0.36B
- Number of Layers: 24
- Number of Attention Heads (GQA): 14 for Q and 2 for KV
- Context Length: Full 32,768 tokens and generation 8192 tokens


## Requirements

The code of BanglaGptAi has been in the latest Hugging face `transformers` and we advise you to use the latest version of `transformers`.

With `transformers<4.37.0`, you will encounter the following error:
```
KeyError: 'qwen2'
```

## Quickstart

Here provides a code snippet with `apply_chat_template` to show you how to load the tokenizer and model and how to generate contents.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "sumitsen/BanglaGptAi1.0"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are BanglaGptAi, created by Sumit Sen. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
```


## Evaluation & Performance

Detailed evaluation results are reported in this [📑 blog](https://).

For requirements on GPU memory and the respective throughput, see results [here](https://).

## Citation

If you find our work helpful, feel free to give us a cite.

```
@misc{qwen2.5,
    title = {BanglaGptAi: A Party of Foundation Models},
    url = {https://},
    author = {Sumit Sen},
    month = {September},
    year = {2026}
}

@article{BanglaGptAi1.0,
      title={BanglaGptAi1.0 Technical Report}, 
      author={Sumit Sen and Crew},
      journal={Technical Report},
      year={2026}
}
```