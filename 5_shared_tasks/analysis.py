"""Quantitative synthesis of the BLP shared-task extraction (revision R1.5).
Outcome: official rank converted to a within-task percentile p = (team_rank-1)/(n_teams-1),
0 = best. Baseline rows in printed leaderboards are removed before ranking.
For each binary design factor: n with/without, median percentile, Cliff's delta,
two-sided Mann-Whitney U p-value (pooled), and a stratified permutation test that permutes the
factor *within task* (10,000 permutations) so task difficulty cannot drive the result.
Usage: python analysis.py shared_task_extraction.json out.json
"""
import json, sys
import numpy as np
from scipy.stats import mannwhitneyu, spearmanr

rng = np.random.default_rng(20261028)
R = json.load(open(sys.argv[1]))
BASELINE_ROWS = {"2023-T2": [25, 29], "2025-T1": [35, 37], "2025-T2": [29]}


def team_rank(r):
    return r["rank_official"] - sum(1 for b in BASELINE_ROWS.get(r["task"], []) if b < r["rank_official"])


for r in R:
    r["pct"] = (team_rank(r) - 1) / (r["n_teams"] - 1)


def cliffs(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(((a[:, None] < b[None, :]).sum() - (a[:, None] > b[None, :]).sum()) / (len(a) * len(b)))


def strat_perm(rows, f, B=10000):
    tasks = sorted(set(r["task"] for r in rows))
    x = np.array([r[f] for r in rows]); p = np.array([r["pct"] for r in rows])
    groups = [np.where(np.array([r["task"] for r in rows]) == t)[0] for t in tasks]
    obs = p[x == 1].mean() - p[x == 0].mean(); cnt = 0
    for _ in range(B):
        xs = x.copy()
        for g in groups:
            xs[g] = rng.permutation(xs[g])
        d = p[xs == 1].mean() - p[xs == 0].mean()
        cnt += abs(d) >= abs(obs) - 1e-12
    return float(obs), (cnt + 1) / (B + 1)


def factor(rows, f, label):
    rows = [r for r in rows if r[f] in (0, 1)]
    a = [r["pct"] for r in rows if r[f] == 1]; b = [r["pct"] for r in rows if r[f] == 0]
    if len(a) < 2 or len(b) < 2:
        return None
    u = mannwhitneyu(a, b, alternative="two-sided")
    d, pp = strat_perm(rows, f)
    return {"factor": label, "n_with": len(a), "n_without": len(b),
            "median_pct_with": float(np.median(a)), "median_pct_without": float(np.median(b)),
            "cliffs_delta": cliffs(a, b), "mw_p": float(u.pvalue),
            "mean_pct_diff": d, "stratified_perm_p": pp,
            "tasks": sorted(set(r["task"] for r in rows))}


out = {"coverage": {}, "classification": [], "code": [], "per_task": {}}
for t in ["2023-T1", "2023-T2", "2025-T1", "2025-T2"]:
    rs = [r for r in R if r["task"] == t]
    out["coverage"][t] = {"papers": len(rs), "teams": rs[0]["n_teams"],
                          "top_quartile_with_paper": sum(1 for r in rs if r["pct"] <= 0.25)}
cls = [r for r in R if r["task"] != "2025-T2"]
for r in cls:
    r["lexical"] = int("classical" in r["backbone"].lower())
    r["bangla_encoder"] = int(any(s in r["backbone"] for s in ["BanglaBERT", "Bangla-ELECTRA", "Hierarchical-BERT"]))
for f, lab in [("ensemble", "Ensemble"), ("external_data", "External training data"),
               ("augmentation", "Data augmentation"), ("hierarchical", "Hierarchical / two-stage"),
               ("lexical", "Lexical / classical features only"), ("bangla_encoder", "Bangla-specific encoder")]:
    res = factor(cls, f, lab)
    if res: out["classification"].append(res)
t25 = [r for r in cls if r["task"] == "2025-T1"]
for f, lab in [("multitask", "Multi-task learning (2025 T1 only)"), ("decoder_llm", "Decoder LLM (2025 T1 only)")]:
    res = factor(t25, f, lab)
    if res: out["classification"].append(res)
code = [r for r in R if r["task"] == "2025-T2"]
for f, lab in [("exec_feedback", "Unit-test execution feedback"), ("proprietary", "Proprietary model"),
               ("translation", "Translate to English first"), ("finetuned", "Task fine-tuning")]:
    res = factor(code, f, lab)
    if res: out["code"].append(res)
# per-task adoption counts
for t in ["2023-T1", "2023-T2", "2025-T1"]:
    rs = [r for r in cls if r["task"] == t]
    out["per_task"][t] = {f: sum(r[f] for r in rs) for f in ["ensemble", "multitask", "external_data", "augmentation", "hierarchical", "decoder_llm", "lexical"]}
    out["per_task"][t]["n"] = len(rs)
rs = code
out["per_task"]["2025-T2"] = {f: sum(r[f] for r in rs) for f in ["exec_feedback", "proprietary", "translation", "finetuned"]}
out["per_task"]["2025-T2"]["n"] = len(rs)
# size vs rank among open models (classification and code separately)
for name, rows in [("classification", cls), ("code_open", [r for r in code if r["params_B"]])]:
    xs = [(r["params_B"], r["pct"]) for r in rows if r["params_B"]]
    rho = spearmanr([x for x, _ in xs], [y for _, y in xs])
    out[f"size_spearman_{name}"] = {"n": len(xs), "rho": float(rho.statistic), "p": float(rho.pvalue)}
# score spread among top-10 in 2025 T1 (how separable are ranks?)
t1 = sorted([r["score_official"] for r in t25])
out["2025T1_top10_paper_score_range"] = [min(r["score_official"] for r in t25 if r["rank_official"] <= 10),
                                        max(r["score_official"] for r in t25 if r["rank_official"] <= 10)]
json.dump(out, open(sys.argv[2], "w"), indent=1)
for k in ["classification", "code"]:
    for x in out[k]:
        print(f"{x['factor']:38s} {x['n_with']:>2}/{x['n_without']:<2} med {x['median_pct_with']:.2f} vs {x['median_pct_without']:.2f} "
              f"delta={x['cliffs_delta']:+.2f} MW p={x['mw_p']:.3f} strat-perm p={x['stratified_perm_p']:.3f}")
print(json.dumps(out["coverage"])); print(json.dumps(out["per_task"]))
print({k: v for k, v in out.items() if k.startswith("size") or k.startswith("2025T1")})
