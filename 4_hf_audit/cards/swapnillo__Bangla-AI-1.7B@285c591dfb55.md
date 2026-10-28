---
library_name: transformers
license: mit
datasets:
- md-nishat-008/Bangla-Instruct
language:
- en
- bn
metrics:
- bleu
- accuracy
base_model:
- Qwen/Qwen3-1.7B
---

# Qwen3-1.7B-Bengali-Instruct

## Model Details

### Model Description

This model is a fine-tuned version of Qwen/Qwen3-1.7B on Bengali (Bangla) instruction-response pairs. It has been optimized to understand and generate natural Bengali language responses while maintaining cultural appropriateness and proper grammar. The model uses LoRA (Low-Rank Adaptation) for efficient fine-tuning on a 100K Bengali instruction dataset.

- **Developed by:** Ismam Nur Swapnil
- **Model type:** Causal Language Model (Decoder-only Transformer)
- **Language(s):** Bengali (Bangla)
- **License:** Same as base Qwen3-1.7B model license
- **Finetuned from model:** [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B)

### Model Sources

- **Base Repository:** [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B)
- **Training Dataset:** [swapnillo/Bangla-Instruction-Tuning-100K](https://huggingface.co/datasets/swapnillo/Bangla-Instruction-Tuning-100K)

## Uses

### Direct Use

This model is designed for conversational AI applications in Bengali. It can be used for:
- Bengali chatbots and virtual assistants
- Question-answering systems in Bengali
- Instruction-following tasks in Bengali language
- General Bengali language generation tasks

The model is optimized to provide culturally appropriate responses with proper Bengali grammar and natural conversational style.

### Downstream Use

This model can be further fine-tuned for specific Bengali NLP tasks such as:
- Domain-specific question answering (medical, legal, educational)
- Bengali content generation
- Translation assistance
- Customer service chatbots for Bengali-speaking users

### Out-of-Scope Use

This model should not be used for:
- Generating harmful, biased, or offensive content
- High-stakes decision making without human oversight
- Applications requiring 100% accuracy (medical diagnosis, legal advice, etc.)
- Languages other than Bengali (primary training is Bengali-focused)

## Bias, Risks, and Limitations

- The model's responses are limited by the quality and diversity of the training data
- May occasionally generate factually incorrect information
- Could reflect biases present in the training dataset
- Performance may vary across different Bengali dialects and registers
- Not suitable for tasks requiring real-time critical decision making

### Recommendations

Users (both direct and downstream) should:
- Verify critical information from the model's outputs
- Implement content filtering for production deployments
- Monitor for potential biases in model outputs
- Not use the model for high-stakes decisions without human oversight
- Test thoroughly on their specific use cases before deployment

## How to Get Started with the Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model and tokenizer
base_model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-1.7B",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-1.7B", trust_remote_code=True)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "path/to/your/model")

# Generate response
messages = [
    {"role": "system", "content": "You are a knowledgeable AI assistant fluent in Bengali language and culture. Provide accurate, helpful, and culturally appropriate responses. Use proper Bengali grammar and natural conversational style. When answering questions, be clear, concise, and respectful of Bengali cultural norms."},
    {"role": "user", "content": "বাংলাদেশের রাজধানী কোথায়?"}
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.7)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

## Training Details

### Training Data

The model was fine-tuned on the [Bangla-Instruction-Tuning-100K dataset](https://huggingface.co/datasets/swapnillo/Bangla-Instruction-Tuning-100K), which contains approximately 100,000 Bengali instruction-response pairs covering diverse topics and conversational patterns.

**Data Split:**
- Training: 99% (~99,000 examples)
- Validation: 1% (~1,000 examples)
- Test split ratio: 0.01, seed: 42

### Training Procedure

The model was fine-tuned using LoRA (Low-Rank Adaptation) with DeepSpeed ZeRO-3 optimization for efficient training.

#### LoRA Configuration

- **LoRA Rank (r):** 32
- **LoRA Alpha:** 64
- **LoRA Dropout:** 0.1
- **Target Modules:** q_proj, k_proj, v_proj
- **Task Type:** Causal Language Modeling
- **Bias:** none

#### Training Hyperparameters

- **Training regime:** fp16 mixed precision with DeepSpeed ZeRO-3
- **Number of epochs:** 1
- **Maximum training steps:** 2,700
- **Per device train batch size:** 2
- **Per device eval batch size:** 2
- **Gradient accumulation steps:** 8
- **Effective batch size:** 16 (2 × 8)
- **Learning rate:** 1e-4
- **Learning rate scheduler:** Cosine
- **Warmup steps:** 100
- **Weight decay:** 0.01
- **Max gradient norm:** 1.0
- **Optimizer:** AdamW (PyTorch)
- **Max sequence length:** 1024 tokens
- **Evaluation strategy:** Every 250 steps
- **Logging:** Every step
- **Checkpointing:** Every 500 steps (keeping best checkpoint only)

#### Speeds, Sizes, Times

- **Hardware:** Training performed on Kaggle GPU environment
- **Optimization:** DeepSpeed ZeRO-3 for memory efficiency
- **Data workers:** 2 with pin memory enabled
- **Monitoring:** Weights & Biases (wandb) integration
- **LoRA adapter size:** Significantly smaller than full model (~1-2% of parameters)

## Evaluation

### Testing Data, Factors & Metrics

#### Testing Data

Validation set: 1% of the Bangla-Instruction-Tuning-100K dataset (~1,000 examples), randomly split with seed 42.

#### Factors

Evaluation focuses on:
- Bengali language fluency and grammatical correctness
- Instruction-following capability
- Cultural appropriateness of responses
- Response relevance and coherence

#### Metrics

- **Primary metric:** Training and validation loss
- **Best model selection:** Based on lowest validation loss
- **Monitoring:** Loss tracked at every step via wandb

### Results

The model was trained for 2,700 steps with evaluation every 250 steps. The best checkpoint was selected based on validation loss. Specific metrics can be viewed in the associated Weights & Biases project: "qwen-bangla-finetuning".

## Environmental Impact

Training was performed on Kaggle's GPU infrastructure with DeepSpeed ZeRO-3 optimization for improved efficiency.

- **Hardware Type:** GPU (Kaggle environment)
- **Training time:** ~2,700 training steps with fp16 precision
- **Compute Region:** Cloud-based (Kaggle)
- **Optimization:** DeepSpeed ZeRO-3 for memory efficiency, LoRA for parameter efficiency

Carbon emissions could be estimated using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700).

## Technical Specifications

### Model Architecture and Objective

- **Base Architecture:** Qwen3-1.7B (1.7 billion parameters)
- **Fine-tuning Method:** LoRA (Low-Rank Adaptation)
- **Trainable Parameters:** Only LoRA adapters (~1-2% of total parameters)
- **Objective:** Causal language modeling with instruction tuning
- **Context Length:** 1024 tokens (during training)

### Compute Infrastructure

#### Hardware

- **Platform:** Kaggle GPU environment
- **Precision:** FP16 mixed precision training
- **Memory Optimization:** DeepSpeed ZeRO-3

#### Software

- **Framework:** PyTorch with Hugging Face Transformers
- **Key Libraries:**
  - `transformers`: Model and tokenizer
  - `peft`: LoRA implementation
  - `datasets`: Data loading
  - `deepspeed`: Distributed training optimization
  - `wandb`: Experiment tracking
- **Python Version:** Compatible with transformers ecosystem

## Citation

**BibTeX:**

```bibtex
@misc{qwen3-bengali-instruct,
  author = {Ismam Nur Swapnil},
  title = {Qwen3-1.7B-Bengali-Instruct: A Fine-tuned Bengali Language Model},
  year = {2024},
  publisher = {HuggingFace},
  howpublished = {\url{https://huggingface.co/swapnillo/Bangla-AI-1.7B}}
}
```

## Model Card Authors

Ismam Nur Swapnil

## Model Card Contact

For questions or feedback about this model, please open an issue in the model repository or contact the developer through HuggingFace.