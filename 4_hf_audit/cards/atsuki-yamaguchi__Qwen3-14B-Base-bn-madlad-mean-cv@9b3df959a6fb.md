
---
license: apache-2.0
datasets:
- allenai/MADLAD-400
language:
- bn
base_model:
- Qwen/Qwen3-14B-Base
- Qwen/Qwen3-14B
- atsuki-yamaguchi/Qwen3-14B-Base-bn-madlad-mean-tuned
library_name: transformers
---
# Qwen3 14B Base for Bengali: Chat Vector

This model is built on top of Qwen3 14B Base adapted for Bengali using 500M target language tokens sampled from MADLAD-400. It has an additional target vocabulary of 10K. Chat vector was added to the model after continual pre-training.

## Model Details

* **Vocabulary**: This model has an additional target vocabulary of 10K.
* **Target vocabulary initialization**: The target weights of the embedding and LM head were initialized using mean initialization.
* **Training**: This model was continually pre-trained on 500M target language tokens sampled from MADLAD-400.
* **Post-processing**: The model was post-processed using the Chat Vector method.


## Model Description

- **Language:** Bengali
- **License:** Apache 2.0
- **Fine-tuned from model:** Qwen/Qwen3-14B-Base


## Model Sources

- **Repository:** https://github.com/gucci-j/chat-cve
- **Paper:** https://arxiv.org/abs/2412.11704


## How to Get Started with the Model
Use the code below to get started with the model.
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "atsuki-yamaguchi/Qwen3-14B-Base-bn-madlad-mean-cv"
)
tokenizer = AutoTokenizer.from_pretrained(
    "atsuki-yamaguchi/Qwen3-14B-Base-bn-madlad-mean-cv"
)
```


## Citation
```
@article{yamaguchi2025adapting,
      title={Adapting Chat Language Models Using Only Target Unlabeled Language Data}, 
      author={Atsuki Yamaguchi and Terufumi Morishita and Aline Villavicencio and Nikolaos Aletras},
      journal={Transactions on Machine Learning Research},
      issn={2835-8856},
      year={2025},
      url={https://openreview.net/forum?id=6IdoIKowfe},
      note={}
}
```


