---
license: mit
language:
- bn
tags:
- Bangla-Key2Text
pipeline_tag: text2text-generation
datasets:
- tonmoytalukder/Bangla-Key2Text-2Million
widget:
- text: ঠিকমতো এই অভাবের তাই শিক্ষার্থীরা কারণে
- text: কেমন ডাটাসেট সময় ভাই বানাতে
---
This code imports the necessary libraries and loads <b>tonmoytalukder/Bangla-Key2Text</b> pre-trained model for sequence-to-sequence learning using the Hugging Face Transformers library. The model is designed to convert Bangla text from a key to a sentence.

<b>Using this model in transformers</b>
```python
!pip install sentencepiece
!pip install transformers
!pip install git+https://github.com/csebuetnlp/normalizer
!pip install torch

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from normalizer import normalize

model_dir = 'tonmoytalukder/Bangla-Key2Text'
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predict(key): # Function to generate text from given keywords
    input_ids = tokenizer.encode(key, return_tensors='pt',add_special_tokens=True).to(device)

    with torch.no_grad():
      outputs = model.generate(
          input_ids=input_ids,
          max_length =512,
          num_beams =2,
          early_stopping =True,
          num_return_sequences = 1,
          top_k= 50,
          top_p= 0.95,
          repetition_penalty= 2.5,
          length_penalty= 1.0)

    preds = [tokenizer.decode(g,skip_special_tokens=True,clean_up_tokenization_spaces=True) for g in outputs]

    generated_text = preds[0]
    return generated_text


keywords = "কেমন ডাটাসেট সময় ভাই বানাতে" # Put as কেমন ডাটাসেট সময় ভাই বানাতে in the Hosted inference API. Don't put any punctuation mark.
predict(normalize(keywords)) # "ভাই, ডাটাসেট বানাতে কেমন সময় লাগে?"
```

The code defines a function called predict() that takes a string of keywords as input and returns a generated sentence based on those keywords. The function uses the pre-trained model to generate the sentence.