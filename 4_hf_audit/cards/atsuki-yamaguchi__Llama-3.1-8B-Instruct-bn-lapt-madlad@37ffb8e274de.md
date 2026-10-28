
---
license: llama3.1
datasets:
- allenai/MADLAD-400
language:
- bn
base_model:
- meta-llama/Llama-3.1-8B-Instruct
library_name: transformers
---
# Llama 3.1 8B Instruct for Bengali: Continual pre-training only

This model is built on top of Llama 3.1 8B Instruct adapted for Bengali using 500M target language tokens sampled from MADLAD-400.

## Model Details

* **Vocabulary**: This model has no additional target vocabulary. It retains the original vocabulary of Llama 3.1 8B Instruct.
* **Training**: This model was continually pre-trained on 500M target language tokens sampled from MADLAD-400.


## Model Description

- **Language:** Bengali
- **License:** Llama 3.1 Community License Agreement
- **Fine-tuned from model:** meta-llama/Llama-3.1-8B-Instruct


## Model Sources

- **Repository:** https://github.com/gucci-j/chat-cve
- **Paper:** https://arxiv.org/abs/2412.11704


## How to Get Started with the Model
Use the code below to get started with the model.
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "atsuki-yamaguchi/Llama-3.1-8B-Instruct-bn-lapt-madlad"
)
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct"
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


