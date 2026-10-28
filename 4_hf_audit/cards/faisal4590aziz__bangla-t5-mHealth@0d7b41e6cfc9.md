---
datasets:
- faisal4590aziz/bangla-t5-health
language:
- bn
pipeline_tag: text-generation
tags:
- medical
- healthcare
- nlp
- paraphrasing
license: cc-by-4.0
metrics:
- bleu
- rouge
- meteor
base_model:
- csebuetnlp/banglat5_banglaparaphrase
---
# BanglaT5-mHealth

### Model Description

BanglaT5-mHealth is a Bengali paraphrasing model fine-tuned on the BanglaHealth dataset—an extensive collection of health-related Bengali sentences with high-quality paraphrase pairs. This model leverages the multilingual T5 (mT5) architecture as its foundation and adapts it to the low-resource, domain-specific context of Bengali healthcare content.

The model is designed to generate paraphrases that retain the semantic meaning of the original sentence while altering its lexical or syntactic form. It is suitable for downstream applications such as:

- Medical chatbot development

- Patient instruction simplification

- Automatic content rewriting for Bengali health education

- Dataset augmentation for Bengali NLP


- **Developed by:** [Faisal Ibn Aziz]
- **Funded by :** [Military Institute of Science & Technology(MIST)]
- **Model type:** [Text to Text transformer based architecture]
- **Language(s) (NLP):** [Bengali]
- **License:** [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)]
- **Finetuned from model :** [https://huggingface.co/csebuetnlp/banglat5_banglaparaphrase]

### Training Details

| Field       | Description                                 |
|-------------|---------------------------------------------|
| Base Model  | csebuetnlp/banglat5_banglaparaphrase        |
| Dataset     | [Link](https://huggingface.co/datasets/faisal4590aziz/bangla-health-related-paraphrased-dataset)   |
| Size        | 200,000 sentence pairs                      |
| Fine-Tuning Strategy      | Incremental domain-specific fine-tuning |
| Epochs      | 5 (per incremental subset) |
| Batch Size      | 12 |
| Learning Rate      | 3e-5 |
| Loss Function      | Cross-Entropy Loss |
| Decoding Strategy      | Beam Search (beam width = 5) |
| License     | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

### Model Sources
- **Repository:** [Link](https://huggingface.co/faisal4590aziz/bangla-t5-mHealth/)

## Using this model

```python
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the trained model
model_name = 'faisal4590aziz/bangla-t5-mHealth'
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Function to generate paraphrase
def generate_paraphrase(model, tokenizer, sentence, max_length=128):
    input_ids = tokenizer.encode(sentence, return_tensors='pt')
    outputs = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    paraphrase = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return paraphrase

# Load the test dataset
from datasets import load_dataset
dataset = load_dataset("faisal4590aziz/bangla-health-related-paraphrased-dataset")

for idx, row in dataset.iterrows():
  paraphrase = generate_paraphrase(model, tokenizer, row['source_sentence'])

```

## 📰 Related Publication

The dataset that was used to train this model is published in **Data in Brief (Elsevier)**:
> **BanglaHealth: A Bengali paraphrase Dataset on Health Domain**  
> [Faisal Ibn Aziz, Dr. Mohammad Nazrul Islam, 2025](https://doi.org/10.1016/j.dib.2025.111699)


### Training Data

[Dataset Link](https://huggingface.co/datasets/faisal4590aziz/bangla-health-related-paraphrased-dataset)

### Training Procedure

>>
**Incremental Training Approach**

Since training on a large dataset would require a lot of computing power, an ”Incremental Training Approach” was introducted to develop our custom
model. Instead of using the entire dataset at once,
we divided it into smaller parts. This allowed the model to
gradually learn and improve without putting too much strain
on the system. This process of adopting incremental training
approach on our proposed model is described in below:
For this, firstly, the complete dataset, comprising 200,000
Bengali sentences, was divided into smaller, manageable
batches. Each batch contained a subset of the data, typically
20,000 sentences.
Secondly, the initial batch was used to train the base model,
csebuetnlp/banglat5 banglaparaphrase. This first phase in-
volved standard training procedures, where the model learned
from the initial batch of 20,000 sentences.
Then, upon completion of the initial training, the model was
saved and then used as the starting point for the next training
iteration. The subsequent batch of 20,000 sentences was then
introduced for further training. This process ensured that
the model retained knowledge from previous batches while
continually integrating new information.
After that, this iterative process was repeated for each succes-
sive batch. Each iteration leveraged the model trained on all
previous batches, progressively refining and augmenting the
model’s capabilities with each new set of data.
Finally, after each batch training, the updated model was saved
and uploaded to the HuggingFace repository. This systematic
saving ensured that the model’s incremental progress was pre-
served and could be reused for further training or evaluation.
>>

## Benchmarking of Domain Specific Paraphrase Generation

Here, Base model: [csebuetnlp/banglat5_banglaparaphrase](https://huggingface.co/csebuetnlp/banglat5_banglaparaphrase)
and the proposed model is [our model](https://huggingface.co/faisal4590aziz/bangla-t5-mHealth/)

| Metric      | Base Model       | Proposed Model           |
|-------------|------------------|--------------------------|
| BLEU        | 0.1919           | 0.4213                   |
| ROUGE-1 (F1)| 0.5160           | 0.6924                   |
| ROUGE-2 (F1)| 0.2761           | 0.4969                   |
| ROUGE-L (F1)| 0.4903           | 0.6924                   |
| METEOR      | 0.5160           | 0.6924                   |

#### Metrics

[BLEU, ROUGUE, METEOR]

## Citation
If you are using this model/dataset, please cite the following papers in your research.

```
@INPROCEEDINGS{11381664,
  author={Aziz, Faisal Ibn and Islam, Muhammad Nazrul},
  booktitle={2025 IEEE 2nd International Conference on Computing, Applications and Systems (COMPAS)}, 
  title={Development And Enhancement Of Bengali Paraphrasing Model Using Domain Specific Knowledge}, 
  year={2025},
  volume={},
  number={},
  pages={1-7},
  keywords={Training;Vocabulary;Technological innovation;Computational modeling;Semantics;Medical services;Computer architecture;Linguistics;Transformers;Context modeling;Natural Language Processing (NLP);Paraphrasing;Bengali Paraphrasing;Bengali Language;Health Domain},
  doi={10.1109/COMPAS67506.2025.11381664}
}
```

```
@article{AZIZ2025111699,
  title = {BanglaHealth: A Bengali paraphrase Dataset on Health Domain},
  journal = {Data in Brief},
  pages = {111699},
  year = {2025},
  issn = {2352-3409},
  doi = {https://doi.org/10.1016/j.dib.2025.111699},
  url = {https://www.sciencedirect.com/science/article/pii/S2352340925004299},
  author = {Faisal Ibn Aziz and Muhammad Nazrul Islam},
  keywords = {Natural Language Processing (NLP), Paraphrasing, Bengali Paraphrasing, Bengali Language, Health Domain},
}
```

## Model Card Authors

[Faisal Ibn Aziz, Dr. Mohammad Nazrul Islam]

## Model Card Contact

[faisal4590ibnaziz@gmail.com, nazrul@cse.mist.ac.bd]