"""Field-level audit of every bib entry against its DOI record (revision R1.2/R1.8).
Compares: author count, each author's family name (order-sensitive), year, pages.
Usage: python audit_fields.py file.bib out.json
"""
import json, re, sys, time, urllib.request, unicodedata
s = open(sys.argv[1], encoding="utf-8").read()
ents = [e for e in re.split(r"\n(?=@)", s) if e.strip().startswith("@")]


def field(e, k):
    m = re.search(r"\n\s*" + k + r"\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n", e, re.S)
    return " ".join(m.group(1).split()) if m else None


def fold(x):
    x = re.sub(r"\\[`'^\"~=.uvHcdbtk]\{?(\w)\}?", r"\1", x or "")
    x = re.sub(r"[{}\\]", "", x)
    return unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower().strip()


def get(doi):
    for i in range(4):
        try:
            req = urllib.request.Request("https://doi.org/" + doi.replace("\\_", "_"), headers={
                "Accept": "application/vnd.citationstyles.csl+json", "User-Agent": "bibaudit (mailto:sm.nihal4@gmail.com)"})
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception as ex:
            time.sleep(4 * (i + 1)); err = str(ex)
    return {"err": err}


out = []
for e in ents:
    key = re.match(r"@\w+\{([^,]+),", e.strip()).group(1)
    doi = field(e, "doi")
    if not doi:
        out.append({"key": key, "status": "no-doi"}); continue
    d = get(doi); time.sleep(0.8)
    if "err" in d:
        out.append({"key": key, "status": "error " + d["err"]}); continue
    bib_auth = [fold(a.split(",")[0]) for a in re.split(r"\s+and\s+", field(e, "author") or "") if a.strip()]
    rec_auth = [fold(a.get("family") or a.get("literal") or "") for a in d.get("author", [])]
    issues = []
    if "others" in bib_auth:
        issues.append(f"truncated author list ('and others'); record has {len(rec_auth)}")
        bib_auth = [a for a in bib_auth if a != "others"]
    elif rec_auth and len(bib_auth) != len(rec_auth):
        issues.append(f"author count {len(bib_auth)} vs record {len(rec_auth)}")
    for i, (a, b) in enumerate(zip(bib_auth, rec_auth)):
        if a and b and a.split()[-1] not in b and b.split()[-1] not in a:
            issues.append(f"author {i+1}: bib '{a}' vs record '{b}'")
    yr = (d.get("issued", {}).get("date-parts", [[None]])[0][0])
    if field(e, "year") and yr and str(yr) != field(e, "year"):
        issues.append(f"year {field(e, 'year')} vs record {yr}")
    pg = d.get("page"); bp = field(e, "pages")
    if pg and bp and re.sub(r"-+", "-", bp) != pg:
        issues.append(f"pages {bp} vs record {pg}")
    if pg and not bp:
        issues.append(f"pages missing (record {pg})")
    out.append({"key": key, "status": "ok" if not issues else "check", "issues": issues,
                "record_authors": [f"{a.get('family','')}, {a.get('given','')}" for a in d.get("author", [])],
                "record_year": yr, "record_pages": pg, "record_venue": d.get("container-title")})
json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
for o in out:
    if o["status"] != "ok":
        print(o["key"], "|", o["status"], "|", "; ".join(o.get("issues", []))[:300])
print(sum(o["status"] == "ok" for o in out), "ok of", len(out))
