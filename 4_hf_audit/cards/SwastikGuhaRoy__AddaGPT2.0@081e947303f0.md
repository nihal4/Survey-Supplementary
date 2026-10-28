---
library_name: transformers
license: apache-2.0
datasets:
- ai4bharat/naamapadam
language:
- bn
base_model:
- openai-community/gpt2
---

# Model Card for Model ID

AddaGPT 2.0 is a Bengali language model based on GPT-2, fine-tuned using LoRA adapters for academic and low-resource applications. While GPT-2 was originally trained only on English data, this model has been adapted to Bengali using the AI4Bharat NaamaPadam dataset — a corpus focused on Named Entity Recognition (NER).
This project is intended as a proof of concept to explore how small, pretrained models like GPT-2 can be extended to Indic languages using low-rank adaptation (LoRA) techniques, even under limited compute settings (e.g., free Kaggle GPUs). It lays the foundation for future work in adapting language models for low-bandwidth, regional, and offline-first use cases — to support local communities.

## Model Details
| **Attribute**                      | **Description**                                                                                                        |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Base Model**                     | GPT-2 (117M parameters)                                                                                                |
| **Fine-tuned Using**               | [LoRA (Low-Rank Adaptation)](https://arxiv.org/abs/2106.09685)                                                         |
| **Language**                       | Bengali (`bn`)                                                                                                         |
| **Training Dataset**               | [`ai4bharat/naamapadam`](https://huggingface.co/datasets/ai4bharat/naamapadam) – Bengali NER corpus (train split only) |
| **Sentences Seen During Training** | \~9.6 million Bengali sentences                                                                                        |
| **Training Platform**              | Kaggle (Free T4 GPUs)                                                                            |
| **Frameworks**                     | 🤗 Transformers + PEFT (Parameter-Efficient Fine-Tuning) + Safetensors                                                 |
| **Trainable Parameters**           | 294,912                                                                                                                |
| **Total Parameters**               | 124,734,720                                                                                                            |
| **Percentage Fine-Tuned**          | 0.2364%                                                                                                                |



### Model Description

- **Developed by:** Swastik Guha Roy
- **Funded by   :** Self Funded


### Uses

AddaGPT 2.0 is an academic proof-of-concept project designed to explore how low-resource, low-compute setups (like Kaggle T4 GPUs) can be used to adapt large language models like GPT-2 for Indic languages, specifically Bengali.

### Intended Use Cases:
Academic research on low-rank adaptation (LoRA) for regional languages

Language modeling experimentation in Bengali

Demonstration of fine-tuning techniques in resource-constrained environments

Baseline comparison for future Bengali language model development

Educational purposes for students and ML enthusiasts working on low-resource NLP

### Intended Users:

ML/NLP researchers exploring parameter-efficient tuning

Students building regional language models

Developers prototyping Bengali language tools (with limitations)

Community contributors interested in advancing open-source Bengali AI


## Limitations

This model is not capable of generating grammatically or syntactically correct Bengali sentences. Instead, it outputs individual Bengali words or word-like tokens that are often meaningful on their own — a direct result of training on a NER-style dataset rather than full natural language text.

->This version does not produce grammatically coherent Bengali sentences

->It's trained on a NER dataset, so it mostly outputs individual Bengali words

->It is not suitable for downstream tasks like summarization, translation, or question-answering — yet



### How to Get Started with the Model

# Load Nessecary Libraries
  ```python
     from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
  ```

# Load the model and tokenizer
```python
  model = AutoModelForCausalLM.from_pretrained("SwastikGuhaRoy/AddaGPT2.0")
  tokenizer = AutoTokenizer.from_pretrained("SwastikGuhaRoy/AddaGPT2.0_tokenizer")
```
# Initialize generation pipeline
  ```python
  text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
 ```
# Run inference
``` python
  prompt = "রবীন্দ্রনাথ ঠাকুর একজন"
  output = text_generator(
      prompt,
      max_new_tokens=30,
      temperature=0.7,
      top_p=0.95,
      do_sample=True
  )
  
  print(output[0]["generated_text"])
```

## Evaluation
### Results

The model was evaluated on the validation split of the ai4bharat/naamapadam dataset to measure how well it models Bengali text.

## Metric: Perplexity (Lower is Better)
| Model                   | Validation Perplexity |
| ----------------------- | --------------------- |
| **AddaGPT 2.0**         | **25.61**             |
| Vanilla GPT-2 (English) | 144.53                |


## AddaGPT 2.0 shows a significantly lower perplexity, indicating a better fit to Bengali text.

## GPT-2 struggles with Bengali due to the lack of Bengali data during pretraining.

## Summary
Despite lower perplexity, the model still generates mostly isolated Bengali words, not grammatically complete sentences (due to the nature of the training dataset — a NER corpus).


### Citation 
If you use this model, please cite:

```bibtex
 @misc{addagpt2.0,
  author = {Swastik Guha Roy},
  title = {AddaGPT 2.0: Bengali Finetuned GPT-2 with LoRA},
  year = 2025,
  howpublished = {\url{https://huggingface.co/SwastikGuhaRoy/AddaGPT2.0}},
 }
