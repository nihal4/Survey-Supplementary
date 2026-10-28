---
base_model: mistralai/Ministral-3-3B-Base-2512
language: [bn, en]
license: apache-2.0
pipeline_tag: text-generation
library_name: transformers
tags: [banglish, bengali, bangla, conversational, low-resource-languages]
---

# Banglish Companion 3B

### Answers the way you typed

Most models answer romanized Bengali in English, or in Bengali script, or in
neither. This one answers the way the message was written.

```
you    aj mood bhalo na
model  mama mood bhalo na hole patience rakh. Ar ki korle feel better hobe?
```

Full-precision weights, 6.9 GB. Runs on CPU or GPU, and nothing
leaves your machine.

[Ministral-3-3B](https://huggingface.co/mistralai/Ministral-3-3B-Base-2512),
further trained on Banglish conversation. It follows
[banglish-companion](https://huggingface.co/sifat-febo/banglish-companion),
the 1.7B, and answers shorter and closer to the question.

&nbsp;

## Banglish e

**ki eta?** Banglish e kotha bola ekta model. 6.9 GB. Internet lagbe na,
account lagbe na, taka lagbe na — tumi ja likhba tomar computer er baire jabe na.

**ki lagbe?** `pip install transformers torch`. Mac hole
[banglish-companion-3b-mlx](https://huggingface.co/sifat-febo/banglish-companion-3b-mlx)
ta niyo — choto ar druto.

**kemon uttor dey?** choto uttor, ar age jigges kore ki hoyeche. lomba lecture
dey na. chhoto model — bhul tottho confident bhabe bole, tai fact er jonno
eta use koro na.

&nbsp;

## Use it

```bash
pip install transformers torch huggingface_hub
hf download sifat-febo/banglish-companion-3b --local-dir banglish-3b
python banglish-3b/companion.py
```

That starts a chat in your terminal. It first answers *aj mood bhalo na*, the
line shown at the top of this page, then whatever you type. In your own code,
`from companion import reply` is the only import you need. It reads the
message first with the small `ontor` classifier that ships here. If someone
writes that they are in danger, it replies with fixed text and does not ask
the model. Otherwise it answers with the settings this model was tested with.

On a Mac, the same model runs at 3.6 GB as
[banglish-companion-3b-mlx](https://huggingface.co/sifat-febo/banglish-companion-3b-mlx).

&nbsp;

## Limits

- **Banglish only.** Not Bengali script, not English. There is no formal
  register — the language does not have one in writing.
- **It states wrong things confidently.** A 3B will invent a number or a name
  mid-sentence. Not a source of fact.
- **Short exchanges.** It loses the thread over long conversations, and it is
  not a therapist, doctor, or lawyer.
- **Some answers are not the model's.** If someone writes that they are in
  danger, the reply is fixed text from a file in this repo. The model is not
  asked.

&nbsp;

## AI Disclosure

The author designed the system, chose the base models, ran all training and
measurement on the author's own machine, read the models' conversations, and
chose what to publish and what to withhold. [Claude Code](https://claude.ai)
(Anthropic) was used as a coding and writing tool under that direction.

&nbsp;

## License

Apache 2.0. Base model
[Ministral-3-3B-Base-2512](https://huggingface.co/mistralai/Ministral-3-3B-Base-2512)
(Mistral AI, Apache 2.0).

Cite the technical report, which describes how the models were built,
trained and measured: <https://doi.org/10.5281/zenodo.22371896>

```bibtex
@misc{febo2026banglishcompanion,
  author    = {Febo, Sifat},
  title     = {Banglish Companion: Small Chat Models for Romanized Bengali
               — Technical Report},
  year      = {2026},
  month     = sep,
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.5281/zenodo.22371896},
  url       = {https://doi.org/10.5281/zenodo.22371896},
  note      = {Repository: sifat-febo/banglish-companion-3b}
}
```
