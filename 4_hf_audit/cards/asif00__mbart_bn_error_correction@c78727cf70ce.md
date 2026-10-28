---
license: apache-2.0
language:
- bn
metrics:
- bleu
- cer
- wer
- meteor
library_name: transformers
pipeline_tag: text2text-generation
tags:
- text-generation-inference
---
# Bengali Sentence Error Correction

The goal here is to train a model that could fix grammatical and syntax errors in Bengali text. The approach was similar to how a language translator works, where the incorrect sentence is transformed into a correct one. We fine-tune a pertained model, namely [mBart50](https://huggingface.co/facebook/mbart-large-50) with a [dataset](https://github.com/hishab-nlp/BNSECData) of 1.3 M samples for 6500 steps and achieve a score of ```BLEU: 0.443, CER:0.159, WER:0.406, Meteor: 0.655``` when tested on unseen data. Clone/download this repo, run the `correction.py` script, and type the sentence after the prompt and you are all set.  Here is a live [Demo Space](https://huggingface.co/spaces/asif00/Bengali_Sentence_Error_Correction__mbart_bn_error_correction) of the finetune model in action. The full training process with the original training notebook can be found here: [GitHub](https://github.com/himisir/Bengali-Sentence-Error-Correction).

## Usage

Here is a simple way to use the fine-tuned model to correct Bengali sentences:
If you are trying to use it on a script, this is how can do It:

```python
from transformers import AutoModelForSeq2SeqLM, MBart50Tokenizer

checkpoint = "asif00/mbart_bn_error_correction"
tokenizer = MBart50Tokenizer.from_pretrained(checkpoint, src_lang="bn_IN", tgt_lang="bn_IN", use_fast=True)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,  use_safetensors =True)

incorrect_bengali_sentence = "আপনি কমন আছেন?"
inputs = tokenizer.encode(incorrect_bengali_sentence, truncation = True, return_tensors='pt', max_length=len(incorrect_bengali_sentence))
outputs = model.generate(inputs, max_new_tokens=len(incorrect_bengali_sentence), num_beams=5, early_stopping=True)
correct_bengali_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
# আপনি কেমন আছেন?
```

 
# Model Characteristics

We fine-tuned a [mBART Large 50](https://huggingface.co/facebook/mbart-large-50) with custom data. [mBART Large 50](https://huggingface.co/facebook/mbart-large-50) is a 600M parameter multilingual Sequence-to-Sequence model. It was introduced to show that multilingual translation models can be created through multilingual fine-tuning. Instead of fine-tuning in one direction, a pre-trained model is fine-tuned in many directions simultaneously. mBART-50 is created using the original mBART model and extended to add an extra 25 languages to support multilingual machine translation models of 50 languages. More about the base model can be found in [Official Documentation](https://huggingface.co/docs/transformers/model_doc/mbart)

# Data Overview

The [BNSECData](https://github.com/hishab-nlp/BNSECData) dataset contains over 1.3 million pairs of incorrect and correct Bengali sentences. Some data included repeated digits like '1', which were combined into a single number to help the model learn numbers better. To mimic common writing mistakes, new incorrect sentences with specific errors were added using a [custom script](https://github.com/himisir/Bengali-Sentence-Error-Correction/blob/main/simulate_error.py). These errors included mixing up sounds and changing diacritic marks, like mixing up `পরি` with `পড়ি` and `বিশ` with `বিষ`. Each mix-up changes the meaning of the words significantly. This helps make sure the dataset represents typical writing errors in Bengali.


# Evaluation Results

| Metric | Training | Post-Training Testing |
| ------ | -------- | --------------------- |
| BLEU   | 0.805    | 0.443                 |
| CER    | 0.053    | 0.159                 |
| WER    | 0.101    | 0.406                 |
| Meteor | 0.904    | 0.655                 |


## Usage limitations

The correct model struggles to correct shorter sentences or sentences with complex words.

## What's next?

The model is overfitting, and we can reduce that. My best guess is that we have a comparatively smaller validation set, which needed to be smaller to fit the model on a GPU, thus exacerbating the huge discrepancy between the two tests. We can train it on a more balanced distribution of datasets for further improvement. Another thing we can do is fine-tune the already fine-tuned model using a new dataset. I already have a script, [Scrapper](https://github.com/himisir/Scrape-Any-Sites), that I can use with the [Data Pipeline](simulate_error.py) that I just created for more diverse training data.

I'm also planning to run a 4-bit quantization on the same model to see how it performs against the base model. It should be a fun experiment.


## Cite

```bibtex
@misc {abdullah_al_asif_2024,
	author       = { {Abdullah Al Asif} },
	title        = { mbart_bn_error_correction (Revision 55cacd5) },
	year         = 2024,
	url          = { https://huggingface.co/asif00/mbart_bn_error_correction },
	doi          = { 10.57967/hf/2231 },
	publisher    = { Hugging Face }
}
```
## Resources and References:

[Dataset Source](https://github.com/hishab-nlp/BNSECData)
[Model Documentation and Troubleshooting](https://huggingface.co/docs/transformers/model_doc/mbart)
