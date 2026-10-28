import gzip,re,json,sys
txt=gzip.open(sys.argv[1],"rt",encoding="utf-8").read()
ents=re.split(r"\n(?=@)",txt)
out=[]
def f(e,k):
    m=re.search(r"\n\s*"+k+r'\s*=\s*"(.*?)",?\s*\n',e,re.S)
    if not m: m=re.search(r"\n\s*"+k+r"\s*=\s*\{(.*?)\},?\s*\n",e,re.S)
    return re.sub(r"\s+"," ",m.group(1)).strip() if m else ""
for e in ents:
    m=re.match(r"@(\w+)\{([^,]+),",e)
    if not m or m.group(1)=="proceedings": continue
    out.append({"key":m.group(2),"type":m.group(1),"title":f(e,"title"),"abstract":f(e,"abstract"),"booktitle":f(e,"booktitle") or f(e,"journal"),"year":f(e,"year"),"url":f(e,"url"),"doi":f(e,"doi"),"author":f(e,"author")})
json.dump(out,open(sys.argv[2],"w"))
print(len(out))
