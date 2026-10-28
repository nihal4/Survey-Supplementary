---
language:
- bn
tags:
- hishab
- titulm
- pytorch
- gemma
- gemma-2
license: gemma
library_name: transformers
pipeline_tag: text-generation
base_model:
- google/gemma-2-2b
---

## Model Information

This model is a continually pre-trained version of the [google/gemma-2-2b](https://huggingface.co/google/gemma-2-2b) architecture, fine-tuned on extensive Bangla datasets. The primary goal of the continual pretraining was to enhance the model's ability to generate high-quality Bangla text. By extending the pretraining process specifically on Bangla data, the model has demonstrated superior performance in Bangla language understanding evaluation benchmarks and text generation tasks.

**Model Architecture:** Gemma 2 is an auto-regressive language model that uses an optimized transformer architecture. 

|  | Training Data | Params | Input modalities | Output modalities | Context Length | Token count |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Gemma 2  | Hishab curated Bangla text corpus | 2B | Monolingual Text(Bangla) | Monolingual Text(Bangla)  | 4096 | 4.4B tokens | |

### How To Use

Below we share some code snippets on how to get quickly started with running the model. First, install the Transformers library with:
```sh
pip install -U transformers
```

Then, copy the snippet from the section that is relevant to your use case.

#### Running with the `pipeline` API

```python
import torch
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="titulm-gemma-2-2b-v1.1",
    device="cuda",  # replace with "mps" to run on a Mac device
)

text = "আমাদের দেশের নাম"
outputs = pipe(text, max_new_tokens=256)
response = outputs[0]["generated_text"]
print(response)
```


## Hardware and Software

**Training Factors:** We used the [llama-factory](https://github.com/hiyouga/LLaMA-Factory) training library, a cloud GPU cluster, and production infrastructure for pretraining. Fine-tuning, annotation, and evaluation were also performed on cloud infrastructure.


## Training Data

**Overview:** We have collected a large Bangla raw dataset of text data from a wide variety of sources. Our collected data so far includes a mix of web documents, books, translated text, transliterated text, transcribed text, code-mixed text, conversations, and open-source raw data. The dataset is cleaned and filtered by different filtering criteria to ensure the quality of the data. Our collected data size is roughly around 268 GB. We separated __33GB__ data from that using a ratio of the actual data size. Total trained tokens are __4.4B__ tokens.

Data sources summary:
- Web documents: Extracted, cleaned, and filtered common crawl data
- Books: Extracted, cleaned, filtered books data
- Transcribed text: Used in-house Bangla ASR model to transcribe Bangla audio data
- Translation data: We trained an English-Bangla translation LLM model and used it to translate English data to Bangla
- Code-mixed data: We trained an English-Bangla code-mixed LLM model and used it to generate code-mixed data
- Transliteration data: We trained a Bangla-English transliteration LLM model and used it to generate transliterated data
- Synthetic data: We generated synthetic data using a Bangla LLM model
- Others: We scrapped data from some selected websites, used open-source data, and used some other data sources


## Benchmarks

In this section, we report the results for __titulm-gemma-2-2b-v1.1__ models on standard automatic benchmarks. For all these evaluations, we used [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) evaluations library. 

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
- [BoolQ](https://huggingface.co/datasets/google/boolq): BoolQ is a question-answer dataset for yes/no questions containing 15942 examples. These questions are naturally occurring. They are generated in unprompted and unconstrained settings. Each example is a triplet of (question, passage, answer), with the title of the page as optional additional context. The text-pair classification setup is similar to existing natural language inference tasks.

### Evaluation Results

#### Evaluation of Bangla Benchmark datasets
- **gemma-2-2b** shows stronger performance in **Bangla MMLU** and **BoolQ BN** in the 0-shot setting.
- **titulm-gemma-2-2b-v1.1** performs better in **Commonsense QA BN**, **OpenBook QA BN**, and **PIQA BN** across both 0-shot and 5-shot settings.
- In the 5-shot setting, **titulm-gemma-2-2b-v1.1** leads in **BoolQ BN**, **Commonsense QA BN**, and **OpenBook QA BN**.
- **PIQA BN** scores are close, with **titulm-gemma-2-2b-v1.1** having a slight edge in the 0-shot setting.

| Model                    | Shots   | Bangla MMLU | BoolQ BN | Commonsense QA BN | OpenBook QA BN | PIQA BN |
|--------------------------|---------|-------------|----------|-------------------|----------------|---------|
| gemma-2-2b               | 0-shot  | **0.32**    | **0.63** | 0.26              | 0.34           | 0.56    |
|                          | 5-shot  | **0.35**    | 0.46     | 0.28              | 0.33           | **0.56**|
| titulm-gemma-2-2b-v1.1   | 0-shot  | 0.30        | 0.61     | **0.31**          | **0.35**       | **0.62**|
|                          | 5-shot  | 0.35        | **0.57** | **0.40**          | **0.38**       | 0.60    |

#### Evaluation of English Benchmark datasets
- **gemma-2-2b** consistently achieves the highest scores across all tasks in both 0-shot and 5-shot settings, leading in **MMLU**, **BoolQ**, **Commonsense QA**, **OpenBook QA**, and **PIQA**, with a maximum 5-shot score of **0.80** in **PIQA**.
- **titulm-gemma-2-2b-v1.1** performs well but trails behind **gemma-2-2b**, particularly in **Commonsense QA** and **OpenBook QA**, with the best scores being slightly lower across all tasks.
- It is expected as we have trained only on Bangla text.

| Model                                | Shots  | MMLU         | BoolQ      | Commonsense QA     | OpenBook QA     | PIQA      |
|--------------------------------------|--------|--------------|------------|--------------------|-----------------|-----------|
| gemma-2-2b                           | 0-shot | **0.50**     | **0.74**   | **0.52**           | **0.42**        | **0.79**  |
|                                      | 5-shot | **0.53**     | **0.78**   | **0.66**           | **0.42**        | **0.80**  |
| titulm-gemma-2-2b-v1.1               | 0-shot | 0.40         | 0.71       | 0.37               | 0.36            | 0.76      |
|                                      | 5-shot | 0.44         | 0.75       | 0.53               | 0.36            | 0.76      |

### Instruction Tuned Models


### Intended Use
- Bangla text generation
- Bangla language understanding tasks
- Bangla instruction fine-tuning tasks