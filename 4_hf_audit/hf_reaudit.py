"""Auditable re-run of the Hugging Face Hub disclosure audit (revision R1.4).
Sampling frame (deterministic, recorded with the run date):
  1. all models returned by HfApi.list_models(filter="bn")
  2. pipeline_tag in {text-generation, fill-mask, text2text-generation}
  3. Bangla-specific: card metadata lists <= 3 languages including bn, OR the repo id matches
     /bangla|bengali|bangla|\bbn\b|titu|tiger/
  4. excluded as derivative re-packaging: repo id or tags match gguf|gptq|awq|exl2|mlx|bnb|4bit|8bit|
     int4|int8|quant|onnx|openvino, or the repo contains only adapter weights (adapter_config.json, no full weights)
  5. downloads >= 10 in the last 30 days (removes abandoned test uploads); threshold recorded
For every included repo the README is archived at its commit SHA and each disclosure axis is
scored by a documented keyword rule; the matching sentence is stored as evidence so that every
score can be checked and overridden by a human reviewer (column human_verified left blank).
Usage: python hf_reaudit.py out_dir
"""
import json, re, sys, os, time, csv, datetime
from huggingface_hub import HfApi, hf_hub_download
OUT = sys.argv[1]; os.makedirs(f"{OUT}/cards", exist_ok=True)
api = HfApi()
RUN_DATE = datetime.datetime.now(datetime.timezone.utc).isoformat()
PIPES = {"text-generation", "fill-mask", "text2text-generation"}
BN_ID = re.compile(r"(bangla|bengali|bangla|(^|[-_/])bn([-_/]|$)|titu|tiger)", re.I)
QUANT = re.compile(r"(gguf|gptq|awq|exl2|mlx|bnb|4bit|8bit|int4|int8|quant|onnx|openvino)", re.I)
MIN_DL = 10
WEIGHT = re.compile(r"\.(safetensors|bin|pt|pth|h5|msgpack|ckpt)$")
TOKF = re.compile(r"(tokenizer\.json|tokenizer\.model|vocab\.txt|vocab\.json|spiece\.model|sentencepiece\.bpe\.model|merges\.txt)$")
AX = {
 "decontamination": re.compile(r"(decontaminat\w*|contaminat\w*|n-?gram overlap|benchmark (leak|overlap)|"
                               r"(overlap|leak\w*) (with|between) (the )?(test|eval|benchmark)|deduplicat\w* against)", re.I),
 "eval_splits": re.compile(r"(test split|validation split|held[- ]out|train[/ -](val|validation|test)|"
                           r"\b\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{1,2}\b|evaluation (set|split|data)|evaluated on|dev set|test set)", re.I),
 "corpus": re.compile(r"(trained on|pre-?trained on|fine-?tuned on|dataset[s]?:|datasets:|corpus|corpora|training data)", re.I),
 "code_link": re.compile(r"github\.com/[\w.-]+/[\w.-]+", re.I),
 "paper_link": re.compile(r"(arxiv\.org/abs/|aclanthology\.org/|doi\.org/)", re.I),
 "license": re.compile(r"(^|\n)\s*license\s*:", re.I),
}


def sentences(text, rx, k=2):
    sents = re.split(r"(?<=[.!?\n])\s+", text)
    return [s.strip()[:300] for s in sents if rx.search(s)][:k]


def main():
    allm = list(api.list_models(filter="bn", full=True, cardData=True, limit=50000))
    log = {"run_date_utc": RUN_DATE, "n_bn_tagged": len(allm)}
    s2 = [m for m in allm if m.pipeline_tag in PIPES]; log["n_lm_pipelines"] = len(s2)
    rows = []
    for m in s2:
        langs = (m.card_data or {}).get("language") if m.card_data else None
        langs = [langs] if isinstance(langs, str) else (langs or [])
        bn_specific = (0 < len(langs) <= 3 and "bn" in langs) or bool(BN_ID.search(m.id))
        quant = bool(QUANT.search(m.id)) or any(QUANT.search(t) for t in (m.tags or []) if not t.startswith("base_model"))
        rows.append({"repo": m.id, "pipeline": m.pipeline_tag, "languages": ";".join(langs),
                     "bn_specific": bn_specific, "quant_or_repack": quant, "downloads_30d": m.downloads or 0,
                     "likes": m.likes or 0, "created": str(m.created_at)[:10]})
    for r in rows:
        r["include_stage3"] = r["bn_specific"]
        r["include_stage4"] = r["include_stage3"] and not r["quant_or_repack"]
        r["include_stage5"] = r["include_stage4"] and r["downloads_30d"] >= MIN_DL
    log.update({k: sum(r[k] for r in rows) for k in ["include_stage3", "include_stage4", "include_stage5"]})
    audited = []
    for r in [r for r in rows if r["include_stage5"]]:
        try:
            info = api.model_info(r["repo"], files_metadata=False)
        except Exception as e:
            r["error"] = str(e)[:80]; continue
        files = [s.rfilename for s in info.siblings]
        adapter_only = "adapter_config.json" in files and not any(WEIGHT.search(f) and "adapter" not in f for f in files)
        r["adapter_only"] = adapter_only
        if adapter_only:
            r["include_final"] = False; continue
        r["include_final"] = True
        r["commit_sha"] = info.sha
        r["weights_public"] = int(any(WEIGHT.search(f) for f in files) and not info.gated)
        r["gated"] = str(info.gated)
        r["tokenizer_shipped"] = int(any(TOKF.search(f) for f in files))
        card = ""
        if "README.md" in files:
            try:
                p = hf_hub_download(r["repo"], "README.md", revision=info.sha)
                card = open(p, encoding="utf-8", errors="ignore").read()
                safe = r["repo"].replace("/", "__")
                open(f"{OUT}/cards/{safe}@{info.sha[:12]}.md", "w", encoding="utf-8").write(card)
            except Exception as e:
                r["card_error"] = str(e)[:80]
        r["has_card"] = int(len(card.strip()) > 0)
        r["card_chars"] = len(card)
        r["base_model"] = ";".join(t.split(":", 1)[1] for t in (info.tags or []) if t.startswith("base_model:") and t.count(":") == 1)
        for ax, rx in AX.items():
            ev = sentences(card, rx)
            r[f"{ax}_auto"] = int(bool(ev)); r[f"{ax}_evidence"] = " || ".join(ev)
        r["human_verified"] = ""
        audited.append(r)
        time.sleep(0.2)
    log["n_final"] = len(audited)
    with open(f"{OUT}/hf_frame_all.csv", "w", newline="") as f:
        keys = sorted({k for r in rows for k in r}); w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
    with open(f"{OUT}/hf_audit_scored.csv", "w", newline="") as f:
        keys = sorted({k for r in audited for k in r}); w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(audited)
    json.dump(log, open(f"{OUT}/hf_audit_log.json", "w"), indent=1)
    print(json.dumps(log, indent=1))
    n = len(audited)
    for ax in ["weights_public", "tokenizer_shipped", "has_card"] + [f"{a}_auto" for a in AX]:
        k = sum(r.get(ax, 0) for r in audited); print(f"{ax:22s} {k}/{n}")


if __name__ == "__main__":
    main()
