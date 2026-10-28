---

language: bn
license: mit
datasets:
- mc4

---

# Bengali GPT-2

Bengali GPT-2 demo. Part of the [Huggingface JAX/Flax event](https://discuss.huggingface.co/t/open-to-the-community-community-week-using-jax-flax-for-nlp-cv/). Also features a [finetuned](https://huggingface.co/khalidsaifullaah/bengali-lyricist-gpt2?) model on bengali song lyrics. 

# Model Description

OpenAI GPT-2 model was proposed in [Language Models are Unsupervised Multitask Learners](https://paperswithcode.com/paper/language-models-are-unsupervised-multitask) paper .Original GPT2 model was a causal (unidirectional) transformer pretrained using language modeling on a very large corpus of ~40 GB of text data. This model has same configuration but has been pretrained on bengali corpus of mC4(multilingual C4) dataset. The code for training the model has all been open-sourced [here](https://huggingface.co/flax-community/gpt2-bengali/tree/main).

# Training Details

Overall Result: 

```Eval loss : 1.45, Eval Perplexity : 3.141```

Data: [mC4-bn](https://huggingface.co/datasets/mc4)

Train Steps: 250k steps

link 🤗 flax-community/gpt2-bengali

Demo : https://huggingface.co/spaces/flax-community/Gpt2-bengali

# Usage 

For using the model there are multiple options available. For example using the pipeline directly we can try to generate sentences.

```
from transformers import pipeline

gpt2_bengali = pipeline('text-generation',model="flax-community/gpt2-bengali", tokenizer='flax-community/gpt2-bengali')
```

Similarly for using the finetuned model on bangla songs we can use following.

```
from transformers import pipeline

singer = pipeline('text-generation',model="khalidsaifullaah/bengali-lyricist-gpt2", tokenizer='khalidsaifullaah/bengali-lyricist-gpt2')
```

For using on other tasks the model needs to be fine-tuned on custom datasets. Details can be found in huggingface [documentation](https://huggingface.co/transformers/training.html)

# Contributors
* Khalid Saifullah
* Tasmiah Tahsin Mayeesha
* Ritobrata Ghosh
* Ibrahim Musa
* M Saiful Bari

### BibTeX entry and citation info

@misc {flax_community_2023,
author       = { {Flax Community} },
title        = { gpt2-bengali (Revision cb8fff6) },
year         = 2023,
url          = { https://huggingface.co/flax-community/gpt2-bengali },
doi          = { 10.57967/hf/0938 },
publisher    = { Hugging Face }
}