---
language:
  - bn
  - en
license: apache-2.0
library_name: transformers
pipeline_tag: text-generation
tags:
  - gpt2
  - causal-lm
  - bilingual
  - bengali
  - bangla
datasets:
  - KothaGPT/bilingual-corpus
---

# KothaGPT Model Collection Update

## 📦 Model Collection Overview

This repository contains the complete collection of KothaGPT bilingual language models and tools for Bangla (Bengali) and English languages. All models have been updated and published to the Hugging Face Hub.

**Last Updated:** January 2026  
**Organization:** KothaGPT  
**License:** Apache 2.0

## 🚀 Available Models

### Core Language Models
- **[bilingual-lm](https://huggingface.co/KothaGPT/bilingual-lm)** - Main bilingual causal language model
- **[literary-lm](https://huggingface.co/KothaGPT/literary-lm)** - Literary text specialized model
- **[tokenizer](https://huggingface.co/KothaGPT/tokenizer)** - Bilingual tokenizer

### Classification Models
- **[readability-classifier](https://huggingface.co/KothaGPT/readability-classifier)** - Text readability assessment
- **[sentiment-tone-classifier](https://huggingface.co/KothaGPT/sentiment-tone-classifier)** - Sentiment and tone analysis
- **[text-complexity-predictor](https://huggingface.co/KothaGPT/text-complexity-predictor)** - Text complexity prediction

### Specialized Models
- **[poetic-meter-detector](https://huggingface.co/KothaGPT/poetic-meter-detector)** - Bengali poetic meter detection
- **[metaphor-simile-detector](https://huggingface.co/KothaGPT/metaphor-simile-detector)** - Literary device detection
- **[named-entity-recognizer](https://huggingface.co/KothaGPT/named-entity-recognizer)** - NER for Bangla/English
- **[cross-lingual-embed](https://huggingface.co/KothaGPT/cross-lingual-embed)** - Cross-lingual embeddings
- **[style-transfer-gpt](https://huggingface.co/KothaGPT/style-transfer-gpt)** - Text style transfer

## 🔄 Update Process

### Automated Publishing
All models are published using the automated script:
```bash
HF_TOKEN=your_token bash scripts/huggingface/publish_all.sh false
```

### Script Features
- **Modern Commands**: Uses `hf upload-large-folder` for better large file handling
- **Error Recovery**: Resumable uploads for large models
- **Validation**: Pre-upload validation checks
- **Progress Tracking**: Detailed progress bars and status reports

## 📊 Model Statistics

| Model | Parameters | Files | Size | Use Case |
|-------|------------|-------|------|----------|
| bilingual-lm | ~125M | 42 | ~500MB | General text generation |
| literary-lm | ~125M | 2 | ~5MB | Literary text analysis |
| readability-classifier | - | 5 | ~2MB | Text assessment |
| sentiment-tone-classifier | - | 2 | ~1MB | Sentiment analysis |
| text-complexity-predictor | - | 1 | ~505KB | Complexity scoring |
| poetic-meter-detector | - | 2 | ~1MB | Poetry analysis |
| metaphor-simile-detector | - | 2 | ~1MB | Literary analysis |
| named-entity-recognizer | - | 2 | ~1MB | Entity extraction |
| cross-lingual-embed | - | 1 | ~1MB | Embeddings |
| style-transfer-gpt | - | 2 | ~1MB | Style transfer |
| tokenizer | - | 2 | ~262KB | Tokenization |

## 🛠️ Usage Examples

### Loading Multiple Models
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load main bilingual model
tokenizer = AutoTokenizer.from_pretrained("KothaGPT/bilingual-lm")
model = AutoModelForCausalLM.from_pretrained("KothaGPT/bilingual-lm")

# Load classifier
classifier = AutoModelForSequenceClassification.from_pretrained("KothaGPT/readability-classifier")
```

### Batch Processing
```python
models = {
    "sentiment": "KothaGPT/sentiment-tone-classifier",
    "readability": "KothaGPT/readability-classifier", 
    "complexity": "KothaGPT/text-complexity-predictor"
}

for task, model_name in models.items():
    # Load and process
    pass
```

## 📈 Performance Metrics

### Language Support
- **Bangla (Bengali)**: Full support with native tokenizer
- **English**: Full support with standard tokenizer
- **Code-switching**: Handles mixed language text

### Benchmark Results
- **Perplexity**: < 25 on bilingual test set
- **Accuracy**: > 85% on classification tasks
- **Inference Speed**: ~50 tokens/second on CPU

## 🔧 Technical Details

### Training Infrastructure
- **Framework**: PyTorch + Transformers
- **Hardware**: GPU training on T4/V100
- **Optimization**: AdamW with cosine scheduling
- **Evaluation**: Comprehensive test suite

### Model Architecture
- **Base**: GPT-2 style transformer
- **Tokenizer**: SentencePiece with bilingual vocabulary
- **Embeddings**: Cross-lingual shared space
- **Layers**: 12 transformer layers, 12 attention heads

## 📚 Documentation

- **[API Reference](docs/api/)** - Complete API documentation
- **[Examples](examples/)** - Usage examples and tutorials
- **[Dataset Cards](cards/dataset_card.md)** - Training dataset information
- **[Individual Model Cards](cards/)** - Detailed model-specific information

## 🤝 Contributing

### Model Updates
1. Train/improve model locally
2. Update model files in `models/` directory
3. Run validation tests
4. Publish with: `bash scripts/huggingface/publish_all.sh false`

### Quality Assurance
- All models pass automated tests
- Manual review of model cards
- Performance benchmarking
- Documentation updates

## 📄 License

All models in this collection are licensed under Apache 2.0. See individual model repositories for specific usage terms.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/KothaGPT/bilingual/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KothaGPT/bilingual/discussions)
- **Documentation**: [Project Docs](https://kothagpt.github.io/bilingual/)

---

**Note**: This collection represents the complete suite of KothaGPT bilingual models. Models are regularly updated with new training data and improved architectures.
