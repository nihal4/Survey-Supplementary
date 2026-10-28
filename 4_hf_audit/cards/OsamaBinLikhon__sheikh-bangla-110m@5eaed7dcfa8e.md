---
language:
- bn
datasets:
- osamabinlikhon/bengali-text-dataset
widget:
- text: "বাংলা ভাষা হলো"
license: apache-2.0
tags:
- bengali
- gpt2
- language-model
- text-generation
- pytorch
---

# sheikh-bangla-110m

A Bengali GPT-2 language model trained from scratch with custom BPE tokenizer.

## Model Details

- **Model Type:** GPT-2 (Causal Language Model)
- **Language:** Bengali (বাংলা)
- **Training:** Trained from scratch (no pretrained weights)
- **Parameters:** 23,142,400 (110M approx)
- **Architecture:** 6 layers, 8 attention heads, 512 hidden size

## Tokenizer

- **Type:** BPE (Byte Pair Encoding)
- **Vocabulary Size:** 8,000 tokens
- **Special Tokens:**
  - `[PAD]` - Padding token (ID: 0)
  - `[UNK]` - Unknown token (ID: 1)
  - `[CLS]` - Beginning of sentence (ID: 2)
  - `[SEP]` - End of sentence (ID: 3)
  - `[MASK]` - Mask token (ID: 4)

## Usage

```python
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

# Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained("OsamaBinLikhon/sheikh-bangla-110m")
tokenizer = PreTrainedTokenizerFast.from_pretrained("OsamaBinLikhon/sheikh-bangla-110m")

# Generate text
input_text = "বাংলা ভাষা হলো"
inputs = tokenizer.encode(input_text, return_tensors="pt")
outputs = model.generate(inputs, max_length=100, do_sample=True, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training Details

- **Training Data:** Bengali text corpus
- **Epochs:** 20
- **Batch Size:** 4
- **Learning Rate:** 0.001
- **Max Length:** 256 tokens
- **Optimizer:** AdamW

## Performance

The model shows progressive loss reduction during training:
- Initial Loss: ~8.08
- Final Loss: ~6.69 (after 20 epochs)

## Limitations

- This is a small model trained on limited data
- May produce repetitive or nonsensical text for complex prompts
- Not suitable for production use without fine-tuning
- Training was done on CPU with limited computational resources

## Citation

```bibtex
@misc{sheikh-bangla-110m,
  author = {Osama Bin Likhon},
  title = {sheikh-bangla-110m: Bengali GPT-2 Model Trained from Scratch},
  url = {https://huggingface.co/OsamaBinLikhon/sheikh-bangla-110m},
}
```

## Acknowledgments

- Hugging Face for the Transformers library
- The tokenizers library for BPE implementation
