"""S2 (arXiv API) and S3 (Crossref REST API) arms of the documented search.
S2 query string (arXiv API syntax), submitted 2019-01-01..2026-10-28:
  (ti:Bangla OR ti:Bengali OR ti:Banglish OR ti:Sylheti OR ti:Chittagonian OR
   abs:Bangla OR abs:Bengali OR abs:Banglish OR abs:Sylheti OR abs:Chittagonian) AND cat:cs.CL
S3: Crossref /works, query.title=<term> for term in {Bangla, Bengali, Banglish}, filter
  from-pub-date:2019-01-01, until-pub-date:2026-10-28, type:journal-article|proceedings-article,
  deep-paged with a cursor; a record is retained only if the term occurs as a word in the title
  (Crossref title search is relevance-ranked, not boolean, so the regex is the actual criterion).
  NLP-text eligibility: title also matches the NLP term list below.
Usage: python search_arxiv_crossref.py outdir
"""
import json, re, sys, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
OUT = sys.argv[1]
UA = {"User-Agent": "bangla-survey-search (mailto:sm.nihal4@gmail.com)"}
LANG = re.compile(r"\b(bangla|bengali|banglish|sylheti|chittagonian)\b", re.I)
NLP = re.compile(r"\b(language|text\w*|nlp|sentiment|hate|toxic|offensive|abusive|fake news|misinformation|"
                 r"translat\w*|summar\w*|question|qa|token\w*|corpus|corpora|dataset|benchmark|bert|transformer\w*|"
                 r"llms?|gpt|embedding\w*|word\w*|sentence\w*|named entity|ner|parsing|pos tagg\w*|stemm\w*|"
                 r"lemmat\w*|spell\w*|grammar|classification|detection|news|social media|comments?|reviews?|"
                 r"emotion\w*|stance|sarcasm|cyberbully\w*|chatbot|dialog\w*|transliterat\w*|code-mix\w*|romani[sz]ed)\b", re.I)
NONTEXT = re.compile(r"\b(speech|asr|speaker|audio|handwrit\w*|ocr|sign language|bdsl|image|video|character recognition|"
                     r"numeral|digit|license plate|face|eeg|medical image)\b", re.I)


def get(url, tries=5):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
        except Exception as e:
            time.sleep(5 * (i + 1)); err = e
    raise err


def arxiv():
    terms = ["Bangla", "Bengali", "Banglish", "Sylheti", "Chittagonian"]
    q = "(" + " OR ".join([f"ti:{t}" for t in terms] + [f"abs:{t}" for t in terms]) + \
        ") AND cat:cs.CL AND submittedDate:[201901010000 TO 202610282359]"
    ns = {"a": "http://www.w3.org/2005/Atom"}
    recs, start = [], 0
    while True:
        u = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": q, "start": start, "max_results": 500, "sortBy": "submittedDate", "sortOrder": "ascending"})
        root = ET.fromstring(get(u)); es = root.findall("a:entry", ns)
        total = int(root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
        for e in es:
            t = " ".join(e.find("a:title", ns).text.split())
            recs.append({"id": e.find("a:id", ns).text, "title": t, "published": e.find("a:published", ns).text[:10],
                         "doi": (e.find("{http://arxiv.org/schemas/atom}doi").text if e.find("{http://arxiv.org/schemas/atom}doi") is not None else ""),
                         "journal_ref": (e.find("{http://arxiv.org/schemas/atom}journal_ref").text if e.find("{http://arxiv.org/schemas/atom}journal_ref") is not None else ""),
                         "in_title": bool(LANG.search(t))})
        start += len(es)
        if not es or start >= total:
            break
        time.sleep(3.5)
    return q, total, recs


def crossref():
    recs, log = {}, []
    for term in ["Bangla", "Bengali", "Banglish"]:
        cursor, seen, kept, misses = "*", 0, 0, 0
        while True:
            u = "https://api.crossref.org/works?" + urllib.parse.urlencode({
                "query.title": term, "rows": 1000, "cursor": cursor,
                "filter": "from-pub-date:2019-01-01,until-pub-date:2026-10-28,type:journal-article,type:proceedings-article",
                "select": "DOI,title,container-title,issued,type,publisher", "mailto": "sm.nihal4@gmail.com"})
            m = json.loads(get(u))["message"]; items = m["items"]
            if seen == 0:
                log.append({"term": term, "crossref_total_results": m["total-results"]})
            page_kept = 0
            for it in items:
                t = " ".join((it.get("title") or [""])[0].split())
                if re.search(rf"\b{term}\b", t, re.I):
                    page_kept += 1
                    recs[it["DOI"].lower()] = {"doi": it["DOI"].lower(), "title": t,
                        "venue": (it.get("container-title") or [""])[0], "publisher": it.get("publisher", ""),
                        "year": (it.get("issued", {}).get("date-parts", [[None]])[0][0]), "type": it["type"]}
            seen += len(items); kept += page_kept
            misses = misses + 1 if page_kept == 0 else 0
            cursor = m.get("next-cursor")
            # relevance-ranked: stop after two consecutive pages with no title match
            if not items or misses >= 2 or seen >= 20000:
                break
            time.sleep(1)
        log[-1].update({"records_paged": seen, "title_matches": kept})
        print("crossref", log[-1], flush=True)
    return log, list(recs.values())


if __name__ == "__main__":
    q, total, ax = arxiv()
    for r in ax:
        r["eligible_text_nlp"] = bool(NLP.search(r["title"])) and not NONTEXT.search(r["title"])
    json.dump({"query": q, "total": total, "records": ax}, open(f"{OUT}/s2_arxiv.json", "w"), indent=0)
    print("arxiv total", total, "title-hits", sum(r["in_title"] for r in ax))
    log, cr = crossref()
    for r in cr:
        r["eligible_text_nlp"] = bool(NLP.search(r["title"])) and not NONTEXT.search(r["title"])
    json.dump({"log": log, "records": cr}, open(f"{OUT}/s3_crossref.json", "w"), indent=0)
    print("crossref unique", len(cr), "eligible", sum(r["eligible_text_nlp"] for r in cr))
