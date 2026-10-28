---
license: apache-2.0
language:
- bn
library_name: transformers
pipeline_tag: fill-mask
---
# BanglaClickBERT

<!-- Provide a longer summary of what this model is/does. -->
This repository contains **BanglaClickBERT** base, a more pretrained version of the model [BanglaBERT](https://huggingface.co/csebuetnlp/banglabert) base, specifically designed to address the challenge of clickbait detection in Bengali (Bangla) news headlines. This specialized language model leverages the Masked Language Model (MLM) approach to gain contextual understanding and enhance its ability to identify clickbait content.  The model&#39;s pretraining data, collected from clickbait-prone news websites, consists of 1 million unlabeled Bangla news headlines, ensuring adaptability across various contexts.

# Uses

```python
from transformers import AutoModelForPreTraining, AutoTokenizer
import torch

model = AutoModelForPreTraining.from_pretrained("samanjoy2/banglaclickbert_base")
tokenizer = AutoTokenizer.from_pretrained("samanjoy2/banglaclickbert_base")

original_sentence = "আমি কৃতজ্ঞ কারণ আপনি আমার জন্য অনেক কিছু করেছেন।"
fake_sentence = "আমি হতাশ কারণ আপনি আমার জন্য অনেক কিছু করেছেন।"

fake_tokens = tokenizer.tokenize(fake_sentence)
fake_inputs = tokenizer.encode(fake_sentence, return_tensors="pt")
discriminator_outputs = model(fake_inputs).logits
predictions = torch.round((torch.sign(discriminator_outputs) + 1) / 2)

[print("%7s" % token, end="") for token in fake_tokens]
print("\n" + "-" * 50)
[print("%7s" % int(prediction), end="") for prediction in predictions.squeeze().tolist()[1:-1]]
print("\n" + "-" * 50)
```
## Direct Use

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->
<!-- If the user enters content, print that. If not, but they enter a task in the list, use that. If neither, say "more info needed." -->

BanglaClickBERT can be directly used for clickbait detection in Bengali (Bangla) news headlines. Its primary intended use is to help identify and filter out clickbait content from news articles, websites, or other textual sources written in the Bengali language. This can be valuable for news organizations, social media platforms, or anyone interested in promoting accurate and trustworthy information.


# Bias, Risks, and Limitations

One of the primary challenges with models like BanglaClickBERT is data bias, as pretraining data collected from clickbait-prone sources can introduce biases. This may lead to the model being sensitive to certain types of clickbait while less accurate in detecting others. Additionally, contextual limitations exist, as it may not perform effectively outside Bengali and its cultural context. Users should be aware of false positives and negatives, and the model's inability to immediately identify evolving clickbait techniques. Furthermore, it offers limited context, primarily analyzing headlines and not considering the entire article, potentially missing clickbait embedded within the content. Continuous updates and monitoring are essential to address these challenges effectively.

# Training Details

## Training Data

We collected a diverse set of clickbait news headlines comprising 1 million samples from various online sources. These headlines were chosen to cover a wide range of clickbait headlines, ensuring the model's adaptability to different contexts like news on lifestyle, entertainment, business, viral videos etc.


## Training Procedure

Utilize the Transformer architecture for pretraining the model. Pretraining typically involves training the model as a Masked Language Model (MLM) on the unlabeled data. The MLM approach involves randomly masking words or tokens in the input and training the model to predict the missing tokens based on the context provided by the surrounding tokens. During pretraining, the model learns the linguistic patterns, context, and features of the Bangla language. The vast amount of unlabeled data is crucial for the model's general language understanding.


### Speeds, Sizes, Times

BanglaClickBERT is a BERT-based model with 12 layers. It utilizes the foundational architecture of BERT (Bidirectional Encoder Representations from Transformers) with 12 transformer encoder layers.


# Citation

If you use this model, please cite the following paper:

```
@inproceedings{joy-etal-2023-banglaclickbert,
    title = "{B}angla{C}lick{BERT}: {B}angla Clickbait Detection from News Headlines using Domain Adaptive {B}angla{BERT} and {MLP} Techniques",
    author = "Joy, Saman Sarker  and
      Aishi, Tanusree Das  and
      Nodi, Naima Tahsin  and
      Rasel, Annajiat Alim",
    editor = "Muresan, Smaranda  and
      Chen, Vivian  and
      Casey, Kennington  and
      David, Vandyke  and
      Nina, Dethlefs  and
      Koji, Inoue  and
      Erik, Ekstedt  and
      Stefan, Ultes",
    booktitle = "Proceedings of the 21st Annual Workshop of the Australasian Language Technology Association",
    month = nov,
    year = "2023",
    address = "Melbourne, Australia",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.alta-1.1",
    pages = "1--10",
    abstract = "News headlines or titles that deliberately persuade readers to view a particular online content are referred to as clickbait. There have been numerous studies focused on clickbait detection in English language, compared to that, there have been very few researches carried out that address clickbait detection in Bangla news headlines. In this study, we have experimented with several distinctive transformers models, namely BanglaBERT and XLM-RoBERTa. Additionally, we introduced a domain-adaptive pretrained model, BanglaClickBERT. We conducted a series of experiments to identify the most effective model. The dataset we used for this study contained 15,056 labeled and 65,406 unlabeled news headlines; in addition to that, we have collected more unlabeled Bangla news headlines by scraping clickbait-dense websites making a total of 1 million unlabeled news headlines in order to make our BanglaClickBERT. Our approach has successfully surpassed the performance of existing state-of-the-art technologies providing a more accurate and efficient solution for detecting clickbait in Bangla news headlines, with potential implications for improving online content quality and user experience.",
}
```