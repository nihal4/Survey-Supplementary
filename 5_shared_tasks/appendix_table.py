import json,sys
R=json.load(open(sys.argv[1])); out=sys.argv[2]
def esc(s): return str(s).replace("&","\\&").replace("_","\\_").replace("%","\\%").replace("#","\\#")
def ck(v): return "\\checkmark" if v==1 else ""
L=[]
L.append(r"""{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{longtable}{@{}l l r r p{3.7cm} c c c c c c@{}}
\caption{Paper-by-paper extraction for the three classification shared tasks (one row per system paper and task). Rank and score are the official values from the organisers' overview papers; where a system paper states a different rank it is noted in the released CSV. Ens = ensemble; MTL = multi-task learning; Hier = hierarchical/two-stage; LLM = decoder LLM produced the submission; Ext = external training data; Aug = augmentation of the official data. Coding rules are given in Section~\ref{sec:shared-tasks}.}\label{tab:st-extraction}\\
\toprule
\textbf{Task} & \textbf{Team} & \textbf{Rank} & \textbf{Score} & \textbf{Submitted system} & \textbf{Ens} & \textbf{MTL} & \textbf{Hier} & \textbf{LLM} & \textbf{Ext} & \textbf{Aug}\\
\midrule\endfirsthead
\toprule
\textbf{Task} & \textbf{Team} & \textbf{Rank} & \textbf{Score} & \textbf{Submitted system} & \textbf{Ens} & \textbf{MTL} & \textbf{Hier} & \textbf{LLM} & \textbf{Ext} & \textbf{Aug}\\
\midrule\endhead
\bottomrule\endfoot""")
tn={"2023-T1":"23-T1","2023-T2":"23-T2","2025-T1":"25-T1"}
for r in R:
    if r["task"]=="2025-T2": continue
    sc=f"{r['score_official']:.2f}" if r["task"]=="2023-T1" else f"{r['score_official']:.4f}"
    L.append(f"{tn[r['task']]} & {esc(r['team'])}~\\citep{{{r['key']}}} & {r['rank_official']}/{r['n_teams']} & {sc} & {esc(r['backbone'])} & {ck(r['ensemble'])} & {ck(r['multitask'])} & {ck(r['hierarchical'])} & {ck(r['decoder_llm'])} & {ck(r['external_data'])} & {ck(r['augmentation'])}\\\\")
L.append(r"\end{longtable}}")
L.append(r"""
{\scriptsize\setlength{\tabcolsep}{3pt}
\begin{longtable}{@{}l r r p{4.2cm} r c c c c@{}}
\caption{Paper-by-paper extraction for BLP-2025 Task~2 (Bangla-to-Python code generation; Pass@1, test phase). Exec = unit tests executed and the result fed back at inference or used to select training samples; Trans = Bangla instruction translated or rewritten into English first; FT = task fine-tuning; Prop = proprietary model in the submitted system. Params = billions of parameters of the largest open model (--- for proprietary).}\label{tab:st-extraction-code}\\
\toprule
\textbf{Team} & \textbf{Rank} & \textbf{Pass@1} & \textbf{Submitted system} & \textbf{Params} & \textbf{Exec} & \textbf{Trans} & \textbf{FT} & \textbf{Prop}\\
\midrule\endfirsthead
\toprule
\textbf{Team} & \textbf{Rank} & \textbf{Pass@1} & \textbf{Submitted system} & \textbf{Params} & \textbf{Exec} & \textbf{Trans} & \textbf{FT} & \textbf{Prop}\\
\midrule\endhead
\bottomrule\endfoot""")
for r in R:
    if r["task"]!="2025-T2": continue
    pb="---" if r["params_B"] in (None,"") else (f"{r['params_B']:g}")
    L.append(f"{esc(r['team'])}~\\citep{{{r['key']}}} & {r['rank_official']}/{r['n_teams']} & {r['score_official']:.2f} & {esc(r['backbone'])} & {pb} & {ck(r['exec_feedback'])} & {ck(r['translation'])} & {ck(r['finetuned'])} & {ck(r['proprietary'])}\\\\")
L.append(r"\end{longtable}}")
open(out,"w",encoding="utf-8").write("\n".join(L)+"\n")
