---
language:
- bn
- en
license: llama3.2
base_model:
- BanglaLLM/BanglaLLama-3.2-1b-unolp-culturax-base-v0.0.1
datasets:
- BanglaLLM/bangla-alpaca-orca
tags:
- bangla
- banglaLLM
- banglaNLP
- LLM
- LLama
- Transformer
- LLama 3.2
- bengali
- low_resource_language
pipeline_tag: text-generation
---

# Bangla LLaMA-3.2 1B Bangla-Alpaca-Orca Instruct v0.1 [finetune]

Welcome to the inaugural release of the Bangla LLaMA-3.2 1B bangla-alpaca-orca instruct model – an important step in advancing LLMs for the Bangla language. This model is ready for immediate inference.

> **Please Note:** This model, labeled as a foundational Bangla Language Model (LLM), is designed primarily for Causal Language Modeling (LM) purposes. 

## Model description

- **Model type:** A 1B parameter model for Causal LM instruct finetuned with BanglaLLM/bangla-alpaca-orca.
- **Language(s):** Bangla and English
- **License:** GNU General Public License v3.0
- **Source Model:** [BanglaLLM/BanglaLLama-3.2-1b-unolp-culturax-base-v0.0.1](https://huggingface.co/BanglaLLM/BanglaLLama-3.2-1b-unolp-culturax-base-v0.0.1)
- **Training Precision:** `float16`
- **Code:** [GitHub](https://github.com/abhinand5/bangla-llama)

## Related Models

| Model                    | Type                        | Data              | Base Model           | # Params | Download Links                                                         |
|--------------------------|-----------------------------|-------------------|----------------------|------|------------------------------------------------------------------------|
| Bangla LLaMA 7B Base      | Base model                  | 12GB              | LLaMA 7B             | 7B   | [HF Hub](https://huggingface.co/BanglaLLM/bangla-llama-7b-base-v0.1)     |
| Bangla LLaMA 13B Base     | Base model                  | 4GB               | LLaMA 13B            | 13B  | [HF Hub](https://huggingface.co/BanglaLLM/bangla-llama-13b-base-v0.1)    |
| Bangla LLaMA 7B Instruct  | Instruction following model | 145k instructions | Bangla LLaMA 7B Base  | 7B   | [HF Hub](https://huggingface.co/BanglaLLM/bangla-llama-7b-instruct-v0.1) |
| Bangla LLaMA 13B Instruct | Instruction following model | 145k instructions | Bangla LLaMA 13B Base | 13B  | [HF Hub](https://huggingface.co/BanglaLLM/bangla-llama-13b-instruct-v0.1)                       |
| Bangla LLaMA 3 8B Base | Base model | 12.4M | LLaMA 3 8b | 8B | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3-8b-unolp-culturax-base-v0.0.1)
| Bangla LLaMA 3 8B Instruct | Instruction following model | 172k instructions | Bangla LLaMA 3 8B Base | 8B | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3-8b-bangla-alpaca-orca-instruct-v0.0.1)
| Bangla LLaMA 3.1 8B Base | Base model	| 12.4M | LLaMA 3.1 8b | 8B | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3.1-8b-unolp-culturax-base-v0.0.1)
| Bangla LLaMA 3.1 8B Instruct | Instruction following model | 172k instructions | Bangla LLaMA 3.1 8B Base | 8b | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3.1-8b-bangla-alpaca-orca-instruct-v0.0.1)
| Bangla LLaMA 3.2 1B Base | Base model | 12.4M | LLaMA 3.2 1b | 1b | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3.2-1b-unolp-culturax-base-v0.0.1)
| Bangla LLaMA 3.2 3B Base | Base Model | 12.4 | LLaMA 3.2 3B | 1b | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3.2-1b-bangla-alpaca-orca-instruct-v0.0.1)
| Bangla LLaMA 3.2 3B Instruct| Instruction following model	| 172k instructions	| Bangla LLaMA 3.2 3B Base | 3B | [HF Hub](https://huggingface.co/BanglaLLM/BanglaLLama-3.2-3b-bangla-alpaca-orca-instruct-v0.0.1)
## Usage Note

It's important to note that the models have not undergone detoxification. Therefore, while they possess impressive linguistic capabilities, there is a possibility for them to generate content that could be deemed harmful or offensive. We urge users to exercise discretion and supervise the model's outputs closely, especially in public or sensitive applications.

## Meet the Developers

Get to know the creators behind this innovative model and follow their contributions to the field:

- [Abdullah Khan Zehady](https://www.linkedin.com/in/abdullah-khan-zehady-915ba024/)

## Citation


We hope this model serves as a valuable tool in your NLP toolkit and look forward to seeing the advancements it will enable in the understanding and generation of the Bangla language.