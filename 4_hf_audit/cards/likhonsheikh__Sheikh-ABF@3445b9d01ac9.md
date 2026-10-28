
---
library_name: transformers
tags:
- Bangla
- nlp
- decoder-only
- causal-lm
- Lora
- code-generation
- agentic-ai
- from-scratch
metrics:
- pass@k
- task-completion-rate
model_name: Sheikh-ABF
language: bn
license: mit
---

# Sheikh-ABF: Sheikh Artificial Bangla Foundation

## Model Description

**Sheikh-ABF** is a state-of-the-art, **decoder-only Transformer language model for Bangla NLP**, developed entirely **from scratch**. This project emphasizes a **Bangla-first approach**, focusing on the unique linguistic and cultural aspects of the Bengali language. The name 'Sheikh' explicitly refers to its origin as a model developed in **Bangladesh**, aiming to provide a foundational LLM for the region.

### Goal
The primary objective is to create a robust base language model capable of advanced **internal reasoning**, moving beyond simple pattern matching to understand and process information more deeply. This base model serves as a strong foundation for future fine-tuning and specialized applications.

### Core Principles
*   **No Pre-trained Weights**: Trained entirely from scratch, ensuring a truly native Bangla foundation.
*   **Bangla-First Approach**: Optimized for Bangla, addressing its specific linguistic nuances.
*   **Internal Reasoning**: Designed to learn explicit 'thought processes' during training via interleaved thinking.
*   **Base Model Only**: Focused on providing a general-purpose foundation, not end-use applications.

## Model Architecture

The model is a **decoder-only Transformer**, styled after **GPT-2**, with approximately **~60 million parameters**.

*   **Layers**: 8
*   **Hidden Size (Embedding Dimension)**: 512
*   **Attention Heads**: 8
*   **Context Length (Maximum Sequence Length)**: 1024 tokens
*   **Dropout Rate**: 0.1 (applied to residual connections, embeddings, and attention probabilities)

## Tokenizer Details

The tokenizer is a **SentencePiece BPE (Byte-Pair Encoding) tokenizer**, trained exclusively on a **Bangla-only corpus**. It features a **vocabulary size of 32,000** unique tokens and incorporates several mandatory special tokens:

*   `<bos>`: Beginning of Sentence
*   `<eos>`: End of Sentence
*   `<pad>`: Padding token
*   `<think>`: Start Thinking (for internal reasoning blocks during training)
*   `</think>`: End Thinking

These tokens are consistently used for proper parsing, context handling, and enabling advanced training strategies like loss masking.

## Dataset and Mixing Ratios

The training corpus is a blend of three distinct dataset types:

*   **70% Raw Bangla Text**: For foundational language modeling and fluency.
*   **20% Instruction/QA**: For improving instruction following and question answering capabilities.
*   **10% Reasoning**: Incorporates interleaved thinking (`<think>...</think>`) patterns to foster internal reasoning processes.

## Interleaved Thinking and Loss Weighting

**Interleaved Thinking** is a core training strategy where explicit 'thought processes' (`<think>...</think>`) are included in the training data to teach the model logical reasoning. During inference, the model is expected to internalize this reasoning and produce direct answers without generating the `<think>` blocks.

To facilitate this, a **differential loss weighting strategy** is applied:
*   **Normal Tokens**: Loss weight of 1.0 (emphasizing accurate generation of primary content).
*   **`<think>` Tokens**: Loss weight of 0.3 (encouraging internalization of reasoning logic without over-prioritizing explicit generation).

## Training Configuration

The base model was trained with efficiency and resource optimization in mind:

*   **FP16 (Mixed Precision)**: Reduces memory and speeds up computations.
*   **Gradient Checkpointing**: Further reduces memory footprint.
*   **Gradient Accumulation Steps**: 8 (effective batch size of 16, with micro-batch size of 2).

## LoRA Fine-Tuning for Coding and Agentic Workflows

This model has been conceptually prepared for **LoRA (Low-Rank Adaptation) fine-tuning**, specifically targeting **coding tasks and agentic workflows**. LoRA allows for efficient adaptation by training only a small fraction of parameters while keeping the base model frozen.

### LoRA Strategy
*   **Target Modules**: `c_attn` (query, key, and value projections in attention mechanism).
*   **Rank (`r`)**: 8
*   **Scaling Coefficient (`lora_alpha`)**: 16
*   **Dropout (`lora_dropout`)**: 0.05

### Adapter Training Configuration (Conceptual)
*   **Learning Rate**: `5e-4` (0.0005)
*   **Epochs**: 5 (initial)
*   **Effective Batch Size**: 16 (micro-batch of 2, 8 gradient accumulation steps)
*   **Scheduler**: Linear warmup (10%) and linear decay.

## Evaluation Benchmarks (Conceptual)

To assess the LoRA fine-tuned model's performance on specialized tasks, hypothetical benchmarks were considered:

### Coding Tasks
*   **Benchmarks**: HumanEval-like (Bangla adaptation), LeetCode-style (simplified Bangla), Code Correction/Refactoring.
*   **Metrics**: Functional Correctness (Pass@k), Adherence to Problem Constraints, Code Generation Quality, Safety/Security.

### Agentic Workflows
*   **Benchmarks**: Simulated Environment Tasks, Tool-Use Scenarios, Multi-step Reasoning Chains.
*   **Metrics**: Task Completion Rate, Efficiency of Steps Taken, Correct Use of Tools, Adherence to User Intent, Robustness to Ambiguity.

## Conceptual Benchmark Results

Below are hypothetical performance metrics for the LoRA fine-tuned model on coding and agentic tasks. These illustrate the expected types of evaluation results.

### Coding Task Metrics:

![Coding Metrics](coding_metrics.png)

### Agentic Task Metrics:

![Agentic Metrics](agentic_metrics.png)

## Usage Instructions

To load and use the fine-tuned Bangla Decoder-Only Transformer model and its tokenizer from the Hugging Face Hub, you can use the `transformers` library.

### Loading the Model and Tokenizer

First, ensure you have the `transformers` and `torch` libraries installed. Then, you can load the model and tokenizer using their `from_pretrained` methods, specifying the `repo_id`.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Define the repository ID on Hugging Face Hub
repo_id = "likhonsheikh/bangla-decoder-only-transformer"

# Load the model
model = AutoModelForCausalLM.from_pretrained(repo_id)
# Ensure the model is in evaluation mode and on the correct device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device).eval()
print(f"Model loaded from {repo_id} and moved to {device}.")

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(repo_id)
print(f"Tokenizer loaded from {repo_id}.")

# Set pad_token_id if not already set (important for generation)
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '<pad>'})
    # Resize model embeddings if new tokens were added
    model.resize_token_embeddings(len(tokenizer))
```

### Performing Text Generation

Once the model and tokenizer are loaded, you can use the `model.generate()` method to create new text. It's important to prepare your prompt with the `<bos>` (beginning of sentence) token to signal the start of generation, similar to how the model was trained. The model was trained with loss masking for `<think>` tokens, meaning it focuses on generating the surrounding context rather than the content within `<think>` blocks. During inference, if the model generates a `<think>` token, it would typically generate an empty thought or move past it as it was trained to not predict its content explicitly.

```python
# Example prompt for text generation
prompt = "<bos> বাংলাদেশের জাতীয় ফল হলো " # Bangla for: "The national fruit of Bangladesh is "

# Encode the prompt
input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

# Generate text
# You can adjust parameters like max_new_tokens, num_beams, temperature, top_k, top_p
output_ids = model.generate(
    input_ids,
    max_new_tokens=50, # Generate up to 50 new tokens
    num_return_sequences=1,
    do_sample=True, # Enable sampling for more diverse outputs
    top_k=50, # Sample from top 50 probable tokens
    top_p=0.95, # Sample from tokens that cumulatively exceed 95% probability
    temperature=0.7, # Controls randomness: lower means less random
    pad_token_id=tokenizer.pad_token_id, # Use the pad token ID
    eos_token_id=tokenizer.eos_token_id # Stop generation at EOS token
)

# Decode the generated text
generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=False)

print("
Generated Text:")
print(generated_text)
```

## Future Work and Next Steps

This project provides a foundational decoder-only Transformer model and a custom Bangla BPE tokenizer, trained according to the 'Sheikh-ABF Final Training Plan'. To further enhance its capabilities and utility, the following next steps and future work are suggested:

1.  **Dataset Expansion and Diversification**: The current training corpus is a small placeholder. Expanding the dataset significantly with more diverse and high-quality Bangla text, covering various domains (e.g., news, literature, technical, social media), will greatly improve the model's fluency, coherence, and knowledge.

2.  **Advanced Benchmarking**: Conduct comprehensive benchmarking against existing state-of-the-art Bangla NLP models across a suite of downstream tasks, such as text summarization, question answering, sentiment analysis, and machine translation. This will provide a clearer understanding of the model's strengths and weaknesses.

3.  **Fine-tuning for Specific Tasks**: Fine-tune the base model on task-specific datasets to adapt it for specialized applications. For instance, fine-tuning on a Bangla chatbot dataset for conversational AI, or on a legal document corpus for legal NLP tasks.

4.  **Experiment with Loss Weighting**: Further experimentation with the loss weighting strategy for `<think>` tokens is crucial. Different weighting schemes and dynamic adjustment based on training progress could lead to more effective learning of reasoning patterns.

5.  **Model Optimization and Scaling**: Explore techniques for model optimization, such as knowledge distillation or quantization, to deploy the model more efficiently on resource-constrained devices. Consider scaling the model up (more layers, larger hidden size) with a larger dataset for improved performance, if computational resources allow.

6.  **Integrate More Special Tokens/Structures**: Depending on specific use cases, introduce and train for additional special tokens or structural markers to guide model behavior, similar to the `<think>` tags.

7.  **Human Evaluation**: Beyond automated metrics, conduct human evaluations to assess the quality of generated text, particularly focusing on the coherence and correctness of reasoning responses when `<think>` tokens are involved.
