"""Rubric coding of archived model cards (revision R1.4), with model-family grouping.
Rubric (applied to the archived README at the recorded commit SHA):
  eval_named         1 if the card identifies the evaluation data by name (public benchmark or dataset)
  split_reproducible 1 if every evaluation set is public AND the split is identified (split name,
                     harness task, released test file, or ratio + seed) so the comparison can be rerun
  decontamination    1 if the card states a check of training data against evaluation data, reports an
                     overlap statistic, or states that evaluation items were excluded from training
Cards with no evaluation-bearing text were scored 0 on all three; their keyword scan is in
hf_audit_scored.csv. Codes below were assigned from the archived card text (eval_contexts.txt) and
must be verified by a second, human coder before publication (column human_verified).
Family = author + model-name stem (size, version and training-variant suffixes stripped).
Usage: python code_cards.py hf_audit_scored.csv out_dir
"""
import csv, re, sys, json, collections
EVAL_NAMED_AND_REPRO = {  # repo: (eval_named, split_reproducible, decontamination, evidence)
 "emonHasan01/BanglaGPT-Pro": (1, 0, 0, "hishab benchmark suite named; held-out Bangla-Instruct responses unspecified"),
 "neuropark/sahajBERT": (1, 1, 0, "WikiANN Bengali split; IndicGLUE news category classification"),
 "shihab17/bn-to-en-translation": (1, 0, 0, "kde4 named; model-index lists split: train"),
 "asif00/mbart_bn_error_correction": (1, 0, 0, "BNSECData named; post-training test split unspecified"),
 "ai4bharat/hercule-bn": (1, 1, 0, "evaluated on RECON test set"),
 "ai4bharat/hercule-bn-lora": (1, 1, 0, "evaluated on RECON test set"),
 "SwastikGuhaRoy/AddaGPT2.0": (1, 1, 0, "validation split of ai4bharat/naamapadam"),
 "md-nishat-008/TigerLLM-1B-it": (1, 0, 0, "six benchmarks named (paper Table 2); splits not identified; 500 held-out examples unspecified"),
 "md-nishat-008/TigerLLM-12B-it": (1, 0, 0, "six benchmarks named (paper Table 2); splits not identified"),
 "Polygl0t/LilTii-v0.1": (1, 1, 0, "hishab/bangla-mmlu split: test; harness branch URL"),
 "Polygl0t/LilTii-v0.2": (1, 1, 0, "hishab/bangla-mmlu split: test; harness branch URL"),
 "swapnillo/Bangla-AI-1.7B": (1, 1, 0, "99/1 split, test ratio 0.01, seed 42 on named dataset"),
 "md-nishat-008/TigerCoder-1B": (1, 0, 0, "mHumanEval and MBPP named; Bangla MBPP version/split not identified"),
 "md-nishat-008/TigerCoder-12B": (1, 0, 0, "mHumanEval and MBPP named; Bangla MBPP version/split not identified"),
 "Polygl0t/GigaKriya-ablation-EDU-1.5B": (1, 1, 0, "Polygl0t/ARC-poly split: test; harness URL"),
 "Polygl0t/GigaKriya-ablation-NonEDU-1.5B": (1, 1, 0, "Polygl0t/ARC-poly split: test; harness URL"),
 "spitfire4794/Alo-70m": (1, 0, 0, "harness task names; splits not identified"),
 "nahid-hub/BnLM-F-135m": (1, 1, 0, "BLUGE collection releases evaluation tasks"),
 "nahid-hub/BnLM-C-66m": (1, 1, 0, "BLUGE collection releases evaluation tasks"),
 "AvinabhDutta-Dev/bangla-paraphrase-tigerllm-qlora": (1, 1, 0, "csebuetnlp/BanglaParaphrase split: test"),
 "AvinabhDutta-Dev/bangla-paraphrase-qwen2.5-qlora": (1, 1, 0, "csebuetnlp/BanglaParaphrase split: test"),
 "mdhamidhosen/baamr-math-qwen2.5-1.5b-12k": (1, 1, 1, "held-out test split sharing no template with training (exclusion by construction; borderline)"),
}
PATTERNS = [  # families coded identically from their shared card text
 (r"^hishab/titulm-(llama|gemma)", (1, 0, 0, "lm-eval-harness; named Bangla/English benchmarks incl. private Bangla MMLU")),
 (r"^dipta007/GanitLLM", (1, 1, 0, "Bn-MGSM and Bn-MSVAMP public benchmarks (single test sets)")),
 (r"^dipta007/dagger", (1, 0, 0, "MGSM-derived distractor sets; release not identified")),
]


def family(repo):
    """author + first alphabetic token of the model name (e.g. dipta007/GanitLLM-1.7B_SFT -> dipta007/ganitllm)."""
    a, n = repo.split("/", 1)
    tok = [t for t in re.split(r"[-_.\s\d]+", n) if t]
    return f"{a.lower()}/{(tok[0] if tok else n).lower()}"


def main():
    R = list(csv.DictReader(open(sys.argv[1]))); out = sys.argv[2]
    for r in R:
        code = EVAL_NAMED_AND_REPRO.get(r["repo"])
        if code is None:
            for p, c in PATTERNS:
                if re.search(p, r["repo"]):
                    code = c; break
        code = code or (0, 0, 0, "")
        r["eval_named"], r["split_reproducible"], r["decontamination"], r["rubric_evidence"] = code
        r["family"] = family(r["repo"])
        r["code_linked"] = int(r["code_link_auto"])
    fields = ["repo", "family", "commit_sha", "pipeline", "languages", "downloads_30d", "base_model", "weights_public",
              "tokenizer_shipped", "has_card", "card_chars", "code_linked", "paper_link_auto", "eval_named",
              "split_reproducible", "decontamination", "rubric_evidence", "decontamination_evidence",
              "eval_splits_evidence", "code_link_evidence", "human_verified"]
    with open(f"{out}/hf_audit_final.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(R)
    n = len(R); fam = collections.defaultdict(list)
    for r in R: fam[r["family"]].append(r)
    axes = ["weights_public", "tokenizer_shipped", "code_linked", "eval_named", "split_reproducible", "decontamination"]
    res = {"n_repos": n, "n_families": len(fam), "repo": {}, "family_any": {}}
    for a in axes:
        res["repo"][a] = sum(int(r[a]) for r in R)
        res["family_any"][a] = sum(1 for v in fam.values() if any(int(r[a]) for r in v))
    res["largest_families"] = sorted(((k, len(v)) for k, v in fam.items()), key=lambda x: -x[1])[:8]
    json.dump(res, open(f"{out}/hf_audit_summary.json", "w"), indent=1)
    for a in axes:
        print(f"{a:20s} repos {res['repo'][a]:3d}/{n} ({100*res['repo'][a]/n:5.1f}%)   families {res['family_any'][a]:3d}/{len(fam)} ({100*res['family_any'][a]/len(fam):5.1f}%)")
    print(res["largest_families"])


if __name__ == "__main__":
    main()
