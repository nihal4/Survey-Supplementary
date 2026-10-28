---
library_name: transformers
license: apache-2.0
tags:
- merge
- mergekit
- lazymergekit
- sillytavern
- roleplay
- rp
- math
- coding
- mistral
- 12b
base_model:
- MarinaraSpaghetti/NemoMix-Unleashed-12B
- inflatebot/MN-12B-Mag-Mell-R1
- elinas/Chronos-Gold-12B-1.0
- Retreatcost/KansenSakura-Eclipse-RP-12b
- redrix/patricide-12B-Unslop-Mell-v2
language:
- en
- bn
---

# RP-king-12b

RP-king-12b is a merge of the following models using [mergekit](https://github.com/cg123/mergekit):
* [MarinaraSpaghetti/NemoMix-Unleashed-12B](https://huggingface.co/MarinaraSpaghetti/NemoMix-Unleashed-12B)
* [inflatebot/MN-12B-Mag-Mell-R1](https://huggingface.co/inflatebot/MN-12B-Mag-Mell-R1)
* [elinas/Chronos-Gold-12B-1.0](https://huggingface.co/elinas/Chronos-Gold-12B-1.0)
* [Retreatcost/KansenSakura-Eclipse-RP-12b](https://huggingface.co/Retreatcost/KansenSakura-Eclipse-RP-12b)
* [redrix/patricide-12B-Unslop-Mell-v2](https://huggingface.co/redrix/patricide-12B-Unslop-Mell-v2)

## 🧩 Configuration

```yamlmodels:
  - model: MarinaraSpaghetti/NemoMix-Unleashed-12B  # Base model for creative foundation
    parameters:
      density: 0.65
      weight: 1.0
  - model: inflatebot/MN-12B-Mag-Mell-R1  # For worldbuilding and prose
    parameters:
      density: 0.8
      weight: 1.2
  - model: elinas/Chronos-Gold-12B-1.0  # For roleplay and prompt adherence
    parameters:
      density: 0.9
      weight: 1.1
  - model: Retreatcost/KansenSakura-Eclipse-RP-12b
    parameters:
      density: 0.5
      weight: 0.7
  - model: redrix/patricide-12B-Unslop-Mell-v2  # For anti-GPTism and balance
    parameters:
      density: 0.6
      weight: 0.9
merge_method: dare_ties
base_model: MarinaraSpaghetti/NemoMix-Unleashed-12B
parameters:
  normalize: true
dtype: bfloat16
tokenizer_source: base
```


# sillytavern usages:
in sillytavern you can use it just like any other mistral-nemo model. you should pick chatml template and set those parameters.:

```
tempatature: 0.5 - 1.2.
0.1 Top A or 0.01-0.1 Min P,
and with 0.8/1.75/2/0 DRY.
Also works with lower Temperatures below 1.0. Nothing more needed.
```