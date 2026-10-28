"""Merge the three search arms, de-duplicate, and measure how the 157-work corpus covers them.
Eligibility (title-level, documented): Bangla term in title AND text-NLP term in title AND no
speech/OCR/vision term in title (same lists as search_arxiv_crossref.py). Abstract-only ACL hits
(multilingual papers mentioning Bangla) are counted separately because the inclusion criterion
requires separately reported Bangla results, which cannot be judged from an abstract.
Usage: python coverage.py <search_dir> <bib> out.json
"""
import json, re, sys, collections
D, BIB, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, D)
NLP = re.compile(r"\b(language|text\w*|nlp|sentiment|hate|toxic|offensive|abusive|fake news|misinformation|"
                 r"translat\w*|summar\w*|question|qa|token\w*|corpus|corpora|dataset|benchmark|bert|transformer\w*|"
                 r"llms?|gpt|embedding\w*|word\w*|sentence\w*|named entity|ner|parsing|pos tagg\w*|stemm\w*|"
                 r"lemmat\w*|spell\w*|grammar|classification|detection|news|social media|comments?|reviews?|"
                 r"emotion\w*|stance|sarcasm|cyberbully\w*|chatbot|dialog\w*|transliterat\w*|code-mix\w*|romani[sz]ed)\b", re.I)
NONTEXT = re.compile(r"\b(speech|asr|speaker|audio|handwrit\w*|ocr|sign language|bdsl|image|video|character recognition|"
                     r"numeral|digit|license plate|face|eeg|medical image)\b", re.I)
LANG = re.compile(r"\b(bangla|bengali|banglish|sylheti|chittagonian|chakma)\b", re.I)


def norm(t):
    return re.sub(r"[^a-z0-9]", "", re.sub(r"[{}\\]", "", t.lower()))[:80]


def elig(t):
    return bool(LANG.search(t)) and bool(NLP.search(t)) and not NONTEXT.search(t)


s1 = json.load(open(f"{D}/s1_acl_hits.json")); s2 = json.load(open(f"{D}/s2_arxiv.json")); s3 = json.load(open(f"{D}/s3_crossref.json"))
recs = {}
def add(src, title, doi, year, venue, extra=None):
    k = doi.lower() if doi else "t:" + norm(title)
    tk = "t:" + norm(title)
    # merge by doi or by normalised title
    key = k if k in recs else (tk if tk in recs else None)
    if key is None:
        for kk, v in recs.items():
            if v["ntitle"] == norm(title):
                key = kk; break
    if key is None:
        key = k; recs[key] = {"title": title, "ntitle": norm(title), "doi": doi.lower() if doi else "", "year": year,
                              "venue": venue, "sources": set(), "abstract_only": False}
    recs[key]["sources"].add(src)
    if extra: recs[key].update(extra)
for h in s1:
    add("ACL", h["title"], h["doi"], h["year"], h["booktitle"], {"abstract_only": h["in_abstract_only"]} if h["in_abstract_only"] else None)
for r in s2["records"]:
    add("arXiv", r["title"], r["doi"], r["published"][:4], "arXiv")
for r in s3["records"]:
    add("Crossref", r["title"], r["doi"], r["year"], r["venue"])
# corpus
s = open(BIB, encoding="utf-8").read()
ents = [e for e in re.split(r"\n(?=@)", s) if e.strip().startswith("@")]
corpus = {}
for e in ents:
    k = re.match(r"@\w+\{([^,]+),", e.strip()).group(1)
    d = re.search(r"\bdoi\s*=\s*[{\"]([^}\"]+)", e); t = re.search(r"\btitle\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", e, re.S)
    corpus[k] = {"doi": d.group(1).lower().replace("\\_", "_") if d else "", "ntitle": norm(t.group(1)), "title": re.sub(r"[{}]", "", t.group(1))}
cd = {v["doi"] for v in corpus.values() if v["doi"]}; ct = {v["ntitle"] for v in corpus.values()}
for v in recs.values():
    v["in_corpus"] = (v["doi"] in cd) or (v["ntitle"] in ct)
    v["eligible_title"] = elig(v["title"])
    v["sources"] = sorted(v["sources"])
corpus_bangla = {k: v for k, v in corpus.items() if LANG.search(v["title"])}
found = [k for k, v in corpus_bangla.items() if any(r["in_corpus"] and (r["doi"] == v["doi"] or r["ntitle"] == v["ntitle"]) for r in recs.values())]
E = [v for v in recs.values() if v["eligible_title"]]
out = {
 "unique_records": len(recs),
 "by_source": collections.Counter("+".join(v["sources"]) for v in recs.values()),
 "eligible_by_title_rule": len(E),
 "eligible_in_corpus": sum(v["in_corpus"] for v in E),
 "eligible_not_in_corpus": sum(not v["in_corpus"] for v in E),
 "eligible_not_in_corpus_by_source": collections.Counter("+".join(v["sources"]) for v in E if not v["in_corpus"]),
 "eligible_not_in_corpus_by_year": dict(sorted(collections.Counter(str(v["year"]) for v in E if not v["in_corpus"]).items())),
 "acl_abstract_only_hits": sum(v["abstract_only"] for v in recs.values()),
 "corpus_entries": len(corpus), "corpus_entries_with_bangla_title": len(corpus_bangla),
 "corpus_bangla_title_retrieved_by_search": len(found),
 "corpus_bangla_title_missed": [corpus_bangla[k]["title"] for k in corpus_bangla if k not in found],
}
# publisher breakdown for Crossref-only eligible-not-in-corpus
pub = collections.Counter()
for v in E:
    if not v["in_corpus"] and v["sources"] == ["Crossref"]:
        pub[(v.get("venue") or "")[:40]] += 1
out["crossref_only_missing_top_venues"] = pub.most_common(15)
json.dump(out, open(OUT, "w"), indent=1, default=list)
json.dump(sorted([{k: (sorted(x) if isinstance(x, set) else x) for k, x in v.items()} for v in recs.values()], key=lambda r: (str(r["year"]), r["title"])),
          open(OUT.replace(".json", "_records.json"), "w"), indent=0)
print(json.dumps(out, indent=1, default=list))
