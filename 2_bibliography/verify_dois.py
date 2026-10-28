import re,sys,json,urllib.request,difflib,time,concurrent.futures as cf
s=open(sys.argv[1],encoding="utf-8").read()
ents=[e for e in re.split(r"\n(?=@)",s) if e.strip().startswith("@")]
def field(e,k):
    m=re.search(r"\b"+k+r"\s*=\s*[{\"](.+?)[}\"]\s*,?\s*\n",e,re.S); return m.group(1) if m else None
def norm(t): return re.sub(r"[^a-z0-9 ]","",re.sub(r"[{}\\]","",t.lower()))
def get(doi):
    req=urllib.request.Request("https://doi.org/"+doi.replace("\\_","_"),headers={"Accept":"application/vnd.citationstyles.csl+json","User-Agent":"bibcheck (mailto:sm.nihal4@gmail.com)"})
    try:
        d=json.load(urllib.request.urlopen(req,timeout=40)); return d
    except Exception as ex: return {"err":str(ex)[:60]}
rows=[]
def work(e):
    key=re.match(r"@\w+\{([^,]+),",e.strip()).group(1)
    doi=field(e,"doi"); title=field(e,"title") or ""
    if not doi: return (key,"NO-DOI",title[:70],"")
    d=get(doi)
    if "err" in d: return (key,"ERR "+d["err"],title[:70],doi)
    rt=d.get("title",""); rt=rt if isinstance(rt,str) else rt[0]
    sim=difflib.SequenceMatcher(None,norm(title),norm(rt)).ratio()
    yr=(d.get("issued",{}).get("date-parts",[[None]])[0][0])
    return (key,f"sim={sim:.2f} yr={yr}",title[:70],rt[:70] if sim<0.9 else "")
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(work,ents): rows.append(r)
json.dump(rows,open("doi_check.json","w"),indent=0)
for r in rows:
    if not r[1].startswith("sim=1.00") and not r[1].startswith("sim=0.9"): print(r)
print(len(rows),"entries checked")
