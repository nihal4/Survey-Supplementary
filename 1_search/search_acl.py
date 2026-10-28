"""S1: exhaustive search of the ACL Anthology dump (anthology+abstracts.bib.gz).
Query (case-insensitive, word-boundary) on title OR abstract:
  LANG  = Bangla | Bengali | Banglish | Sylheti | Chittagonian | Chakma | Bangladesh(i)
Year window 2019-2026. Output: hits with matched field, and an NLP-text eligibility flag
(speech/OCR/sign-language-only records flagged as out of scope by title rule).
Usage: python search_acl.py anthology.json out.json
"""
import json, re, sys
A = json.load(open(sys.argv[1]))
LANG = re.compile(r"\b(bangla|bengali|banglish|sylheti|chittagonian|chakma|bangladesh(i)?)\b", re.I)
OUT_OF_SCOPE = re.compile(r"\b(speech|asr|speaker|audio|handwrit\w*|ocr|sign language|bdsl|grapheme recognition|image caption\w*)\b", re.I)
hits = []
for a in A:
    try:
        y = int(a["year"])
    except ValueError:
        continue
    if not 2019 <= y <= 2026:
        continue
    t, ab = a["title"], a["abstract"]
    in_t, in_a = bool(LANG.search(t)), bool(LANG.search(ab))
    if not (in_t or in_a):
        continue
    hits.append({**{k: a[k] for k in ("key", "title", "year", "url", "doi", "booktitle")},
                 "in_title": in_t, "in_abstract_only": (not in_t) and in_a,
                 "speech_ocr_title": bool(OUT_OF_SCOPE.search(t)),
                 "blp_workshop": "banglalp" in a["url"]})
json.dump(hits, open(sys.argv[2], "w"), indent=0)
print("records 2019-2026 in dump:", sum(1 for a in A if a["year"].isdigit() and 2019 <= int(a["year"]) <= 2026))
print("hits:", len(hits), "| title:", sum(h["in_title"] for h in hits), "| abstract-only:", sum(h["in_abstract_only"] for h in hits))
print("BLP workshop:", sum(h["blp_workshop"] for h in hits), "| speech/OCR by title:", sum(h["speech_ocr_title"] for h in hits))
