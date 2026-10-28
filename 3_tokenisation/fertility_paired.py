"""Paired Bangla-English tokenisation analysis (revision R1.3).

For each tokeniser and each parallel corpus we report
  * corpus-level fertility (tokens / whitespace word) for Bangla and English
  * paired sentence-level token-count ratio r_i = |T(bn_i)| / |T(en_i)|
      - mean, median, IQR, geometric mean, and 95% bootstrap CIs
  * aggregate token ratio sum|T(bn)| / sum|T(en)| with 95% bootstrap CI
  * decomposition: sentence ratio = fertility ratio x word-count ratio
  * unknown-token rate and byte-fallback rate per language
Usage: python fertility_paired.py <data_dir> <out_dir>
"""
import sys, json, hashlib, re, unicodedata
import numpy as np
from transformers import AutoTokenizer

DATA, OUT = sys.argv[1], sys.argv[2]
RNG = np.random.default_rng(20261028)
B = 10000

CORPORA = {
    "FLORES-200 devtest": ("flores200_dataset/devtest/ben_Beng.devtest", "flores200_dataset/devtest/eng_Latn.devtest"),
    "FLORES-200 dev": ("flores200_dataset/dev/ben_Beng.dev", "flores200_dataset/dev/eng_Latn.dev"),
    "NTREX-128": ("ntrex_ben.txt", "ntrex_eng.txt"),
}

# (display name, repo, vocabulary scope, note)
TOKS = [
    ("GPT-2", "openai-community/gpt2", "English-centric (byte-level BPE)", ""),
    ("Mistral-7B", "mistralai/Mistral-7B-v0.1", "English/European-centric", ""),
    ("Llama-2", "NousResearch/Llama-2-7b-hf", "English-centric", "mirror; tokenizer.model sha256 identical to meta-llama/Llama-2-7b-hf"),
    ("mBERT", "bert-base-multilingual-cased", "Multilingual (Wikipedia)", ""),
    ("XGLM-564M", "facebook/xglm-564M", "Multilingual", ""),
    ("XLM-R (base/large)", "xlm-roberta-base", "Multilingual", "base and large share one vocabulary"),
    ("mT5 / Aya-101", "CohereForAI/aya-101", "Multilingual", ""),
    ("BLOOM-560m", "bigscience/bloom-560m", "Multilingual", ""),
    ("Qwen2.5", "Qwen/Qwen2.5-7B", "Multilingual", ""),
    ("Llama-3.2", "unsloth/Llama-3.2-1B", "Multilingual", "mirror of gated meta-llama/Llama-3.2-1B; base of TituLLM and TigerLLM-1B"),
    ("Gemma-2", "unsloth/gemma-2-2b", "Multilingual", "mirror; tokenizer.json sha256 identical to google/gemma-2-2b; base of TigerLLM-9B"),
    ("TigerLLM-1B-it", "md-nishat-008/TigerLLM-1B-it", "Bangla LLM", "released checkpoint is Gemma3ForCausalLM with a 262,144-entry vocabulary"),
    ("TituLLM-1B v2", "hishab/titulm-llama-3.2-1b-v2.0", "Bangla LLM (extended vocabulary)", "Llama-3.2 vocabulary extended from 128,256 to 170,497 entries"),
    ("IndicBERT v2", "ai4bharat/IndicBERTv2-MLM-only", "Indic multilingual", ""),
    ("Sarvam-1", "sarvamai/sarvam-1", "Indic multilingual", ""),
    ("BanglishBERT", "csebuetnlp/banglishbert", "Bangla-English bilingual", ""),
    ("BanglaBERT", "csebuetnlp/banglabert", "Bangla-specific", ""),
    ("BanglaT5", "csebuetnlp/banglat5", "Bangla-specific", ""),
]

BYTE_RE = re.compile(r"^<0x[0-9A-Fa-f]{2}>$")


def load(p):
    with open(f"{DATA}/{p}", encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]


# Primary condition: Unicode NFC. U+09DC/U+09DD/U+09DF are composition exclusions,
# so NFC rewrites them as base + nukta (U+09BC). Several Bangla WordPiece vocabularies
# contain only the decomposed form; on raw FLORES text the precomposed code point is
# out of vocabulary and WordPiece maps the *whole word* to [UNK], deflating token counts.
NORMS = {"NFC": lambda s: unicodedata.normalize("NFC", s), "raw": lambda s: s}


def boot_ci(stat, *arrs):
    n = len(arrs[0]); vals = np.empty(B)
    for b in range(B):
        idx = RNG.integers(0, n, n)
        vals[b] = stat(*[a[idx] for a in arrs])
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def analyse(tok, bn, en):
    unk = tok.unk_token_id
    def enc(texts):
        ids = [tok(t, add_special_tokens=False)["input_ids"] for t in texts]
        n = np.array([len(i) for i in ids], float)
        n_unk = sum(sum(1 for x in i if unk is not None and x == unk) for i in ids)
        n_byte = 0
        try:
            pieces = [tok.convert_ids_to_tokens(i) for i in ids]
            n_byte = sum(sum(1 for p in ps if isinstance(p, str) and BYTE_RE.match(p)) for ps in pieces)
        except Exception:
            pass
        return n, n_unk, n_byte
    tb, ub, bb = enc(bn); te, ue, be = enc(en)
    wb = np.array([len(t.split()) for t in bn], float)
    we = np.array([len(t.split()) for t in en], float)
    r = tb / te
    agg = lambda a, b: a.sum() / b.sum()
    fert_ratio = (tb.sum() / wb.sum()) / (te.sum() / we.sum())
    return {
        "fert_bn": tb.sum() / wb.sum(), "fert_en": te.sum() / we.sum(),
        "fert_ratio": fert_ratio,
        "fert_ratio_ci": boot_ci(lambda a, b, c, d: (a.sum() / c.sum()) / (b.sum() / d.sum()), tb, te, wb, we),
        "word_ratio": wb.sum() / we.sum(),
        "agg_ratio": agg(tb, te), "agg_ratio_ci": boot_ci(agg, tb, te),
        "mean_ratio": r.mean(), "mean_ratio_ci": boot_ci(np.mean, r),
        "median_ratio": float(np.median(r)), "median_ratio_ci": boot_ci(np.median, r),
        "geo_ratio": float(np.exp(np.log(r).mean())),
        "q1": float(np.percentile(r, 25)), "q3": float(np.percentile(r, 75)),
        "p5": float(np.percentile(r, 5)), "p95": float(np.percentile(r, 95)),
        "frac_gt1": float((r > 1).mean()),
        "unk_bn": ub / tb.sum(), "unk_en": ue / te.sum(),
        "byte_bn": bb / tb.sum(), "byte_en": be / te.sum(),
        "n": len(r), "ratios": r.tolist(),
    }


def main():
    corpora = {k: (load(b), load(e)) for k, (b, e) in CORPORA.items()}
    for k, (b, e) in corpora.items():
        assert len(b) == len(e), k
    res = {}
    for name, repo, scope, note in TOKS:
        tok = AutoTokenizer.from_pretrained(repo)
        res[name] = {"repo": repo, "scope": scope, "note": note,
                     "vocab": len(tok), "unk_token": tok.unk_token, "corpora": {}}
        for nname, nf in NORMS.items():
            for cname, (b, e) in corpora.items():
                res[name]["corpora"][f"{cname} | {nname}"] = analyse(tok, [nf(x) for x in b], [nf(x) for x in e])
        d = res[name]["corpora"]["FLORES-200 devtest | NFC"]
        print(f"{name:20s} fert {d['fert_bn']:.2f}/{d['fert_en']:.2f}={d['fert_ratio']:.2f} "
              f"agg {d['agg_ratio']:.2f} [{d['agg_ratio_ci'][0]:.2f},{d['agg_ratio_ci'][1]:.2f}] "
              f"med {d['median_ratio']:.2f} unk {d['unk_bn']*100:.2f}% byte {d['byte_bn']*100:.1f}%", flush=True)
    with open(f"{OUT}/fertility_paired_results.json", "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
