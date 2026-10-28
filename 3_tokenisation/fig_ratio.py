import json,sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=json.load(open(sys.argv[1])); out=sys.argv[2]
names=sorted(R,key=lambda k:R[k]["corpora"]["FLORES-200 devtest | NFC"]["agg_ratio"])
data=[R[k]["corpora"]["FLORES-200 devtest | NFC"]["ratios"] for k in names]
bangla={"BanglaBERT","BanglaT5","BanglishBERT","TituLLM-1B v2","IndicBERT v2","Sarvam-1"}
plt.rcParams.update({"font.size":9,"font.family":"DejaVu Sans"})
fig,ax=plt.subplots(figsize=(6.6,4.6))
bp=ax.boxplot(data,orientation="horizontal",whis=(5,95),showfliers=False,patch_artist=True,widths=0.6,medianprops=dict(color="#1f1f1f",linewidth=1.5))
for i,b in enumerate(bp["boxes"]):
    b.set_facecolor("#2a6fdb" if names[i] in bangla else "#b9c3cf"); b.set_edgecolor("#3a3a3a"); b.set_linewidth(0.8)
for w in bp["whiskers"]+bp["caps"]: w.set_color("#555"); w.set_linewidth(0.8)
ax.axvline(1,color="#c0392b",lw=1,ls="--"); ax.text(1.03,len(names)+0.35,"parity",color="#c0392b",fontsize=8)
ax.set_yticks(range(1,len(names)+1)); ax.set_yticklabels(names)
ax.set_xscale("log"); ax.set_xticks([0.5,1,2,4,8,12]); ax.set_xticklabels(["0.5","1","2","4","8","12"])
ax.set_xlabel("Paired sentence-level token ratio |T(bn)| / |T(en)|  (log scale)")
ax.grid(axis="x",color="#e3e3e3",lw=0.6); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc="#2a6fdb",ec="#3a3a3a",label="Vocabulary trained or extended on Bangla/Indic data"),Patch(fc="#b9c3cf",ec="#3a3a3a",label="English-centric or general multilingual")],loc="lower right",frameon=False,fontsize=8)
fig.tight_layout(); fig.savefig(out); fig.savefig(out.replace(".pdf",".png"),dpi=150)
