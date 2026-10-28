---
language:
- en
- bn
- multilingual
license: apache-2.0
tags:
- moe
- 3t
- sovereign-ai
- bangladesh
- qwen3.8
- sparse-mixture-of-experts
pipeline_tag: text-generation
---

# 👑 M-3T-Moe (3.004 Trillion Parameters)
### *Bangladesh's First Sovereign 3 Trillion Parameter Sparse Mixture-of-Experts Foundation Model*

- **Lead Architect & Creator:** Md. Mushfiqur Rahim
- **Total Parameters:** 3,004,653,056,000 (~3.0047 Trillion / 3.0T)
- **Active Parameters / Token:** 44,145,520,640 (~44.14 Billion, Top-2 Routing)
- **Base Anchor:** `Qwen/Qwen3.8-27B` (64 Layers: 48 Linear Attention + 16 Full Attention)
- **Number of Experts:** 175 Granular Domain Experts

## 🧮 Mathematical Proof of 3T Scale
- Shared Backbone (Attention, Norms, Embeddings, MTP): 9,920,000,000
- 175 SwiGLU Expert MLPs: 175 * 17,112,760,320 = 2,994,733,056,000
- **Grand Total:** 3,004,653,056,000 Parameters (3.0047 Trillion)!
