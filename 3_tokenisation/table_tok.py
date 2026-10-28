import json,sys
R=json.load(open(sys.argv[1]))
order=sorted(R,key=lambda k:-R[k]["corpora"]["FLORES-200 devtest | NFC"]["agg_ratio"])
scope={"GPT-2":"English","Mistral-7B":"English/European","Llama-2":"English-centric","mBERT":"Multilingual","XGLM-564M":"Multilingual","XLM-R (base/large)":"Multilingual","mT5 / Aya-101":"Multilingual","BLOOM-560m":"Multilingual","Qwen2.5":"Multilingual","Llama-3.2":"Multilingual","Gemma-2":"Multilingual","TigerLLM-1B-it":"Multilingual (Gemma-3)$^{b}$","TituLLM-1B v2":"Llama-3.2 + Bangla$^{c}$","IndicBERT v2":"Indic","Sarvam-1":"Indic","BanglishBERT":"Bangla--English","BanglaBERT":"Bangla","BanglaT5":"Bangla"}
L=[]
for k in order:
    d=R[k]["corpora"]["FLORES-200 devtest | NFC"]; raw=R[k]["corpora"]["FLORES-200 devtest | raw"]; nt=R[k]["corpora"]["NTREX-128 | NFC"]
    unk=f"{d['unk_bn']*100:.2f}"
    if abs(raw['unk_bn']-d['unk_bn'])>0.001: unk+=f" ({raw['unk_bn']*100:.2f})"
    name=k.replace("_","\\_")+("$^{a}$" if k in ("Llama-2","Llama-3.2","Gemma-2") else "")
    L.append(f"{name} & {scope[k]} & {d['fert_bn']:.2f} & {d['fert_en']:.2f} & {d['fert_ratio']:.2f} & \\textbf{{{d['agg_ratio']:.2f}}} [{d['agg_ratio_ci'][0]:.2f}, {d['agg_ratio_ci'][1]:.2f}] & {d['median_ratio']:.2f} ({d['q1']:.2f}--{d['q3']:.2f}) & {d['frac_gt1']*100:.0f} & {unk} & {nt['agg_ratio']:.2f} \\\\")
open(sys.argv[2],"w").write("\n".join(L)+"\n"); print("\n".join(L))
d=R["Mistral-7B"]["corpora"]["FLORES-200 devtest | NFC"]; print("word ratio",d["word_ratio"])
# max abs diff between corpora for agg ratio
mx=max(abs(R[k]["corpora"][c+" | NFC"]["agg_ratio"]-R[k]["corpora"]["FLORES-200 devtest | NFC"]["agg_ratio"]) for k in R for c in ["NTREX-128","FLORES-200 dev"])
print("max diff across corpora",mx)
mxr=max(abs(R[k]["corpora"]["FLORES-200 devtest | raw"]["agg_ratio"]-R[k]["corpora"]["FLORES-200 devtest | NFC"]["agg_ratio"]) for k in R); print("max raw-vs-NFC diff",mxr)
print({k:round(R[k]["corpora"]["FLORES-200 devtest | raw"]["agg_ratio"],3) for k in ["BanglaBERT","mBERT","BanglishBERT"]})
