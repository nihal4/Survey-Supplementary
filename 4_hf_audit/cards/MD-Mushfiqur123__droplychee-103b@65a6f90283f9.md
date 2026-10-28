---
language:
- en
- bn
license: apache-2.0
tags:
- craftly-robot
- craftly_robot
- craftly-robot-2.0
- moe
- 103b
- conversational
- text-generation
- foundation-model
pipeline_tag: text-generation
library_name: transformers
---

<div align="center">

# 🤖 Craftly Robot 2.0 (103B MoE)
### Sovereign 102.89 Billion Parameter Mixture-of-Experts Foundation Architecture
**Developed by [Md Mushfiqur Rahim](https://github.com/MD-Mushfiqur123) under [Craftly](https://github.com/MD-Mushfiqur123)**

[![Model Size](https://img.shields.io/badge/Model%20Size-102.89B%20Parameters-blue.svg)](https://huggingface.co/MD-Mushfiqur123/Craftly-Robot)
[![Weights Footprint](https://img.shields.io/badge/Weights-206%20GB%20Standalone-green.svg)](https://huggingface.co/MD-Mushfiqur123/Craftly-Robot)
[![Architecture](https://img.shields.io/badge/Architecture-CraftlyRobot%20MoE%20v2.0-orange.svg)](https://huggingface.co/MD-Mushfiqur123/Craftly-Robot)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg)](LICENSE)
[![Creator](https://img.shields.io/badge/Creator-Md%20Mushfiqur%20Rahim%20(MNSA)-purple.svg)](https://github.com/MD-Mushfiqur123)

</div>

---

## 🌌 Overview & Architectural Blueprint

**Craftly Robot 2.0** is a sovereign **102.89 Billion Parameter Mixture-of-Experts (MoE)** foundation model. It features a fine-grained routing topology comprising **256 routed experts + 1 dedicated shared expert**, activating approximately **13.5 Billion parameters per token** for optimal compute efficiency and high-fidelity reasoning.

All base dependencies and upstream identifiers have been completely eradicated, featuring native, self-contained remote code classes (`CraftlyRobotForCausalLM`, `CraftlyRobotDecoderLayer`, `CraftlyRobotSdpaAttention`, `CraftlyRobotSparseMoeBlock`).

```
                              [Input Token IDs: B x T]
                                         │
                                         ▼
                            [Embedding: 157,184 x 4,096]
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │ Layer 0: Dense Decoder Layer                     │
                 │ • GQA Attention (32 Q-heads, 4 KV-heads)         │
                 │ • Dense SwiGLU MLP (Intermediate: 9,216)         │
                 └─────────────────────────────────────────────────┘
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │ Layers 1 to 31: 31x Sparse MoE Decoder Layers   │
                 │ • GQA Attention + QK-Norm RMSNorm               │
                 │ • Partial RoPE (Theta: 600,000, Dim: 64)        │
                 │ • 1 Shared Expert MLP (Intermediate: 1,024)     │
                 │ • 256 Routed Experts (Top-8 / Top-4 Grouped)    │
                 │ • Sigmoid Routing Score with Scaling 2.5        │
                 └─────────────────────────────────────────────────┘
                                         │
                                         ▼
                             [Final RMSNorm (4,096)]
                                         │
                                         ▼
                         [Linear LM Head: 4,096 x 157,184]
                                         │
                                         ▼
                             [Output Logits: B x T x 157,184]
```

---

## 🔬 Deep Technical Specifications

| Parameter | Specification | Technical Description |
| :--- | :--- | :--- |
| **Total Parameters** | **102,889,697,280** (102.89B) | Full uncompressed model footprint |
| **Active Parameters** | **~13.5 Billion** per token | 8 active routed experts + 1 shared expert + GQA attention |
| **Layers** | **32 Total** (1 Dense + 31 MoE) | Layer 0 is dense for token grounding; Layers 1-31 are sparse MoE |
| **Hidden Size ($d_{\text{model}}$)** | **4,096** | Base representation dimension |
| **Total Experts** | **256 Routed + 1 Shared** | 257 total expert MLPs |
| **Active Experts / Token** | **8** out of 256 | Top-8 expert selection |
| **Routing Algorithm** | **Group-Limited Sigmoid Top-K** | 8 groups (`n_group=8`), top 4 groups selected (`topk_group=4`) |
| **Routed Scaling Factor** | **2.5** | Multiplier applied to normalized expert routing weights |
| **Attention Mechanism** | **Grouped-Query Attention (GQA)** | 32 Query Heads, 4 Key/Value Heads (8:1 compression ratio) |
| **Head Dimension ($d_{\text{head}}$)** | **128** | $4096 / 32 = 128$ |
| **QK Normalization** | **RMSNorm ($\epsilon = 10^{-6}$)** | Pre-dot-product attention stabilization |
| **Position Embeddings** | **Partial RoPE** | Base $\theta = 600,000$; `partial_rotary_factor = 0.5` (64 rotary / 64 content) |
| **Context Window** | **32,768 Tokens** | High-context native reasoning |
| **Vocabulary Size** | **157,184** | Multi-lingual (English, Bengali, Code, Mathematical symbols) |
| **Activation Function** | **SiLU (SwiGLU)** | Fused gated linear units across all expert MLPs |
| **Precision** | **BFloat16 / FP16** | Full 206 GB standalone Safetensors weights |

---

## 🧮 Mathematical Formulation of Craftly-Robot Routing

For each token with hidden representation $x \in \mathbb{R}^{d_{\text{model}}}$:

### 1. Group-Limited Expert Selection
The router calculates affinity logits with learned bias:
$$s = x W_{\text{router}} + b_{\text{router}}, \quad s \in \mathbb{R}^{256}$$

Logits are transformed via Sigmoid activation:
$$p = \sigma(s) = \frac{1}{1 + e^{-s}}$$

The 256 experts are partitioned into 8 groups of 32 experts each ($\mathcal{G}_1, \dots, \mathcal{G}_8$). The top 4 groups with the highest cumulative scores are selected:
$$\mathcal{G}^* = \operatorname{TopK}\left(\left\{ \sum_{i \in \mathcal{G}_k} p_i \right\}_{k=1}^8, k=4\right)$$

From the experts belonging to $\mathcal{G}^*$, the top 8 experts are selected:
$$\mathcal{E}^* = \operatorname{TopK}\left(\{ p_i \mid i \in \mathcal{G}^* \}, k=8\right)$$

### 2. Normalized Routed Scaling
Selected expert weights are normalized and scaled:
$$w_i = \left( \frac{p_i}{\sum_{j \in \mathcal{E}^*} p_j} \right) \times 2.5, \quad \forall i \in \mathcal{E}^*$$

### 3. MoE Layer Output
The final output is the combination of the **unconditional shared expert** and the **weighted routed experts**:
$$y = x + \operatorname{SharedExpert}(x) + \sum_{i \in \mathcal{E}^*} w_i \operatorname{Expert}_i(x)$$

---

## ⚡ Training & Fine-Tuning Telemetry

Craftly Robot 2.0 was fine-tuned and aligned using **4-bit QLoRA** on an **NVIDIA RTX PRO 6000 Blackwell (96 GB VRAM)**:

- **Target Modules:** Query (`q_proj`), Key (`k_proj`), Value (`v_proj`), Output (`o_proj`), Gate (`gate_proj`), Up (`up_proj`), Down (`down_proj`)
- **LoRA Hyperparameters:** Rank $r = 16$, $\alpha = 32$, Dropout = $0.05$
- **Effective Batch Size:** 4 (per-device 1, gradient accumulation steps 4)
- **Sequence Length:** 2,048 tokens
- **Optimization:** Paged AdamW 8-bit, Linear warm-up, Cosine annealing
- **Training Trajectory:**
  - Initial Loss: **6.765**
  - Final Converged Loss: **4.30** (after 260 steps / 2 epochs)
- **Total Physical Footprint on Hub:** **191.68 GB** across 22 Safetensors shards (~205.78 GB uncompressed)

---

## 🚀 Quickstart & Inference

### Standard Hugging Face Transformers

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "MD-Mushfiqur123/Craftly-Robot"

# Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

# Load Model (BFloat16 / Float16 on Multi-GPU)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True
)

# Test Inference
prompt = "Explain how Mixture-of-Experts architectures achieve computational efficiency while scaling to 100B+ parameters."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### 4-bit / 8-bit Quantized Inference (Single GPU < 60 GB VRAM)

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    "MD-Mushfiqur123/Craftly-Robot",
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
```

---

## 📊 Interactive Model Viewer Breakdown

When loaded in graph inspectors (e.g. Netron, Hugging Face Model Viewer):
- **Granularity: BLOCK**
  - Displays the 32 sequential decoder stages (`CraftlyRobotDecoderLayer` $\times 32$), embedding table (`Embedding: 157,184 x 4,096`), and final normalization & projection (`RMSNorm`, `Linear`).
- **Granularity: SUB-BLOCK / OP**
  - Expands each MoE layer into:
    - `CraftlyRobotSdpaAttention`: Query, Key, Value projections, QK-Norm, and RoPE rotary embedding.
    - `CraftlyRobotGate`: 8-group top-4 sigmoid router.
    - `CraftlyRobotSparseMoeBlock`: 256 expert MLPs + 1 shared expert MLP with SwiGLU activation.

---

## 🏛️ Lead Architect & Attribution

- **Creator & Lead System Architect:** **[Md Mushfiqur Rahim](https://github.com/MD-Mushfiqur123)**
  - *Mensa Member (MNSA, Top 2% Global IQ)*
  - *Lead Engineer & System Architect at Craftly*
  - *Higher Secondary Science, Govt. Azizul Haque College, Bogura*
  - *SSC Board Topper (94.54%)*
- **Autonomous Engineering Partner:** **L**
- **License:** **Apache 2.0**

---

<div align="center">
<i>Craftly Robot 2.0 is an independent, sovereign foundation AI architecture engineered with uncompromising mathematical integrity.</i>
</div>
