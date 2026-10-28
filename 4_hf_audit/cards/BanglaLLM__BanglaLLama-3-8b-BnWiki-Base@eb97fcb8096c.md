---
language:
- bn
- en
license: llama3
tags:
- bangla
- large language model
datasets:
- wikimedia/wikipedia
---

# Bangla LLaMA-3 8B Base v0.1 [pre-trained]

Welcome to the inaugural release of the Bangla LLaMA-3 8B base model – an important step in advancing LLMs for the Bangla language. This model is ready for immediate inference and is also primed for further fine-tuning to cater to your specific NLP tasks.

> **Please Note:** This model, labeled as a foundational Bangla Language Model (LLM), is designed primarily for Causal Language Modeling (LM) purposes. In other words, if you are looking for an instruction following model in Bangla, you may find [BanglaLLM/Bangla-llama-7b-instruct-v0.1](https://huggingface.co/BanglaLLM/Bangla-llama-7b-instruct-v0.1) more suitable for your needs.

## Model description

The Bangla LLaMA models have been enhanced and tailored specifically with an extensive Bangla vocabulary of 16,000 tokens, building upon the foundation set by the original LLaMA-2.

- **Model type:** A 8B parameter model for Causal LM pre-trained on [Wikimedia/Wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia) dataset's Bangla subset.
- **Language(s):** Bangla and English
- **License:** GNU General Public License v3.0
- **Source Model:** [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B)
- **Training Precision:** `float16`
- **Code:** [GitHub](https://github.com/brishtiteveja5/Bangla-llama)

## Related Models

| Model                     | Type                        | Data              | Base Model             | # Params | Download Links                                                         |
|---------------------------|-----------------------------|-------------------|------------------------|------|------------------------------------------------------------------------|
| Bangla LLaMA 8B Base      | Base model                  | 173K rows         | LLaMA-3 8B             | 8B   | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3-8b-BnWiki-Base/edit/main/README.md)     |
| Bangla LLaMA 7B Base      | Base model                  | 12GB              | LLaMA-2 7B             | 7B   | [HF Hub](https://huggingface.co/brishtiteveja/Bangla-llama-7b-base-v0.1)     |
| Bangla LLaMA 13B Base     | Base model                  | 4GB               | LLaMA-2 13B            | 13B  | [HF Hub](https://huggingface.co/brishtiteveja/Bangla-llama-13b-base-v0.1)    |
| Bangla LLaMA 7B Instruct  | Instruction following model | 145k instructions | Bangla LLaMA 7B Base   | 7B   | [HF Hub](https://huggingface.co/brishtiteveja/Bangla-llama-7b-instruct-v0.1) |
| Bangla LLaMA 13B Instruct | Instruction following model | 145k instructions | Bangla LLaMA 13B Base  | 13B  | [HF Hub](brishtiteveja/Bangla-llama-13b-instruct-v0.1)                       |

## Usage Note

It's important to note that the models have not undergone detoxification. Therefore, while they possess impressive linguistic capabilities, there is a possibility for them to generate content that could be deemed harmful or offensive. We urge users to exercise discretion and supervise the model's outputs closely, especially in public or sensitive applications.

## Meet the Developers

Get to know the creators behind this innovative model and follow their contributions to the field:

- [Abdullah Khan Zehady](https://www.linkedin.com/in/abdullah-khan-zehady-915ba024/)

## Citation

If you use this model or the Bangla-Llama dataset in your research, please cite:


We hope this model serves as a valuable tool in your NLP toolkit and look forward to seeing the advancements it will enable in the understanding and generation of the Bangla language.