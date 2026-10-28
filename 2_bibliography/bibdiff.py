"""Per-entry differences between the submitted and revised bibliographies."""
import re, sys, csv, unicodedata
def parse(p):
    s=open(p,encoding="utf-8").read(); D={}
    for e in re.split(r"\n(?=@)",s):
        m=re.match(r"\s*@(\w+)\{([^,]+),",e)
        if not m: continue
        f={}
        for k in ["title","author","year","pages","booktitle","journal","doi","volume"]:
            mm=re.search(r"\b"+k+r"\s*=\s*(\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|(\d+))",e,re.I)
            if mm: f[k]=" ".join((mm.group(2) or mm.group(3) or mm.group(4) or "").split())
        f["type"]=m.group(1).lower(); D[m.group(2)]=f
    return D
def n(x): x=re.sub(r"[{}\\'`\"~^.]","",x or "").lower(); x=unicodedata.normalize("NFKD",x).encode("ascii","ignore").decode(); return re.sub(r"[^a-z0-9]","",x.replace("--","-"))
def fam(a): return [n(x.split(",")[0] if "," in x else x.split()[-1]) for x in re.split(r"\s+and\s+",a or "") if x.strip()]
O,N=parse(sys.argv[1]),parse(sys.argv[2]); rows=[]
for k in N:
    if k not in O: rows.append({"key":k,"change":"added","detail":N[k].get("title","")[:90]}); continue
    o,v=O[k],N[k]; ch=[]
    if n(o.get("title"))!=n(v.get("title")): ch.append(f"title: '{o.get('title','')[:60]}' -> '{v.get('title','')[:60]}'")
    fo,fv=fam(o.get("author")),fam(v.get("author"))
    if fo!=fv: ch.append(f"authors: {len(fo)} -> {len(fv)} ({', '.join(fo[:3])}... -> {', '.join(fv[:3])}...)")
    if o.get("year")!=v.get("year"): ch.append(f"year: {o.get('year')} -> {v.get('year')}")
    if n(o.get("pages"))!=n(v.get("pages")): ch.append(f"pages: {o.get('pages','-')} -> {v.get('pages','-')}")
    vo=o.get("booktitle") or o.get("journal") or o["type"]; vv=v.get("booktitle") or v.get("journal") or v["type"]
    if o["type"]=="misc" and v["type"]!="misc": ch.append(f"venue: preprint -> {vv[:70]}")
    if ch: rows.append({"key":k,"change":"corrected","detail":" | ".join(ch)})
with open(sys.argv[3],"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["key","change","detail"]); w.writeheader(); w.writerows(rows)
import collections
print(collections.Counter(r["change"] for r in rows))
kinds=collections.Counter()
for r in rows:
    for t in ["title","authors","year","pages","venue"]:
        if r["change"]=="corrected" and r["detail"].count(t+":") : kinds[t]+=1
print(kinds)
for r in rows:
    if r["change"]=="corrected" and ("authors" in r["detail"] or "title" in r["detail"] or "venue" in r["detail"] or "year" in r["detail"]): print(r["key"],"::",r["detail"][:230])
