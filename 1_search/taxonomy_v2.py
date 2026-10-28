"""Taxonomy classification v2 (revision R1.2): multi-label, title and title+abstract, corpus and field.
Changes from v1 (title-only, single-label, first match wins):
  * every cell is tested independently (multi-label); a record is 'Representation' if any A-cell fires
  * applied to title alone and to title+abstract, with Cohen's kappa between the two
  * applied to the 157-work corpus and to the field-level sample from the documented search
  * single-label shares are still reported, with the full range over all rule orderings
Usage: python taxonomy_v2.py anthology.json bib coverage_records.json out.json
"""
import json, re, sys, itertools, collections, urllib.request, time
import numpy as np

RULES = collections.OrderedDict([
 ("A1 Orthographic", r"\b(spell\w*|punctuation|error (correction|classification)|grammatical error|normali[sz]\w*|diacritic\w*|grapheme\w*|orthograph\w*|unicode)\b"),
 ("A2 Sub-word", r"(tokeni[sz]\w*|sub-?word|byte-?level|byte[- ]pair|\bbpe\b|vocabular\w*|sentencepiece|wordpiece|fertility|segmentation of words)"),
 ("A3 Morphological", r"\b(stemm\w*|stemmer|lemmati[sz]\w*|morpholog\w*|root[- ]word\w*|inflect\w*|pos[- ]tag\w*|part[- ]of[- ]speech|compound word\w*)\b"),
 ("A4 Cross-script", r"(transliterat\w*|romani[sz]\w*|banglish|code[- ]mix\w*|code[- ]switch\w*|latin script|cross[- ]script)"),
 ("B Resources", r"\b(dataset\w*|corpus|corpora|benchmark\w*|resource\w*|treebank|lexicon|annotated|annotation)\b"),
 ("C Models", r"(language model\w*|\bllms?\b|\bbert\b|banglabert|\bgpt\w*|\bt5\b|pre-?train\w*|\bfine-?tun\w*|adapter\w*|\blora\b|instruction[- ]tun\w*|embedding\w*|encoder\w*|decoder\w*)"),
])
RX = {k: re.compile(v, re.I) for k, v in RULES.items()}
A_CELLS = [k for k in RULES if k.startswith("A")]


def labels(text):
    return {k for k, rx in RX.items() if rx.search(text)}


def single(text, order):
    for k in order:
        if RX[k].search(text):
            return k
    return "D Tasks"


def kappa(a, b):
    a, b = np.array(a), np.array(b); po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in set(a) | set(b))
    return float((po - pe) / (1 - pe)) if pe < 1 else 1.0


def shares(texts):
    n = len(texts); L = [labels(t) for t in texts]
    multi = {k: sum(k in l for l in L) for k in RULES}
    anyA = sum(any(c in l for c in A_CELLS) for l in L)
    order = list(RULES)
    s_pub = collections.Counter(single(t, order) for t in texts)
    rngA = []
    for perm in itertools.permutations(order):
        c = collections.Counter(single(t, perm) for t in texts)
        rngA.append(sum(c[k] for k in A_CELLS))
    return {"n": n, "multi_label_counts": multi, "any_A": anyA, "any_A_pct": 100 * anyA / n,
            "single_label_published_order": dict(s_pub),
            "single_label_A_range": [min(rngA), int(np.median(rngA)), max(rngA)],
            "single_label_A_pct_range": [100 * min(rngA) / n, 100 * float(np.median(rngA)) / n, 100 * max(rngA) / n],
            "n_orderings": len(rngA)}


def main():
    A = json.load(open(sys.argv[1])); bib = open(sys.argv[2], encoding="utf-8").read()
    recs = json.load(open(sys.argv[3]))
    ad = {a["doi"].lower(): a for a in A if a["doi"]}; au = {a["url"].rstrip("/"): a for a in A}
    ents = [e for e in re.split(r"\n(?=@)", bib) if e.strip().startswith("@")]
    corpus = []
    for e in ents:
        k = re.match(r"@\w+\{([^,]+),", e.strip()).group(1)
        t = re.sub(r"[{}\\]", "", re.search(r"\btitle\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", e, re.S).group(1))
        d = re.search(r"\bdoi\s*=\s*[{\"]([^}\"]+)", e); u = re.search(r"\burl\s*=\s*[{\"]([^}\"]+)", e)
        a = ad.get(d.group(1).lower() if d else "") or au.get(u.group(1).rstrip("/") if u else "")
        corpus.append({"key": k, "title": " ".join(t.split()), "abstract": (a or {}).get("abstract", "")})
    out = {"rules": RULES}
    out["corpus_title"] = shares([c["title"] for c in corpus])
    out["corpus_title_abstract"] = shares([c["title"] + " " + c["abstract"] for c in corpus])
    out["corpus_n_with_abstract"] = sum(1 for c in corpus if c["abstract"])
    # agreement title vs title+abstract (single-label, published order; and binary any-A)
    order = list(RULES)
    lt = [single(c["title"], order) for c in corpus]; la = [single(c["title"] + " " + c["abstract"], order) for c in corpus]
    bt = [int(any(x in labels(c["title"]) for x in A_CELLS)) for c in corpus]
    ba = [int(any(x in labels(c["title"] + " " + c["abstract"]) for x in A_CELLS)) for c in corpus]
    out["kappa_title_vs_title_abstract_single"] = kappa(lt, la)
    out["kappa_title_vs_title_abstract_anyA"] = kappa(bt, ba)
    out["agreement_anyA"] = float(np.mean(np.array(bt) == np.array(ba)))
    field = [r for r in recs if r.get("eligible_title")]
    out["field_title"] = shares([r["title"] for r in field])
    out["field_title_not_in_corpus"] = shares([r["title"] for r in field if not r["in_corpus"]])
    json.dump(out, open(sys.argv[4], "w"), indent=1)
    json.dump([{**c, "labels_title": sorted(labels(c["title"])), "labels_title_abstract": sorted(labels(c["title"] + " " + c["abstract"]))} for c in corpus],
              open(sys.argv[4].replace(".json", "_corpus_labels.json"), "w"), indent=0)
    for k in ["corpus_title", "corpus_title_abstract", "field_title", "field_title_not_in_corpus"]:
        s = out[k]
        print(f"{k:28s} n={s['n']:5d} anyA={s['any_A']:4d} ({s['any_A_pct']:.1f}%) single-A range {s['single_label_A_pct_range'][0]:.1f}-{s['single_label_A_pct_range'][2]:.1f}% (median {s['single_label_A_pct_range'][1]:.1f}) multi={s['multi_label_counts']}")
    print("abstracts:", out["corpus_n_with_abstract"], "kappa single", round(out["kappa_title_vs_title_abstract_single"], 3), "kappa anyA", round(out["kappa_title_vs_title_abstract_anyA"], 3), "agree", round(out["agreement_anyA"], 3))


if __name__ == "__main__":
    main()
