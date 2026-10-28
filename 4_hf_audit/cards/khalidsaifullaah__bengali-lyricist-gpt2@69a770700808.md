---
language: bn
tags:
- text generation
- bengali
- gpt2
- bangla
- causal-lm
widget:
- text: "জীবনের মানে "
pipeline_tag: text-generation
---

<!-- 
---
tags:
- generated_from_trainer
datasets:
- null
model_index:
- name: bengali-lyricist-gpt2
  results:
  - task:
      name: Causal Language Modeling
      type: text-generation
---
-->

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# bengali-lyricist-gpt2

This model is a fine-tuned version of [flax-community/gpt2-bengali](https://huggingface.co/flax-community/gpt2-bengali) on the [Bengali Song Lyrics](https://www.kaggle.com/shakirulhasan/bangla-song-lyrics) dataset from Kaggle.
It achieves the following results on the evaluation set:
- Loss: 2.1199

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 32
- eval_batch_size: 32
- seed: 42
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 30

### Training results

| Training Loss | Epoch | Step | Validation Loss |
|:-------------:|:-----:|:----:|:---------------:|
| No log        | 1.0   | 284  | 2.0302          |
| 1.9991        | 2.0   | 568  | 2.0079          |
| 1.9991        | 3.0   | 852  | 1.9956          |
| 1.9135        | 4.0   | 1136 | 1.9885          |
| 1.9135        | 5.0   | 1420 | 1.9840          |
| 1.8561        | 6.0   | 1704 | 1.9831          |
| 1.8561        | 7.0   | 1988 | 1.9828          |
| 1.8094        | 8.0   | 2272 | 1.9827          |
| 1.7663        | 9.0   | 2556 | 1.9868          |
| 1.7663        | 10.0  | 2840 | 1.9902          |
| 1.7279        | 11.0  | 3124 | 1.9961          |
| 1.7279        | 12.0  | 3408 | 2.0023          |
| 1.6887        | 13.0  | 3692 | 2.0092          |
| 1.6887        | 14.0  | 3976 | 2.0162          |
| 1.6546        | 15.0  | 4260 | 2.0225          |
| 1.6217        | 16.0  | 4544 | 2.0315          |
| 1.6217        | 17.0  | 4828 | 2.0410          |
| 1.5953        | 18.0  | 5112 | 2.0474          |
| 1.5953        | 19.0  | 5396 | 2.0587          |
| 1.5648        | 20.0  | 5680 | 2.0679          |
| 1.5648        | 21.0  | 5964 | 2.0745          |
| 1.5413        | 22.0  | 6248 | 2.0836          |
| 1.5238        | 23.0  | 6532 | 2.0890          |
| 1.5238        | 24.0  | 6816 | 2.0969          |
| 1.5043        | 25.0  | 7100 | 2.1035          |
| 1.5043        | 26.0  | 7384 | 2.1091          |
| 1.4936        | 27.0  | 7668 | 2.1135          |
| 1.4936        | 28.0  | 7952 | 2.1172          |
| 1.4822        | 29.0  | 8236 | 2.1186          |
| 1.4783        | 30.0  | 8520 | 2.1199          |


### Framework versions

- Transformers 4.9.0.dev0
- Pytorch 1.9.0+cu102
- Datasets 1.9.1.dev0
- Tokenizers 0.10.3
