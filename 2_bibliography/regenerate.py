"""Regenerate every bibliography entry from its publisher export (revision R1.2/R1.8).
  * ACL Anthology papers: the entry is copied verbatim from anthology+abstracts.bib.gz (abstract dropped)
  * other DOIs: BibTeX from doi.org content negotiation (application/x-bibtex)
  * entries with neither (e.g. NeurIPS 2017, a model card) are kept and listed for manual check
Citation keys are preserved so the manuscript does not change.
Usage: python regenerate.py in.bib anthology+abstracts.bib.gz out.bib log.json
"""
import gzip, json, re, sys, time, urllib.request
src, anth, out, logp = sys.argv[1:5]
T = gzip.open(anth, "rt", encoding="utf-8").read()
blocks = {}
for b in re.split(r"\n(?=@)", T):
    m = re.search(r'\n\s*url = "https://aclanthology.org/([^"/]+)/?"', b)
    if m:
        blocks[m.group(1)] = b
s = open(src, encoding="utf-8").read()
ents = [e.strip() for e in re.split(r"\n(?=@)", s) if e.strip().startswith("@")]
pre = s[: s.find("@")]


def field(e, k):
    m = re.search(r"\n\s*" + k + r"\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", e, re.S)
    return " ".join(m.group(1).split()) if m else None


def x_bibtex(doi):
    for i in range(4):
        try:
            req = urllib.request.Request("https://doi.org/" + doi.replace("\\_", "_"),
                                         headers={"Accept": "application/x-bibtex; charset=utf-8",
                                                  "User-Agent": "bibregen (mailto:sm.nihal4@gmail.com)"})
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        except Exception as ex:
            err = str(ex); time.sleep(5 * (i + 1))
    raise RuntimeError(err)


log, outents = [], []
for e in ents:
    key = re.match(r"@\w+\{([^,]+),", e).group(1)
    doi, url = field(e, "doi") or "", field(e, "url") or ""
    acl = None
    m = re.search(r"aclanthology\.org/([^/\s]+)", url) or re.search(r"10\.18653/v1/([^\s}]+)", doi)
    if m:
        acl = m.group(1).rstrip("/")
        # anthology ids are case-sensitive for old ids (e.g. N19-1423, D19-1224)
        acl = next((k for k in blocks if k.lower() == acl.lower()), acl)
    if acl and acl in blocks:
        b = blocks[acl]
        b = re.sub(r"^@(\w+)\{[^,]+,", lambda mm: "@" + mm.group(1) + "{" + key + ",", b.strip())
        b = re.sub(r'\n\s*abstract = ".*?",?\n(?=\s*\w+ =|\})', "\n", b, flags=re.S)
        outents.append(b); log.append({"key": key, "source": "acl-anthology", "id": acl}); continue
    if doi and not doi.startswith("10.48550"):
        try:
            b = x_bibtex(doi).strip()
            b = re.sub(r"^@(\w+)\{[^,]+,", lambda mm: "@" + mm.group(1) + "{" + key + ",", b)
            # keep our url field if publisher export lacks one
            outents.append(b); log.append({"key": key, "source": "doi.org", "id": doi}); time.sleep(1); continue
        except Exception as ex:
            log.append({"key": key, "source": "KEPT (doi fetch failed: %s)" % ex, "id": doi})
    else:
        log.append({"key": key, "source": "KEPT (arXiv/no DOI)", "id": doi or url})
    outents.append(e)
open(out, "w", encoding="utf-8").write(pre + "\n\n".join(outents) + "\n")
json.dump(log, open(logp, "w"), indent=1)
import collections
print(collections.Counter(l["source"].split(" (")[0] for l in log))
for l in log:
    if l["source"].startswith("KEPT"):
        print(" ", l["key"], l["source"], l["id"])
