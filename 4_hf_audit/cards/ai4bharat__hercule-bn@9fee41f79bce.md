---
library_name: transformers
license: mit
language:
- bn
metrics:
- pearsonr
- spearmanr
- accuracy
base_model:
- meta-llama/Llama-3.1-8B-Instruct
pipeline_tag: text-generation
---

# Model Card for Hercule
Hercule is a cross-lingual evaluation model introduced as part of the CIA Suite to assess multilingual Large Language Models (LLMs). It addresses the challenge of evaluating multilingual LLMs by using English reference responses to score multilingual outputs.

Fine-tuned on the INTEL dataset, Hercule demonstrates better alignment with human judgments compared to zero-shot evaluations by proprietary models like GPT-4, on the RECON test set. It excels particularly in low-resource scenarios and supports zero-shot evaluations on unseen languages. The model employs reference-based evaluation, providing feedback and scores on a 1-5 scale, and highlights the effectiveness of lightweight fine-tuning methods (like LoRA) for efficient multilingual evaluation. All FFT models and LoRA weights are available [here](https://huggingface.co/collections/ai4bharat/cia-suite-66ea9a7e18a6c70bd8de27a1).


# Model Details

## Model Description

- **Model type:** Evaluator Language model
- **Language(s) (NLP):** Bengali
- **Related Models:** [Hercule Models](https://huggingface.co/collections/ai4bharat/cia-suite-66ea9a7e18a6c70bd8de27a1)
- **Resources for more information:**
  - [Research paper](https://arxiv.org/abs/2410.13394)
  - [GitHub Repo](https://github.com/AI4Bharat/CIA)


Hercule in fine-tuned on [Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) using Intel training data and evaluated on Recon test set. Models for other languages are available in [CIA Suite](https://huggingface.co/collections/ai4bharat/cia-suite-66ea9a7e18a6c70bd8de27a1).

## Prompt Format

We’ve developed wrapper functions and classes to make it easy to work with Hercule. Check them out on our [github repository](https://github.com/AI4Bharat/CIA) – we highly recommend using them!

If you only need to use the model for your specific use case, please follow the prompt format provided below.

### Reference Guided Direct Assessment
The Hercule model expects four input components: an evaluation instruction (multilingual), a response to evaluate (multilingual), a scoring rubric (English), and a reference answer (English). Use the prompt format provided below, ensuring that you include the instruction, response, reference answer, evaluation criteria, and a detailed score rubric for each score from 1 to 5.

After running inference with HERCULE, the output will include feedback and a score, separated by the phrase ```[RESULT]```.
```
###Task Description:
An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.
3. The output format should look as follows: \"Feedback: (write a feedback for criteria) [RESULT] (an integer number between 1 and 5)\"
4. Please do not generate any other opening, closing, and explanations.

###The instruction to evaluate:
{instruction}

###Response to evaluate:
{response}

###Reference Answer (Score 5):
{reference_answer}

###Score Rubrics:
[{criteria}]
Score 1: {score1_rubric}
Score 2: {score2_rubric}
Score 3: {score3_rubric}
Score 4: {score4_rubric}
Score 5: {score5_rubric}

###Feedback: 
```

We use the same evaluation prompt as used in [Prometheus 2](https://huggingface.co/prometheus-eval/prometheus-7b-v2.0).

## Links for Reference

- **Repository**: https://github.com/AI4Bharat/CIA 
- **Paper**: https://arxiv.org/abs/2410.13394
- **Point of Contact**: sumanthd@cse.iitm.ac.in, safikhan@ai4bharat.org

## License
Intel training data is created from [Feedback Collection](https://huggingface.co/datasets/prometheus-eval/Feedback-Collection) which is subject to OpenAI's Terms of Use for the generated data. If you suspect any violations, please reach out to us.


# Citation


If you find the following model helpful, please consider citing our paper!

**BibTeX:**

```bibtex
@article{doddapaneni2024crosslingual,
  title   = {Cross-Lingual Auto Evaluation for Assessing Multilingual LLMs},
  author  = {Sumanth Doddapaneni and Mohammed Safi Ur Rahman Khan and Dilip Venkatesh and Raj Dabre and Anoop Kunchukuttan and Mitesh M. Khapra},
  year    = {2024},
  journal = {arXiv preprint arXiv: 2410.13394}
}
```