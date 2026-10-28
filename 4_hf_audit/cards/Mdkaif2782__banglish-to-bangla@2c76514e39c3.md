---
datasets:
- SKNahin/bengali-transliteration-data
language:
- bn
- en
base_model:
- facebook/mbart-large-50
tags:
- banglish
- bangla
- translator
- avro
pipeline_tag: text2text-generation
---

# Hugging Face: Banglish to Bangla Translation

This repository demonstrates how to use a Hugging Face model to translate Banglish (Romanized Bangla) text into Bangla using the MBart50 tokenizer and model. The model, `Mdkaif2782/banglish-to-bangla`, is pre-trained and fine-tuned for this task.

## Setup in Google Colab
Follow these steps to use the model in Google Colab:

### 1. Install Dependencies
Make sure you have the `transformers` library installed. Run the following command in your Colab notebook:

```python
!pip install transformers torch
```

### 2. Load and Use the Model
Copy the code below into a cell in your Colab notebook to start translating Banglish to Bangla:

```python
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch

# Load the pre-trained model and tokenizer directly from Hugging Face
model_name = "Mdkaif2782/banglish-to-bangla"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

def translate_banglish_to_bangla(model, tokenizer, banglish_input):
    inputs = tokenizer(banglish_input, return_tensors="pt", padding=True, truncation=True, max_length=128)

    if torch.cuda.is_available():
        inputs = {key: value.cuda() for key, value in inputs.items()}
        model = model.cuda()

    translated_tokens = model.generate(**inputs, decoder_start_token_id=tokenizer.lang_code_to_id["bn_IN"])
    translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

    return translated_text

# Take custom input
print("Enter your Banglish text (type 'exit' to quit):")
while True:
    banglish_text = input("Banglish: ")
    if banglish_text.lower() == "exit":
        break

    # Translate Banglish to Bangla
    translated_text = translate_banglish_to_bangla(model, tokenizer, banglish_text)
    print(f"Translated Bangla: {translated_text}\n")
```

### 3. Run the Notebook
1. Paste the above code into a cell.
2. Run the cell.
3. Enter your Banglish text in the input prompt to get the translated Bangla text. Type `exit` to quit.

## Example Usage

Input:
```
Banglish: amar valo lagche onek
```

Output:
```
Translated Bangla: আমার ভালো লাগছে অনেক
```

## Notes
- Ensure your runtime in Google Colab supports GPU for faster processing. Go to `Runtime > Change runtime type` and select `GPU`.
- The model `Mdkaif2782/banglish-to-bangla` can be fine-tuned further if required.

## License
This project uses the Hugging Face `transformers` library. Refer to the [Hugging Face documentation](https://huggingface.co/docs/transformers/) for more details.