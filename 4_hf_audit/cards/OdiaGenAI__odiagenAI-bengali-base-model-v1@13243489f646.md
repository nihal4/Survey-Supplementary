---
license: cc-by-nc-4.0
language:
- bn
---
# Model Card for Model ID

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Model description

odiagenAI-bengali-base-model-v1 is based on Llama-7b and finetuned with 252k Bengali instruction set. The instruction set is translated data from open-source resources, resulting in good Bengali instruction understanding and response generation capabilities. 

The code of Bengali data generation and other detailed information can be found in our Github project repository: https://github.com/OdiaGenAI/GenerativeAI_and_LLM_Odia.


## Training hyper-parameters
| Parameter | Value |
| ------ | ------ |
| Batch size | 128 |
| Learning rate | 3e-4 |
| Epochs | 5 |
|Cutoff length | 256 |
|Weight_decay | 0.001 |
|Warmup_rate | 0.1 |
|LR_scheduler | linear |
|Lora r | 16 |
|Lora target modules | (q_proj, k_proj, v_proj, o_proj) |


Instructions for running it can be found at https://github.com/OdiaGenAI/GenerativeAI_and_LLM_Odia.

### Licensing Information

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

### Citation Information

If you find this helpful repository, please consider giving 👏 and citing:

```
@misc{OdiaGenAI-Bengali-LLM,
  author = {Shantipriya Parida and Sambit Sekhar and Guneet Singh Kohli and Arghyadeep Sen and Shashikanta Sahoo},
  title = {Bengali Instruction-Tuning Model},
  year = {2023},
  publisher = {Hugging Face},
  journal = {Hugging Face repository},
  howpublished = {\url{https://huggingface.co/OdiaGenAI}},
}
```

### Contributions

- Shantipriya Parida
- Sambit Sekhar
- Guneet Singh Kohli
- Arghyadeep Sen
- Shashikanta Sahoo