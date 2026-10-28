---
language:
- bn
library_name: transformers
pipeline_tag: text-generation
tags:
- hishab
- titulm
- pytorch
- llama
- llama-3
- llama-factory
license: llama3.2
base_model:
- meta-llama/Llama-3.2-3B
---

## Model Information

This model is a continually pre-trained version of the [meta-llama/Llama-3.2-3B](https://huggingface.co/meta-llama/Llama-3.2-3B) architecture, fine-tuned on extensive Bangla datasets. The primary goal of the continual pretraining was to enhance the model's ability to generate high-quality Bangla text. By extending the pretraining process specifically on Bangla data, the model has demonstrated superior performance in Bangla language understanding evaluation benchmarks and text generation tasks.

**Model Architecture:** Llama 3.2 is an auto-regressive language model with optimized transformer architecture. 

|  | Training Data | Params | Input modalities | Output modalities | Context Length | GQA | Shared Embeddings | Token count | Knowledge cutoff |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Llama 3.2 (text only)  | Hishab curated Bangla text corpus | 3B(3.21B) | Monolingual Text(Bangla) | Monolingual Text(Bangla)  | 4096 | Yes | Yes | 8.5B tokens | |

**Supported Languages:** Bengali (primary) and English (secondary)

**Llama 3.2 Model Family:** Token counts refer to pretraining data only. All model versions use Grouped-Query Attention (GQA) for improved inference scalability.

**Model Release Date:** October 24, 2024

**Status:** This is a static model trained on an offline dataset. Future versions may be released to improve model capabilities.

**License:** We are using a similar license to Llama 3.2. Use of Llama 3.2 is governed by the [Llama 3.2 Community License](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/LICENSE) (a custom, commercial license agreement).


## How to use
- Use with transformers

Starting with transformers >= 4.43.0 onward, you can run conversational inference using the Transformers pipeline abstraction or by leveraging the Auto classes with the generate() function.

Make sure to update your transformers installation via pip install --upgrade transformers.

```python
import torch
from transformers import pipeline

model_id = "hishab/titulm-llama-3.2-3b-v1.1"

pipe = pipeline(
    "text-generation", 
    model=model_id, 
    torch_dtype=torch.bfloat16, 
    device_map="auto"
)

pipe("আমাদের দেশের নাম")
```

## Hardware and Software

**Training Factors:** We used [llama-factory](https://github.com/hiyouga/LLaMA-Factory) training library, Cloud GPU cluster, and production infrastructure for pretraining. Fine-tuning, annotation, and evaluation were also performed on cloud infrastructure.


## Training Data

**Overview:** We have collected a large Bangla raw dataset of text data from a wide variety of sources. Our collected data so far includes a mix of web documents, books, translated text, transliterated text, transcribed text, code-mixed text, conversations, and open-source raw data. The dataset is cleaned and filtered by different filtering criteria to ensure the quality of the data. Our collected data size is roughly around 268 GB. The total trained tokens are 37B tokens.

Data sources summary:
- Web documents: Extracted, clean, and filtered common crawl data
- Books: Extracted, clean, filtered books data
- Transcribed text: Used in-house Bangla ASR model to transcribe Bangla audio data
- Translation data: We trained an English-Bangla translation LLM model and used it to translate English data to Bangla
- Code-mixed data: We trained an English-Bangla code-mixed LLM model and used it to generate code-mixed data
- Transliteration data: We trained a Bangla-English transliteration LLM model and used it to generate transliterated data
- Synthetic data: We generated synthetic data using a Bangla LLM model
- Others: We scrapped some selected website data, used open-source data, and used some other data sources


## Benchmarks

In this section, we report the results for __titulm-llama-3.2-3b-v1.1__ models on standard automatic benchmarks. For all these evaluations, we used [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) evaluations library. 

### Evaluation Datasets
We evaluated our pre-trained models on both Bangla and English benchmark datasets. Although the model is trained on Bangla data, its English capability is also evaluated on English benchmark datasets. The evaluation datasets are as follows:

#### Bangla Benchmark datasets
We evaluated the models on the following datasets:
- [Bangla MMLU](): A private multiple choice question dataset developed by Hishab curated from various sources.
- [CommonsenseQa Bangla](https://huggingface.co/datasets/hishab/commonsenseqa-bn): A Bangla translation of the CommonsenseQA dataset. The dataset was translated using a new method called Expressive Semantic Translation (EST), which combines Google Machine Translation with LLM-based rewriting modifications.
- [OpenbookQA Bangla](https://huggingface.co/datasets/hishab/openbookqa-bn): A Bangla translation of the OpenbookQA dataset. The dataset was translated using a new method called Expressive Semantic Translation (EST), which combines Google Machine Translation with LLM-based rewriting modifications.
- [Piqa Bangla](https://huggingface.co/datasets/hishab/piqa-bn): A Bangla translation of the Piqa dataset. The dataset was translated using a new method called Expressive Semantic Translation (EST), which combines Google Machine Translation with LLM-based rewriting modifications.
- [BoolQ Bangla](https://huggingface.co/datasets/hishab/boolq_bn): The dataset contains 15,942 examples, with each entry consisting of a triplet: (question, passage, answer). The questions are naturally occurring, generated from unprompted and unconstrained settings. Input passages were sourced from Bangla Wikipedia, Banglapedia, and News Articles, and GPT-4 was used to generate corresponding yes/no questions with answers.

#### English Benchmark datasets
- [MMLU](https://huggingface.co/datasets/cais/mmlu): This is a massive multitask test consisting of multiple-choice questions from various branches of knowledge. 
- [CommonseQa](https://huggingface.co/datasets/tau/commonsense_qa): CommonsenseQA is a new multiple-choice question-answering dataset that requires different types of commonsense knowledge to predict the correct answers.
- [OpenbookQA](https://huggingface.co/datasets/allenai/openbookqa): OpenBookQA aims to promote research in advanced question-answering, probing a deeper understanding of both the topic (with salient facts summarized as an open book, also provided with the dataset) and the language it is expressed in.
- [Piqa](https://huggingface.co/datasets/ybisk/piqa): The PIQA dataset focuses on physical commonsense reasoning, challenging AI to handle everyday situations requiring practical knowledge and unconventional solutions. Inspired by instructables.com, it aims to enhance AI's ability to understand and reason about physical interactions.
- [BoolQ](https://huggingface.co/datasets/google/boolq): BoolQ is a question answering dataset for yes/no questions containing 15942 examples. These questions are naturally occurring ---they are generated in unprompted and unconstrained settings. Each example is a triplet of (question, passage, answer), with the title of the page as optional additional context. The text-pair classification setup is similar to existing natural language inference tasks.

### Evaluation Results

#### Evaluation of Bangla Benchmark datasets
- **llama-3.2-3b** performs best on **Bangla MMLU** with a 0-shot score of **0.36** and 5-shot score of **0.38**.
- **hishab/titulm-llama-3.2-3b-v1.1** outperforms in most tasks, leading in **BoolQ BN**, **Commonsense QA BN**, **OpenBook QA BN**, and **PIQA BN** in both 0-shot and 5-shot settings, with the highest 5-shot scores.

| Model                                | Shots  | Bangla MMLU | BoolQ BN | Commonsense QA BN | OpenBook QA BN | PIQA BN |
|--------------------------------------|--------|-------------|----------|-------------------|----------------|---------|
| llama-3.2-3b                         | 0-shot | **0.36**    | 0.55     | 0.26              | 0.31           | 0.56    |
|                                      | 5-shot | 0.38        | -        | 0.29              | 0.32           | 0.58    |
| hishab/titulm-llama-3.2-3b-v1.1      | 0-shot | 0.35        | **0.66** | **0.31**          | **0.37**       | **0.62**|
|                                      | 5-shot | **0.40**    | -        | **0.40**          | **0.37**       | **0.63**|

#### Evaluation of English Benchmark datasets
- **llama-3.2-3b** dominates across all tasks, achieving the highest scores in **MMLU**, **BoolQ**, **Commonsense QA**, **OpenBook QA**, and **PIQA**, with improvements in the 5-shot setting.
- **titulm-llama-3.2-3b-v1.1** shows competitive performance but generally trails behind **llama-3.2-3b**, especially in the 0-shot setting across English benchmarks.

| Model                                | Shots  | MMLU         | BoolQ      | Commonsense QA     | OpenBook QA     | PIQA      |
|--------------------------------------|--------|--------------|------------|--------------------|-----------------|-----------|
| llama-3.2-3b                         | 0-shot | **0.54**    | **0.72**  | **0.64**          | **0.43**       | **0.77** |
|                                      | 5-shot | **0.56**    | **0.73**  | **0.67**          | **0.45**       | **0.80** |
| titulm-llama-3.2-3b-v1.1             | 0-shot | 0.43         | 0.65       | 0.56               | 0.39            | 0.77      |
|                                      | 5-shot | 0.51         | 0.72       | 0.61               | 0.43            | 0.78      |

### Instruction Tuned Models


### Intended Use
- Bangla text generation
- Bangla language understanding tasks
- Bangla instruction fine-tuning tasks