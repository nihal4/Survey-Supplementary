---
language:
- bn
license: apache-2.0
library_name: transformers
tags:
- text-generation-inference
datasets:
- Polygl0t/gigakriya-v1
metrics:
- perplexity
pipeline_tag: text-generation
widget:
- text: "বাংলাদেশের রাজধানী হলো"
  example_title: উদাহরণ
- text: "বাংলাদেশের প্রধান নদী হলো"
  example_title: উদাহরণ
inference:
  parameters:
    repetition_penalty: 1.2
    temperature: 0.1
    top_k: 50
    top_p: 1.0
    max_new_tokens: 150
co2_eq_emissions:
  emissions: 146000
  source: CodeCarbon
  training_type: pre-training
  geographical_location: Germany
  hardware_used: NVIDIA A100-SXM4-80GB
model-index:
- name: LilTii-v0.1
  results:
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: Bangla MMLU
      type: hishab/bangla-mmlu
      split: test
      args:
        num_few_shot: 5
    metrics:
    - type: acc
      value: 23.95
      name: Acc
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: bangla_mmlu
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: BoolQ-BN
      type: hishab/boolq_bn
      split: train
      args:
        num_few_shot: 5
    metrics:
    - type: acc
      value: 52.08
      name: Acc
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: boolq_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: CommonsenseQA-BN
      type: hishab/commonsenseqa-bn
      split: train
      args:
        num_few_shot: 5
    metrics:
    - type: acc
      value: 30.22
      name: Acc
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: commonsenseqa_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: OpenBookQA-BN
      type: hishab/openbookqa-bn
      split: train
      args:
        num_few_shot: 5
    metrics:
    - type: acc
      value: 32.79
      name: Acc
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: openbookqa_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: PIQA-BN
      type: hishab/piqa-bn
      split: train
      args:
        num_few_shot: 5
    metrics:
    - type: acc
      value: 58.70
      name: Acc
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: piqa_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: ARC-Challenge
      type: arc_challenge_poly_bn
      args:
        num_few_shot: 5
    metrics:
    - type: acc_norm
      value: 23.52
      name: Acc-norm
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: arc_challenge_poly_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: HellaSwag
      type: hellaswag_poly_bn
      args:
        num_few_shot: 0
    metrics:
    - type: acc_norm
      value: 30.30
      name: Acc-norm
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: hellaswag_poly_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: MMLU
      type: mmlu_poly_bn
      args:
        num_few_shot: 5
    metrics:
    - type: acc_norm
      value: 26.40
      name: Acc-norm
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: mmlu_poly_bn
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      name: TruthfulQA
      type: truthfulqa_poly_bn
      args:
        num_few_shot: 0
    metrics:
    - type: mc1
      value: 24.07
      name: bleurt
    source:
      url: https://github.com/Polygl0t/lm-evaluation-harness/tree/polyglot_harness_bengali
      name: truthfulqa_poly_bn
---
# LilTii-v0.1

<img src="./logo.png" alt="A round logo of a cartoon tiger in a hoodie, cap, and gold chain with the text 'LilTii' below." height="200">

## Model Summary

**[LilTii-v0.1](https://huggingface.co/Polygl0t/LilTii-v0.1)** is a decoder-transformer natively pretrained in Bengali. LilTii is part of the [Polygl0t](https://huggingface.co/Polygl0t) initiative to advance language models for low-resource languages.

## Details

- **Architecture:** a Transformer-based model ([`llama`](https://huggingface.co/docs/transformers/main/en/model_doc/llama))
- **Size:** 670,127,616 parameters
- **Context length:** 4096 tokens
- **Dataset(s):** [Polygl0t/gigakriya-v1](https://huggingface.co/datasets/Polygl0t/gigakriya-v1)
- **Language:** Bengali
- **Batch size:** 2,097,152 tokens
- **Number of steps:** 48,219
- **GPU:** 8 NVIDIA A100-SXM4-80GB
- **Training time**: ~ 94 hours
- **Emissions:** 146 KgCO2 (Germany)
- **Total energy consumption:** 384 kWh

This repository has the [source code](https://github.com/Polygl0t/llm-foundry) used to train this model. The full configuration used for training is available in this [configuration file](training_config.yaml).

### Learning Rate

This model was trained with a cosine learning rate schedule with a linear warmup over the first 1,000 steps to a peak learning rate of 7e-4, followed by a cosine decay to 7e-5. The minimum learning rate was reached and held constant for the last 10% of training. Checkpoints were saved every 2,500 steps, which equates to approximately 5 billion tokens.

The `main` branch of this repository contains the final checkpoint saved at step 48,219. All other checkpoints are available as separate branches. To load a specific checkpoint, you can use the following code snippet:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "Polygl0t/LilTii-v0.1"
revision = "step-2500"  # Change this to the desired checkpoint branch
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, revision=revision)
```

Or, you can access all the revisions for the models via the following code snippet:

```python
from huggingface_hub import list_repo_refs
out = list_repo_refs("Polygl0t/LilTii-v0.1")
branches = [b.name for b in out.branches]
print(branches)
```

<details>
<summary><b>Learning Curves</b></summary>

![Learning Curves](./plots/learning_curves.png)

</details>

<details>
<summary><b>Gradient Norm (L2)</b></summary>

![gradient_statistics_v1](./plots/gradient_statistics_v1.png)

</details>

## Intended Uses

The primary intended use LilTii is to serve as foundations for research and development involving native Bengali language modeling. Checkpoints saved during training are designed to provide a controlled setting for performing comparative experiments, specifically regarding the effects of active pretraining on the performance of currently available benchmarks. You may also fine-tune and adapt LilTii for deployment if your use follows the Apache 2.0 license. If you decide to use LilTii as a basis for your fine-tuned model, please conduct your own risk and bias assessment.

## Out-of-scope Use

- LilTii is **not intended for deployment**. It is not an out-of-the-box product and should not be used for human-facing interactions.

- LilTii is for **the Bengali language only** and is unsuitable for text generation tasks in other languages.

- LilTii has **not been fine-tuned** for downstream tasks.

## Basic usage

```python
from transformers import GenerationConfig, TextGenerationPipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Specify the model and tokenizer
model_id = "Polygl0t/LilTii-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Specify the generation parameters as you like
generation_config = GenerationConfig(
    **{
    "do_sample": True,
    "max_new_tokens": 150,
    "renormalize_logits": True,
    "repetition_penalty": 1.2,
    "temperature": 0.1,
    "top_k": 50,
    "top_p": 1.0,
    "use_cache": True, 
  }
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
generator = TextGenerationPipeline(model=model, task="text-generation", tokenizer=tokenizer, device=device)

# Generate text
prompt = "বাংলাদেশের রাজধানী হলো"
completion = generator(prompt, generation_config=generation_config)
print(completion[0]['generated_text'])
```

## Limitations

Like almost all other language models trained on large text datasets scraped from the web, the LilTii shows behavior that does not make it an out-of-the-box solution to many real-world applications, especially those requiring factual, reliable, and nontoxic text generation. LilTii is subject to the following:

- **Hallucinations:** LilTii can produce content that can be mistaken as true facts, but are misleading or entirely false, i.e., hallucination.

- **Biases and Toxicity:** LilTii inherits the social and historical stereotypes from the data used to train it. Given these biases, the model can produce toxic content, i.e., harmful, offensive, or detrimental to individuals, groups, or communities.

- **Language Limitations:** LilTii is primarily designed to interact with Bengali. Other languages might challenge its comprehension, leading to potential misinterpretations or errors in response.

- **Repetition and Verbosity:** LilTii may get stuck on repetition loops (especially if the repetition penalty during generations is set to a meager value) or produce verbose responses unrelated to the prompt it was given.

Hence, even though LilTii is released with a permissive license, we urge users to perform their risk analysis on them if they intend to use them for real-world applications.

## Evaluations

The table below compares our two versions of LilTii against other base models of similar size. The NPM (Normalized Performance Metric) is a metric designed to provide a balanced view of model performance across various tasks, accounting for the inherent difficulty of each task. It normalizes the performance of each model on a given task by comparing it to a baseline performance, which represents a the performance of a random model.

|                 | NPM (mean) | ARC Challenge | HellaSwag | MMLU     | TruthfulQA MC1 | Bangla MMLU | BoolQ-BN | CommonsenseQA-BN | OpenBookQA-BN | PIQA-BN  |
|-----------------|------------|---------------|-----------|----------|----------------|-------------|----------|------------------|---------------|----------|
| LilTii-v0.2     | 9.63       | 26.18         | 32.20     | 27.06    | 25.48          | 26.09       | 60.65    | 32.43            | 32.19         | 60.50    |
| Qwen3-0.6B-Base | 8.07       | 22.84         | 28.70     | 29.79    | 27.14          | 32.57       | 65.74    | 23.01            | 30.58         | 52.72    |
| Qwen2.5-0.5B    | 6.04       | 22.93         | 28.42     | 28.31    | 28.17          | 30.84       | 57.87    | 22.11            | 30.58         | 53.59    |
| LilTii-v0.1     | 5.82       | 23.52         | 30.31     | 26.41    | 24.07          | 23.95       | 52.08    | 30.22            | 32.80         | 58.71    |

<details>
<summary><b>🏆 HellaSwag</b></summary>

![hellaswag](./plots/hellaswag.png)

</details>

<details>
<summary><b>🏆 PIQA-BN</b></summary>

![piqa-bn](./plots/piqa-bn.png)

</details>

<details>
<summary><b>🏆 ARC Challenge</b></summary>

![arc_challenge](./plots/arc_challenge.png)

</details>

<details>
<summary><b>🏆 CommonsenseQA-BN</b></summary>

![commonsenseqa-bn](./plots/commonsenseqa-bn.png)

</details>

<details>
<summary><b>🏆 OpenBookQA-BN</b></summary>

![openbookqa-bn](./plots/openbookqa-bn.png)

</details>

<details>
<summary><b>🏆 BoolQ-BN</b></summary>

![boolq-bn](./plots/boolq-bn.png)

</details>

<details>
<summary><b>🏆 MMLU</b></summary>

![mmlu](./plots/mmlu.png)

</details>

<details>
<summary><b>🏆 TruthfulQA</b></summary>

![truthfulqa_mc1](./plots/truthfulqa_mc1.png)

</details>

<details>
<summary><b>🏆 Bangla MMLU</b></summary>

![bangla_mmlu](./plots/bangla_mmlu.png)

</details>

<details>
<summary><b>Aggregate NPM Across Benchmarks</b></summary>

![NPM vs Compute](./plots/aggregate_npm.png)

</details>

<details>
<summary><b>Performance vs Compute</b></summary>

![Performance vs Compute](./plots/performance_vs_compute.png)

This plot compares the compute requirements (measured as C = 6 * N * D, where N is the number of parameters and D is the number of tokens processed) against the performance of each model (measured by NPM mean). It highlights the trade-offs between model size, training data, and performance. LilTii models are compared against two baseline models: Qwen2.5-0.5B and Qwen3-0.6B-Base, which are state-of-the-art multilingual models.

</details>

<details>
<summary><b>Text Generation Examples</b></summary>

All models were prompted with the same Bengali prompts, and the generations were produced with the default parameters specified in the `generation_config.json` of each model. All models were set to generate up to 250 new tokens. LilTii models generally produce more text given their custom tokenizer and vocabulary, which is more adapted to Bengali.

<table border="1" cellpadding="5" cellspacing="0">
  <thead>
    <tr>
      <th>Model</th>
      <th>Prompt</th>
      <th>Generated Completion</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Qwen/Qwen2.5-0.5B</td>
      <td>
      <span style="color: red;">বাংলাদেশের রাজধানী হলো</span>
      </td>
      <td>
      <i>মর্যাদা শুরু আনুষ্ঠানিক পরিচালক, যা নির্মাণের সাথে দেবী পর্যায়ন করেন। রাজধানী বিশিষ্ট ইতিবাচ্ছিত পরিচালক সময় হলো ফোনে শুরু হতে চেয়ে চেয়ে চেয়ে চেয়ে চেয়েছিল। রাজধানী অবস্থিত খালিকা হলো মর্যাদার রাজধানীর খালিকা। রাজধানী অবস্থ ... </i>
      </td>
    </tr>
    <tr>
      <td></td>
      <td>
      <span style="color: red;">বাংলাদেশের প্রধান নদী হলো</span>
      </td>
      <td>
      <i>সিনামূল্যান্ড গ্রুপ নদী। সিনামূল্যান্ড গ্রুপ নদী ছিলেন যে সিনামূল্যান্ড গ্রুপ নদী ছিলেন ও সিনামূল্যান্ড গ্রুপ নদী ছিলেন নিশ্বনের প্রধান নদী। সিনামূল্যান্ড গ্রুপ নদী ছিলেন যে সিনামূল্যান্ড গ্রুপ নদী ছিলেন ও সিনামূল্যান্ড গ্রুপ নদ ... </i>
      </td>
    </tr>
    <tr>
      <td>Qwen/Qwen3-0.6B</td>
      <td>
      <span style="color: red;">বাংলাদেশের রাজধানী হলো</span>
      </td>
      <td>
      <i>কোনটি?\n\nবাংলাদেশের রাজধানী হলো মোহাম্মাদ পূর্বাবৃহক। এই জেলায় বিশ্বের বিভিন্ন প্রাচীন জাতীয় শাসকদ্বয় যথা পুরুষ হামীদ এবং গ্রস্ত জীবী আসমান বা মোহাম্মাদ রয়েছে। আসমান এদেশের প্রথম হামীদীয় শাসক, আসমান এর ছোট হামীদীয় উপজেলা ...</i>
      </td>
    </tr>
    <tr>
      <td></td>
      <td>
      <span style="color: red;">বাংলাদেশের প্রধান নদী হলো</span>
      </td>
      <td>
      <i>কী?\nA. সূর্য নদী\nB. দিল্লি নদী\nC. গুম্বার নদী\nD. মহাদেব নদী\nAnswer Choices: (A) A & B only (B) A & C only (C) B & C only (D) All the above\nThe correct answer is:\n\n**D. All the above**\n\nExplanation:\n- **B. দিল্লি নদী** is a river in Bangladesh.\n- **C. গুম্বার নদী** is also a river in Bangladesh.\n- **D. মহাদেব নদী** is a river in India, not Bangladesh.\nSo, all the rivers mentioned (B, C, and D) are in Bangladesh ...</i>
      </td>
    </tr>
    <tr>
      <td>Polygl0t/LilTii-v0.1</td>
      <td>
      <span style="color: red;">বাংলাদেশের রাজধানী হলো</span>
      </td>
      <td>
      <i>ঢাকা। কিন্তু এই ঢাকার একটি নাম আছে, যেটির সাথে জড়িয়ে রয়েছে অনেক ইতিহাস ও ঐতিহ্য । ঢাকা বাংলাদেশের সবচেয়ে বড় শহর এবং এটি দক্ষিণ এশিয়ার মধ্যে দ্বিতীয় বৃহত্তম নগরী হিসেবে পরিচিত৷ এর আয়তন ১ লক্ষ ৪৭ হাজার ৫ শত বর্গকিলোমিটার যা প্রায় বাংলাদেশর সমান ৷ এখানে বসবাস করে বিশ্বের বিভিন্ন দেশের মানুষ তবে বেশিরভাগই আসে পৃথিবীর অন্যান্য দেশ থেকে যেমন ভারত পাকিস্তান নেপাল শ্রীলঙ্কা ইত্যাদি দেশগুলো হতে আগত মানুষের সংখ্যা বেশি হয়ে থাকে তাই বলা যায় এদেশে প্রচুর পরিমাণে বিদেশী নাগরিকের আগমন ঘটেছে যারা এদেশের শিক্ষা সংস্কৃতিতে অবদান রেখে চলেছে প্রতিনিয়ত যার ফলে আমাদের দেশে গড়ে উঠেছে অসংখ্য বিশ্ববিদ্যালয় যেখানে উচ্চ শিক্ষার জন্য বিদেশীরা এসে পড়াশোনা করছে আর এজন্যেই হয়তোবা একে ‘বিশ্ববিদ্যালয়’ নামে ডাকা হয় কেননা এখানকার প্রতিটি শিক্ষার্থীর মাঝে মিশে গিয়েছে নিজ মাতৃভাষার প্রতি ভালোবাসা যেটা তাদের একাডেমিক পড়াশোনার ক্ষেত্রে প্রভাব ফেলে বলে আমি মনে করি কারণ তারা জানে বাংলা ভাষাটা কতটা গুরুত্বপূর্ণ একটা বিষয় সেখানে যদি কোনো ... </i>
      </td>
    </tr>
    <tr>
      <td></td>
      <td>
      <span style="color: red;">বাংলাদেশের প্রধান নদী হলো</span>
      </td>
      <td>
      <i>পদ্মা ও ব্রহ্মপুত্র। নদীর উৎপত্তিস্থল হিমালয় পর্বতমালার কৈলাশ শৃঙ্গের কাছে তিব্বতের মানস সরোবর হ্রদ থেকে । আর বাংলাদেশে প্রবেশ করে ফেনী জেলার মুহুরী নামে কুমিল্লা জেলায় এসে তিতাস নাম ধারণ করেছে এই দুই উপনদীই মিলিত হয়ে মেঘনা তৈরি হয়েছে এবং এর প্রবাহে রয়েছে অসংখ্য ছোট-বড় খাল বিল হাওর বাওড় এমনকি গ্রাম নগর জনপদ, শিল্প কারখানা সবই আছে এ নদীতে।। মানচিত্রের মাধ্যমে বাংলাদেশের নদ -নদীর অবস্থান দেখানো হল: ...</i>
      </td>
    </tr>
    <tr>
      <td>Polygl0t/LilTii-v0.2</td>
      <td>
      <span style="color: red;">বাংলাদেশের রাজধানী হলো</span>
      </td>
      <td>
      <i>ঢাকা। বাংলাদেশের বিভাগীয় শহরগুলোর মধ্যে অন্যতম হলো খুলনা, রাজশাহী ও চট্রগ্রাম ।\n- বাংলাদেশ এর মোট আয়তনের প্রায় ৫৬ শতাংশই সমুদ্র সমতল থেকে মাত্র ১ মিটার (৩ ফুট) উচ্চতায় অবস্থিত এবং উত্তর পূর্ব অংশ জুড়ে রয়েছে ভারতের সাথে সীমান্ত যা দেশের চার ভাগের একভাগ এলাকা দখল করেছে| অন্য তিন দিকে স্থল বেষ্টিত হওয়ায় এই অংশের ভূপ্রকৃতি মূলত পাহাড়ী অঞ্চলের মত উঁচু নিচু ভূমির উপর গড়ে উঠেছে যেখানে গাছপালা খুব কম ফলে দিনের বেশিরভাগ সময় সূর্যের আলো থাকে না বললেই চলে৷ বঙ্গোপসাগর উপকূলে বিস্তৃত উপকূলীয় বনভূমি আছে যার বেশির ভাগ ম্যানগ্রোভ জাতীয়; এগুলো ঝড় প্রতিরোধ করতে পারে বলে ধারণা করা হয় ৷ সুন্দরবনকে ১৯৮৭ সালে ইউনেস্কো বিশ্ব ঐতিহ্যবাহী স্থান হিসেবে ঘোষণা করে ...</i>
      </td>
    </tr>
    <tr>
      <td></td>
      <td>
      <span style="color: red;">বাংলাদেশের প্রধান নদী হলো</span>
      </td>
      <td> 
      <i>পদ্মা। নদীর উৎপত্তি হিমালয় পর্বতে এবং এর দৈর্ঘ্য ১,৫০০ কিলোমিটার (৯৩৫ মা)। এটি বাংলাদেশের উপর দিয়ে প্রবাহিত হয়ে বঙ্গোপসাগরে গিয়ে মিশেছে।[২] পদ্মা ও যমুনার মিলিত প্রবাহ পদ্মার নাম পেয়েছে বলে ধারণা করা হয়; যদিও এই মিলনের সঠিক প্রমাণ পাওয়া যায়নি[৩][৪], তবু পণ্ডিতদের অনুমান এটুকু যে পূর্ব-পশ্চিমদিকে গতিশীল যমুনা ছিল একটি একক বৃহৎ স্রোত যা দক্ষিণ দিকে অগ্রসর হতে হতে গঙ্গা নদীতে এসে পড়েছিল বলেই এটির নামকরণ হয়েছিল 'যমুনা' নামে । অন্যদিকে গ্রিক পুরাণ মতে দেবী রেমেফিসের পুত্রের বংশধর হিসাবে আদিগঙ্গার তীরে গড়ে ওঠা এক আর্য জনজাতির উপনিবেশ থেকে জন্ম নিয়েছিল ‘আর্যান’ বা পুণ্যতোয়া হিসেবে খ্যাত গঙ্গার অপরূপা ধারাটি - যার শাখা প্রশাখার সমন্বয়ে গঠিত হয়েছে বর্তমান কালিন্দী৷ এই দুই ধারার মিলনস্থলটিই আজকের বাংলাদেশে অবস্থিত| বাংলাদেশ অংশে পদ্মায় পানির গড় গভীরতা ৫.৭৮ মিটার অথবা ১৮ ফুটের সামান্য বেশি হলেও ভারত বিভাগের পর থেকেই পলি জমে ক্রমশ তা হ্রাস পেয়ে আসছে – এখন প্রায় ৩ মিঃ অর্থাৎ ১০ ফুট পর্যন্ত নিচে নেমে গেছে ৷ তাই বর্তমানে বর্ষাকালে পানি থাকে মাত্র ৩০০ সেমি.(১ গজ)এর মতো! ফলে তখনকার বিখ্যাত প্রম ...</i>
      </td>
    </tr>
  </tbody>
</table>

</details>

<details>
<summary><b>Other Comparisons</b></summary>

|                           | NPM (normalized mean) | Bangla MMLU | BoolQ-BN | CommonsenseQA-BN | OpenBookQA-BN | PIQA-BN | ARC Challenge | MMLU | HellaSwag | TruthfulQA MC1 |
| ------------------------- | --------------------- | ----------- | -------- | ---------------- | ------------- | ------- | ------------- | ---- | --------- | -------------- |
| **LilTii v0.2**           | 9.63                  | 0.26        | 0.61     | 0.32             | 0.32          | 0.61    | 0.26          | 0.27 | 0.32      | 0.25           |
| Qwen2.5-1.5B              | 9.36                  | 0.35        | 0.67     | 0.23             | 0.3           | 0.53    | 0.23          | 0.31 | 0.29      | 0.29           |
| Qwen2.5-1.5B-Instruct     | 8.74                  | 0.35        | 0.67     | 0.24             | 0.28          | 0.52    | 0.23          | 0.31 | 0.29      | 0.28           |
| Gemma-3-1b-it             | 8.3                   | 0.31        | 0.56     | 0.31             | 0.32          | 0.57    | 0.25          | 0.28 | 0.3       | 0.28           |
| Qwen3-0.6B-Base           | 8.07                  | 0.33        | 0.66     | 0.23             | 0.31          | 0.53    | 0.23          | 0.3  | 0.29      | 0.27           |
| Titulm-llama-3.2-3b-v2.0  | 7.94                  | 0.25        | 0.54     | 0.33             | 0.35          | 0.6     | 0.25          | 0.26 | 0.31      | 0.26           |
| Llama-3.2-1B-Instruct     | 7.74                  | 0.3         | 0.63     | 0.23             | 0.34          | 0.53    | 0.25          | 0.28 | 0.29      | 0.27           |
| Gemma-3-1b-pt             | 7.73                  | 0.25        | 0.57     | 0.32             | 0.32          | 0.58    | 0.25          | 0.27 | 0.3       | 0.27           |
| Gemma-2-2b                | 7.73                  | 0.32        | 0.6      | 0.28             | 0.33          | 0.56    | 0.24          | 0.25 | 0.28      | 0.25           |
| Qwen3-0.6B                | 6.28                  | 0.29        | 0.62     | 0.24             | 0.3           | 0.53    | 0.23          | 0.29 | 0.29      | 0.25           |
| Qwen2.5-0.5B              | 6.04                  | 0.31        | 0.58     | 0.22             | 0.31          | 0.54    | 0.23          | 0.28 | 0.28      | 0.28           |
| **LilTii v0.1**           | 5.82                  | 0.24        | 0.52     | 0.3              | 0.33          | 0.59    | 0.24          | 0.26 | 0.3       | 0.24           |
| Llama-3.2-1B              | 5.71                  | 0.28        | 0.57     | 0.23             | 0.32          | 0.53    | 0.24          | 0.28 | 0.29      | 0.28           |
| Qwen2.5-0.5B-Instruct     | 5.48                  | 0.31        | 0.56     | 0.22             | 0.3           | 0.53    | 0.23          | 0.29 | 0.29      | 0.28           |
| BanglaLLama-3.2-1b-v0.0.1 | 4.28                  | 0.26        | 0.53     | 0.24             | 0.31          | 0.53    | 0.24          | 0.27 | 0.29      | 0.28           |
| Titulm-llama-3.2-1b-v2.0  | 4.11                  | 0.25        | 0.5      | 0.27             | 0.32          | 0.57    | 0.23          | 0.24 | 0.29      | 0.24           |
| BanglaLLama-3.2-3b-v0.0.3 | 2.86                  | 0.33        | 0.54     | 0.2              | 0.29          | 0.5     | 0.24          | 0.25 | 0.26      | 0.24           |
| Goldfish-bengali-1000mb   | 2.79                  | 0.25        | 0.51     | 0.25             | 0.3           | 0.54    | 0.24          | 0.25 | 0.27      | 0.26           |

</details>

## Cite as 🤗 

```latex
@misc{fatimah2026liltii,
  title={{LilTii: A 0.6B Bengali Language Model that Outperforms Qwen}},
  author={Shiza Fatimah and Aniket Sen and Sophia Falk and Florian Mai and Lucie Flek and Nicholas Kluge Corr{\^e}a},
  year={2026},
  howpublished={\url{https://hf.co/blog/Polygl0t/liltii}}
}
```

## Aknowlegments

Polyglot is a project funded by the Federal Ministry of Education and Research (BMBF) and the Ministry of Culture and Science of the State of North Rhine-Westphalia (MWK) as part of TRA Sustainable Futures (University of Bonn) and the Excellence Strategy of the federal and state governments.

We also gratefully acknowledge the granted access to the [Marvin cluster](https://www.hpc.uni-bonn.de/en/systems/marvin) hosted by [University of Bonn](https://www.uni-bonn.de/en) along with the support provided by its High Performance Computing & Analytics Lab.

## License

LilTii is licensed under the Apache License, Version 2.0. For more details, see the [LICENSE](LICENSE) file.
