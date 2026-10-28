---
license: mit
base_model: HuggingFaceH4/zephyr-7b-beta
tags:
- generated_from_trainer
model-index:
- name: bondhu-7b-alpha
  results: []
datasets:
- rishiraj/bengalichat
language:
- bn
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# bondhu-7b-alpha

This model is a fine-tuned version of [HuggingFaceH4/zephyr-7b-beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) on an unknown dataset.
It achieves the following results on the evaluation set:
- Loss: 1.4296

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 2e-05
- train_batch_size: 4
- eval_batch_size: 8
- seed: 42
- distributed_type: multi-GPU
- gradient_accumulation_steps: 128
- total_train_batch_size: 512
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- num_epochs: 1

### Training results

| Training Loss | Epoch | Step | Validation Loss |
|:-------------:|:-----:|:----:|:---------------:|
| 1.4503        | 0.65  | 12   | 1.4296          |


### Framework versions

- Transformers 4.35.0
- Pytorch 2.1.1+cu121
- Datasets 2.14.6
- Tokenizers 0.14.1