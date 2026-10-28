"""Paper-by-paper extraction of the 66 BLP shared-task system papers (revision R1.5).
Official rank and score are taken from the organisers' overview papers (leaderboard tables),
not from the system papers; where a system paper reports a different rank, both are kept.
Coding rules (applied to the officially submitted system, not post-competition variants):
  ens   = predictions of >=2 separately trained models (or k-fold models) are combined
  mtl   = one model trained jointly on >=2 label dimensions with shared parameters
  hier  = cascaded / two-stage classification
  llm   = a decoder-only LLM produces the submitted predictions
  prop  = submitted system relies on a proprietary API model
  ext   = labelled or unlabelled data beyond the official training set used for training
          (incl. domain-adaptive pretraining corpora); augmentation of official data is 'aug'
  exec  = (code task) unit tests are executed and the result is fed back (inference) or used
          to select training samples
  trans = (code task) Bangla instruction translated/rewritten into English before generation
  ft    = model weights fine-tuned (incl. LoRA) for the task
  params_B = approximate parameter count of the largest model in the submitted system
             (public model cards; None = proprietary/undisclosed)
Usage: python extraction.py out_dir
"""
import csv, json, sys

Y, N = 1, 0
# key, task, team, rank_official, score_official, rank_in_paper, backbone, params_B, ens, mtl, hier, llm, prop, ext, aug, note
CLS = [
 # ---- BLP-2023 Task 1: violence-inciting text detection (macro-F1, 27 teams)
 ("fahim-2023-aambela","2023-T1","Aambela",2,76.041,2,"BanglaBERT (+new vocab tokens)",0.11,N,N,N,N,N,N,N,"three classification heads; adds frequent OOV words as tokens"),
 ("hossain-etal-2023-nlp","2023-T1","NLP_CUET",3,74.587,3,"Bangla-ELECTRA + GAN",0.11,N,N,N,N,N,N,N,""),
 ("dey-etal-2023-semantics","2023-T1","Semantics Squad",5,74.413,5,"BanglaBERT-large",0.335,N,N,N,N,N,N,N,""),
 ("raihan-etal-2023-nlpbdpatriots","2023-T1","nlpBDpatriots",6,74.313,6,"multilingual transformer, two-step",0.278,N,N,Y,N,N,N,Y,"back-translation"),
 ("tariquzzaman-etal-2023-linguists","2023-T1","the_linguists",7,73.978,7,"BanglaBERT",0.11,N,N,N,N,N,N,N,"proposed informal FastText embedding scored 70.45 post hoc, below the submitted BanglaBERT"),
 ("das-etal-2023-emptymind","2023-T1","EmptyMind",9,73.797,9,"Hierarchical-BERT",0.11,N,N,Y,N,N,N,N,""),
 ("page-etal-2023-mavericks","2023-T1","Mavericks",10,73.699,10,"BERT-family ensemble",0.278,Y,N,N,N,N,N,N,""),
 ("veeramani-etal-2023-lowresourcenlu","2023-T1","LowResourceNLU",11,73.468,11,"BanglaBERT + mBERT aggregation",0.178,Y,N,N,N,N,N,N,"also Task 2"),
 ("chatterjee-etal-2023-vaclm","2023-T1","VacLM",12,72.656,12,"BanglaBERT",0.11,N,N,N,N,N,N,N,""),
 ("ahmed-etal-2023-score","2023-T1","Score_IsAll_You_Need",14,72.376,14,"BanglaBERT, two-step",0.11,N,N,Y,N,N,N,N,""),
 ("shibu-etal-2023-sust","2023-T1","SUST_Black Box",18,70.680,18,"BanglaBERT + MLM domain adaptation",0.11,N,N,N,N,N,Y,N,"weighted ensemble reported post hoc only"),
 ("riyad-etal-2023-team","2023-T1","Team_Syrax",19,70.450,19,"transformer ensemble",0.278,Y,N,N,N,N,Y,Y,"self-training on external data; back-translation"),
 ("alamgir-haque-2023-team","2023-T1","Team CentreBack",21,69.390,21,"BanglaBERT",0.11,N,N,N,N,N,N,N,""),
 ("mukherjee-etal-2023-ufal","2023-T1","UFAL-ULD",22,69.009,20,"XLM-R base",0.278,N,N,N,N,N,N,N,"paper reports rank 20"),
 ("saha-nanda-2023-banglanlp","2023-T1","BanglaNLP",23,68.110,23,"multilingual-e5-base",0.278,N,N,N,N,N,N,Y,""),
 ("das-etal-2023-team","2023-T1","Team Error Point",26,31.913,26,"classical ML / LSTM",None,N,N,N,N,N,N,N,"lexical/classical features"),
 # ---- BLP-2023 Task 2: sentiment (micro-F1, 30 teams; ranks as printed incl. two baseline rows)
 ("fahim-2023-aambela-blp","2023-T2","Aambela",1,0.7310,1,"BanglaBERT",0.11,Y,N,N,N,N,N,N,"mode-based ensemble"),
 ("liu-etal-2023-knowdee","2023-T2","Knowdee",2,0.7267,2,"BanglaBERT ensemble + pseudo-labels",0.11,Y,N,N,N,N,N,Y,"pseudo-labelling"),
 ("chakma-hasan-2023-lowresource","2023-T2","LowResource",3,0.7179,3,"BanglaBERT ensemble",0.11,Y,N,N,N,N,Y,Y,"several external datasets"),
 ("veeramani-etal-2023-lowresourcenlu","2023-T2","LowResourceNLU",4,0.7172,4,"BanglaBERT + mBERT aggregation",0.178,Y,N,N,N,N,N,N,"same paper as Task 1"),
 ("tarannum-etal-2023-z","2023-T2","Z-Index",5,0.7164,5,"BanglaBERT",0.11,N,N,N,N,N,N,N,""),
 ("fatema-etal-2023-emptymind","2023-T2","EmptyMind",7,0.7109,7,"BanglaBERT-large",0.335,N,N,N,N,N,N,N,""),
 ("tonmoy-2023-embeddings","2023-T2","Embeddings",9,0.7088,9,"fine-tuned transformer, cost-sensitive loss",0.335,N,N,N,N,N,N,N,""),
 ("seth-etal-2023-rsm","2023-T2","RSM-NLP",10,0.7078,10,"weighted/majority-vote transformer ensemble",0.278,Y,N,N,N,N,N,N,""),
 ("goswami-etal-2023-nlpbdpatriots","2023-T2","nlpBDpatriots",12,0.7058,12,"transfer learning",0.278,N,N,N,N,N,N,Y,""),
 ("rahman-uzuner-2023-m1437","2023-T2","M1437",14,0.7036,14,"BanglaBERT-large",0.335,N,N,N,N,N,Y,N,"external training data lowered test F1 (71.54 without)"),
 ("mukherjee-etal-2023-ufal-uld","2023-T2","UFAL-ULD",19,0.6768,19,"XLM-R base",0.278,N,N,N,N,N,N,N,""),
 ("dey-etal-2023-semantics-squad","2023-T2","Semantics Squad",20,0.6742,20,"BanglaBERT-small",None,N,N,N,N,N,N,N,""),
 ("saha-nanda-2023-banglanlp-blp","2023-T2","BanglaNLP",21,0.6702,21,"Twitter-sentiment XLM-R",0.278,N,N,N,N,N,N,N,"intermediate fine-tuning on Twitter sentiment"),
 ("das-etal-2023-team-error","2023-T2","Error Point",27,0.4129,27,"classical ML / LSTM",None,N,N,N,N,N,N,Y,"lexical/classical features"),
 ("khushbu-etal-2023-ushoshi2023","2023-T2","Ushoshi2023",30,0.2626,30,"DistilBERT",0.134,N,N,N,N,N,N,Y,"SVM 75% accuracy reported post hoc, not on leaderboard"),
 # ---- BLP-2025 Task 1, subtask 1A: hate type (micro-F1)
 ("islam-etal-2025-code","2025-T1","Code_Gen",1,0.7362,1,"BanglaBERT/MuRIL/mE5/Twitter-XLM-R logit ensemble",0.278,Y,N,N,N,N,N,N,"adversarial contrastive training"),
 ("riad-2025-syntaxmind","2025-T1","SyntaxMind",2,0.7345,2,"BanglaBERT + CNN/GRU attention",0.11,N,N,N,N,N,N,N,""),
 ("mahim-hasan-2025-teamhatemate","2025-T1","TeamHateMate",4,0.7331,4,"k-fold transformer ensemble, cascade",0.278,Y,N,Y,N,N,N,N,""),
 ("hasan-etal-2025-ecstasy","2025-T1","Ecstasy",5,0.7328,5,"Llama-3.1-8B + LoRA",8.0,N,N,N,Y,N,N,N,"TF-IDF keyword prompts"),
 ("hoque-etal-2025-gradient","2025-T1","Gradient Masters",6,0.7323,6,"BanglaBERT ensemble + FGSM",0.11,Y,N,N,N,N,N,N,""),
 ("hasan-2025-catalyst","2025-T1","Catalyst",7,0.7305,7,"IndicBERTv2 ensemble, multi-task head",0.278,Y,Y,N,N,N,N,N,""),
 ("tripty-etal-2025-belite","2025-T1","BElite",8,0.7282,3,"BanglaBERT/mBERT/XLM-R weighted ensemble",0.278,Y,N,N,N,N,N,N,"paper reports 3rd (0.734); overview lists 8th (0.7282)"),
 ("saha-etal-2025-retriv","2025-T1","Retriv",9,0.7275,9,"BanglaBERT/MuRIL/IndicBERTv2 soft vote",0.278,Y,Y,N,N,N,N,N,"multi-task variants for 1C"),
 ("alam-etal-2025-cou","2025-T1","CoU-CU-DSG",10,0.7273,10,"BanglaBERT/XLM-R/MuRIL weighted fusion",0.278,Y,N,N,N,N,N,N,""),
 ("hossan-etal-2025-cuet-nlp-zenith","2025-T1","CUET-NLP_Zenith",11,0.7263,11,"BanglaBERT/XLM-R ensemble (BanTriX)",0.278,Y,Y,N,N,N,N,N,""),
 ("nabil-etal-2025-nsu","2025-T1","NSU_MILab",12,0.7250,12,"4-model probability averaging",0.278,Y,N,N,N,N,N,N,"paper reports 0.7235"),
 ("tahmid-etal-2025-pentaml","2025-T1","PentaML",14,0.7178,15,"linear probing of fine-tuned BERTs",0.278,N,N,N,N,N,N,N,""),
 ("anam-etal-2025-hatenet","2025-T1","HateNetBN",15,0.7133,15,"frozen BanglaBERT + hierarchical attention",0.11,N,N,N,N,N,N,N,""),
 ("prama-etal-2025-computational","2025-T1","Computational StoryLab",16,0.7111,16,"BanglaBERT (LLMs explored)",0.11,N,Y,N,N,N,N,N,"GPT-4/Llama-3.1-8B/Gemma-2-9B explored, encoder submitted"),
 ("yasir-2025-heisenberg","2025-T1","Heisenberg",18,0.7070,18,"BanglaBERT/BanglaT5/BanglaHateBERT",0.25,N,N,N,N,N,Y,Y,"~4K collected comments; back-translation"),
 ("laskar-paul-2025-bahash","2025-T1","Bahash-AI",20,0.7028,20,"BanglaBERT",0.11,N,N,N,N,N,N,Y,"+28,220 synthesised instances"),
 ("sayem-rahman-2025-velora","2025-T1","Velora",21,0.7013,21,"BanglaBERT",0.11,N,N,N,N,N,Y,Y,"+3,418 from an external dataset"),
 ("fahim-khan-2025-perceptionlab","2025-T1","PerceptionLab",23,0.6941,23,"DAPT BanglaBERT",0.11,N,N,N,N,N,Y,Y,"DAPT on 315K comments; external + weakly supervised sexism data"),
 ("tripty-etal-2025-cuet","2025-T1","CUET_Sntx_Srfrs",27,0.6867,18,"TF-IDF classical ML voting, hierarchical",None,Y,N,Y,N,N,N,N,"lexical/classical features; paper reports 18th (0.6842)"),
 ("hossan-roy-dipta-2025-promptguard","2025-T1","PromptGuard",30,0.6761,30,"Qwen3-32B few-shot + voting",32.0,N,N,N,Y,N,N,N,"chi-square keyword selection"),
]
# ---- BLP-2025 Task 2: Bangla-to-Python (Pass@1, test phase, 31 teams + organiser baseline)
# key, team, rank, pass1, model, params_B, prop, exec, trans, ft, note
CODE = [
 ("saadi-etal-2025-nala","NALA_MAINZ",1,0.95,"GPT-5",None,Y,Y,N,N,"code agent + debugger agent on failing tests"),
 ("asib-etal-2025-retriv","Retriv",2,0.93,"Qwen2.5-Coder-14B",14,N,Y,N,Y,"three test-feedback refinement passes"),
 ("hasan-etal-2025-musafir","Musafir",3,0.92,"Qwen2.5-14B-Instruct",14,N,Y,Y,N,"translate then generate; unit-test validation"),
 ("riyad-junaed-2025-adversaryai","AdversaryAI",4,0.85,"Gemini 2.5 Pro",None,Y,Y,N,N,"CoT fine-tuning for open models; best submission proprietary"),
 ("juboraj-etal-2025-bracu","BRACU_CL",5,0.84,"Gemini-2.5-flash + gpt-oss debugger",None,Y,Y,N,N,""),
 ("agarwala-etal-2025-code","Code_Gen",6,0.84,"GPT-5",None,Y,N,Y,N,"assertions placed in prompt, not executed; paper reports 7th"),
 ("dihan-etal-2025-teamb2b","TeamB2B",7,0.84,"Gemini-2.5-Pro",None,Y,Y,Y,N,"retrieval + coder/reviewer self-refinement"),
 ("fahmid-etal-2025-nsu","NSU_PiedPiper",8,0.83,"Qwen2.5-Coder-14B",14,N,N,N,N,"CoT few-shot; debugger added post-competition"),
 ("jalil-etal-2025-barrier","Barrier Breakers",11,0.82,"GPT-OSS-120B",120,N,Y,N,N,"test-driven development + code interpreter"),
 ("dewan-rifat-2025-pybhasha","PyBhasha",12,0.80,"two-stage ensemble (GPT-4.1 et al.)",None,Y,N,Y,N,"GPT-4.1 rewrites instructions in English"),
 ("pal-das-2025-ju","JU_NLP",13,0.77,"GPT-4.1",None,Y,N,N,N,"zero-shot"),
 ("rahman-etal-2025-alphaborno","AlphaBorno",16,0.72,"GPT-4o",None,Y,Y,Y,N,"synthetic tests + self-repair"),
 ("islam-etal-2025-pybangla","PyBangla",17,0.72,"Qwen3-8B",8,N,Y,N,N,"Thought-Code-Observation agent loop"),
 ("shahrier-etal-2025-cuet","CUET_Expelliarmus",21,0.37,"GPT-OSS-20B",20,N,Y,Y,N,"iterative error correction"),
 ("roy-2025-codeanubad","CodeAnubad",22,0.37,"Gemma-2-9B-it + QLoRA",9,N,N,N,Y,"self-improvement on verified dev predictions"),
 ("farazi-reza-2025-troopers","Troopers",26,0.32,"TigerLLM (Llama-3.x) RSFT",1,N,Y,N,Y,"test execution selects fine-tuning samples"),
]
N_TEAMS = {"2023-T1": 27, "2023-T2": 28, "2025-T1": 36, "2025-T2": 31}  # teams excl. baseline rows


def main(out):
    rows = []
    for (k, t, team, r, s, rp, bb, pb, ens, mtl, hier, llm, prop, ext, aug, note) in CLS:
        rows.append(dict(key=k, task=t, team=team, rank_official=r, n_teams=N_TEAMS[t], score_official=s,
                         metric={"2023-T1": "macro-F1 (x100)", "2023-T2": "micro-F1", "2025-T1": "micro-F1 (1A)"}[t],
                         rank_in_paper=rp, backbone=bb, params_B=pb, ensemble=ens, multitask=mtl,
                         hierarchical=hier, decoder_llm=llm, proprietary=prop, external_data=ext,
                         augmentation=aug, exec_feedback="", translation="", finetuned="", note=note))
    for (k, team, r, s, m, pb, prop, ex, tr, ft, note) in CODE:
        rows.append(dict(key=k, task="2025-T2", team=team, rank_official=r, n_teams=31, score_official=s,
                         metric="Pass@1", rank_in_paper=r, backbone=m, params_B=pb, ensemble="", multitask="",
                         hierarchical="", decoder_llm=1, proprietary=prop, external_data="", augmentation="",
                         exec_feedback=ex, translation=tr, finetuned=ft, note=note))
    with open(f"{out}/shared_task_extraction.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    json.dump(rows, open(f"{out}/shared_task_extraction.json", "w"), indent=1)
    print(len(rows), "rows;", len(set(r["key"] for r in rows)), "unique papers")


if __name__ == "__main__":
    main(sys.argv[1])
