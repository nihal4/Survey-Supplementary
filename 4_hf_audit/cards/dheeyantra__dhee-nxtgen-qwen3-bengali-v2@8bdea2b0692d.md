---
language: bn
license: apache-2.0
tags:
  - causal-lm
  - assistant
  - reasoning
  - bengali
model_name: dhee-nxtgen-qwen3-bengali-v2
library_name: transformers
---

# Dhee-NxtGen-Qwen3-Bengali-v2

## Model Description
**Dhee-NxtGen-Qwen3-Bengali-v2** is a large language model designed for natural and fluent Bengali (Bangla) understanding and generation.  
Built upon the **Qwen3** architecture, this model is optimized for **assistant-style dialogue**, **function-calling tasks**, and **reasoning-oriented responses**.

It is part of DheeYantra’s multilingual initiative in collaboration with **NxtGen Cloud Technologies Private Limited**, focusing on building domain-adapted Indic LLMs.

## Key Features
- Fluent, context-aware Bengali text generation  
- Fine-tuned for assistant-style interactions and reasoning tasks  
- Handles open-domain question answering, summarization, and dialogue  
- Fully compatible with 🤗 Hugging Face Transformers  
- Optimized for VLLM serving for high-performance inference  

## Example Usage
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "dheeyantra/dhee-nxtgen-qwen3-bengali-v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# Qwen3-compatible formatted prompt
prompt = """<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
তুমি কি আমার জন্য একটি অ্যাপয়েন্টমেন্ট নির্ধারণ করতে পারবে?<|im_end|>
<|im_start|>assistant
"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=150)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Intended Uses & Limitations
### Intended Uses
- Bengali conversational chatbots and assistants  
- Function-calling and structured response generation  
- Story generation and summarization in Bengali  
- Natural dialogue systems for Indic AI applications  

### Limitations
- May generate inaccurate or biased responses in rare cases  
- Performance can vary on out-of-domain or code-mixed inputs  
- Primarily optimized for Bengali; other languages may produce less fluent results  

## VLLM / High-Performance Serving Requirements
For high-throughput serving with **vLLM**, ensure the following environment:

- GPU with compute capability ≥ 8.0 (e.g., NVIDIA A100)  
- PyTorch 2.1+ and CUDA toolkit installed  
- For V100 GPUs (sm70), vLLM GPU inference is not supported; CPU fallback is possible but slower.  

Install dependencies:
```bash
pip install torch transformers vllm sentencepiece
```

Run vLLM server:
```bash
vllm serve   --model dheeyantra/dhee-nxtgen-qwen3-bengali-v2   --host 0.0.0.0   --port 8000
```

## License
Released under the **Apache 2.0 License**.

---
*Developed by DheeYantra in collaboration with NxtGen Cloud Technologies Pvt. Ltd.*
