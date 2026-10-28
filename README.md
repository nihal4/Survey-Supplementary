# Reproducibility package: "Representation, Resources, and Reproducibility: A Survey of NLP for Bangla" (revised)

All runs dated 2026-10-28 (UTC+6). Python 3.13; `transformers`, `huggingface_hub` 2.3, `numpy`, `scipy`, `matplotlib`.
Run scripts with `python -I`; each script's docstring gives its usage.

| Folder | What it reproduces | Manuscript |
|---|---|---|
| `1_search/` | Stage-2 documented search (ACL Anthology dump, arXiv API, Crossref API), de-duplication, corpus coverage, multi-label taxonomy v2, flow figure | Table 2, Fig. 1, Table 3, Sec. 2.2, Sec. 4 |
| `2_bibliography/` | Regeneration of every entry from publisher exports, field audit before/after, old-vs-new change log, archived copy of the model card cited as ref. bhaskar1707 | Sec. 2.3 |
| `3_tokenisation/` | Paired sentence-level ratios, bootstrap CIs, UNK and byte-fallback rates; 18 tokenisers x 3 corpora x {NFC, raw} | Table 4, Fig. 4 |
| `4_hf_audit/` | Hub sampling frame (every repo with inclusion decision), archived model cards at commit SHA, rubric codes with evidence, family grouping | Table 7 |
| `5_shared_tasks/` | Paper-by-paper extraction of 66 system papers, rank-percentile analysis, stratified permutation tests, Holm correction | Table 8, Appendix A |
| `6_scorecard/` | Evidence passage behind every cell of the six-model scorecard | Table 6 |

## Data not redistributed
* ACL Anthology export: `https://aclanthology.org/anthology+abstracts.bib.gz` (SHA-256 in `1_search/anthology_sha256.txt`; the anthology changes daily, so use the hash to check you have the same snapshot).
* FLORES-200: `https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz`; NTREX-128: `github.com/MicrosoftTranslator/NTREX` (`NTREX-128/newstest2019-{ref.ben,src.eng}.txt`).
* PDFs of system papers: download from the ACL Anthology URLs in the bibliography.

## Human verification still required
`4_hf_audit/hf_audit_final.csv` and `5_shared_tasks/shared_task_extraction.csv` have codes assigned by one coder from archived text, with evidence columns. The `human_verified` column is for a second coder.
