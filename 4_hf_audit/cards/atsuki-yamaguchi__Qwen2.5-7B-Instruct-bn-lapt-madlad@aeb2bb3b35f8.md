
---
license: apache-2.0
datasets:
- allenai/MADLAD-400
language:
- bn
base_model:
- Qwen/Qwen2.5-7B-Instruct
library_name: transformers
---
# Qwen2.5 7B Instruct for Bengali: Continual pre-training only

This model is built on top of Qwen2.5 7B Instruct adapted for Bengali using 500M target language tokens sampled from MADLAD-400.

## Model Details

* **Vocabulary**: This model has no additional target vocabulary. It retains the original vocabulary of Qwen2.5 7B Instruct.
* **Training**: This model was continually pre-trained on 500M target language tokens sampled from MADLAD-400.


## Model Description

- **Language:** Bengali
- **License:** Apache 2.0
- **Fine-tuned from model:** Qwen/Qwen2.5-7B-Instruct


## Model Sources

- **Repository:** https://github.com/gucci-j/chat-cve
- **Paper:** https://arxiv.org/abs/2412.11704


## How to Get Started with the Model
Use the code below to get started with the model.
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "atsuki-yamaguchi/Qwen2.5-7B-Instruct-bn-lapt-madlad"
)
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen2.5-7B-Instruct"
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


