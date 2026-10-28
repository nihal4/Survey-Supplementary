---
language: "bn"
tags:
  - text-generation
  - example-tag
  - bangpt2
  - banglalm
metrics:
  - perplexity
library_name: transformers
#base_model: banglagov/banGPT2-Base
---

# GPT2 base model for Bangla

The GPT-2 model, short for Generative Pre-trained Transformer 2, is a language model developed by OpenAI. It isbasedon the Transformer architecture, which has proven to be highly effective innatural language processing tasks. GPT-2 is a generative model, which can generate coherent and realistic text based on a given prompt.

At the core of GPT-2 is the transformer architecture, particularly the decoder portion. It is trained usinga standard language modeling objective. After pre-training themodel can be fine-tuned for different downstream tasks.

## Data Details

The model was trained on a 32 GB corpus of text data, which underwent extensive preprocessing to ensure quality and consistency. Below are the key statistics:

| Metric            | Value            |
|-------------------|------------------|
| **Total Words**   | ~1.996 billion   |
| **Unique Words**  | ~21.24 million   |
| **Total Sentences** | ~165.38 million |
| **Total Documents** | ~15.62 million |



## Model Details

This model is a GPT-2-based language model trained on a large corpus of Bangla text in a self-supervised manner. This means the model was pretrained on raw text data without any human-provided labels, leveraging an automated process to create inputs and targets from the text itself. Specifically, the model was trained to predict the next word in a sequence of text

During training, the input sequences consisted of continuous chunks of text, and the target sequences were the same text shifted one token (word or subword) to the right. The model employs an internal masking mechanism to ensure that predictions for a given token depend only on preceding tokens and not future ones.


## How to use

```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel

model_name = "banglagov/banGPT2-Base"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

prompt = "বাংলাদেশ একটি সুন্দর দেশ। এটি"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

output = model.generate(input_ids, max_length=512, temperature=0.7, top_k=50,  do_sample=True)
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
```


## Model Architecture and Training

This model is based on GPT-2 and was trained using the Hugging Face Transformers library. It features a vocabulary size of 50,000, with an embedding dimension of 768, 12 hidden layers, 12 attention heads, and a feed-forward layer size of 3,072. Weights were initialized with a standard deviation of 0.01, and dropout rates were set at 0.1 for attention, residual, and embedding layers.

The training process involved a per-device batch size of 92, gradient accumulation over 4 steps, and an initial learning rate of 0.00005, with 10% of training steps allocated for warmup. The AdamW optimizer was used with parameters Beta1 (0.9), Beta2 (0.98), an epsilon value of 1e-6, and a weight decay of 0.01. The model was trained for a total of 300,000 steps, leveraging mixed-precision training (fp16) for efficiency. Inputs were processed with a maximum sequence length of 256 tokens, a masking probability of 15%, and an average noise span length of 3 tokens.


## Results

#### Training and Evaluation Metrics

| Metric             | Value   | Description                                             |
|--------------------|---------|---------------------------------------------------------|
| **Training Loss**  | 0.3756  | Loss after training on the training dataset.            |
| **Evaluation Loss**| 0.3251  | Loss after evaluating on the evaluation dataset.        |
| **Perplexity**     | 1.3849  | Indicates how well the model predicts the next word.    |


#### Fine-tuned For Downstream Task

| Task            | Precision | Recall  | Macro F1 |
|-----------------|-----------|---------|----------|
| **NER**         | 0.8534    | 0.7473  | 0.7846   |
| **POS**         | 0.8732    | 0.8468  | 0.8496   |
