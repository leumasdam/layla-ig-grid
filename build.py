"""LAYLA IG grid: posty zo src/ -> export/, thumbs/, data.js, thumbs-data.js, proposal.js, avatar.png"""
import json, base64, io, subprocess, pathlib
import numpy as np
from PIL import Image, ImageFilter
ROOT = pathlib.Path(__file__).parent
SRC = pathlib.Path(r"C:\Users\samue\layla-ig\src")
# id: (kind, cat, grp, head, q, title)
T = {
 "p01": ("V","priestor",None,"telo",2,"Lounge – Telo v pohode"),
 "p02": ("F","masaz",None,None,3,"Masáž chrbta pri sviečkach"),
 "p03": ("T","znacka","logo",None,3,"Logo LAYLA"),
 "p04": ("F","priestor",None,None,2,"Masážna miestnosť"),
 "p05": ("O","madero",None,None,3,"Nástroje na maderoterapiu"),
 "p06": ("T","znacka","telo","telo",3,"Telo v pohode – logo"),
 "p07": ("F","masaz",None,None,2,"Masáž chrbta – logo"),
 "p08": ("F","masaz",None,None,2,"Masáž hlavy a šije"),
 "p09": ("T","znacka","logo",None,2,"Logo v kruhu"),
 "p10": ("T","znacka","logo",None,1,"Logo – veľké"),
 "p11": ("T","citat","telomysel","telo",2,"Telo v pohode. Myseľ v pokoji."),
 "p12": ("T","rezervacia","rezerv",None,3,"Rezervujte si svoj termín"),
 "p13": ("T","recenzie","recenzia",None,2,"Názory klientov (doplniť reálnu recenziu)"),
 "p14": ("V","sluzby","sluzby",None,3,"Naše služby – s fotkami"),
 "p15": ("V","masaz","doprajte",None,3,"Doprajte telu regeneráciu"),
 "p16": ("V","priestor","priestor",None,2,"Priestor, kde spomalíte"),
 "p17": ("V","madero","madero",None,3,"Maderoterapia – nástroje"),
 "p18": ("V","masaz","dotyk","dotyk",2,"Dotyk, ktorý uvoľní – chrbát"),
 "p19": ("V","masaz","uvolnenie",None,2,"Uvoľnenie od hlavy po päty – chodidlá"),
 "p20": ("T","citat","telomysel","telo",1,"Telo v pohode. Myseľ v pokoji. (variant)"),
 "p21": ("V","rezervacia","rezerv",None,2,"Rezervujte si chvíľu pokoja"),
 "p23": ("T","sluzby","sluzby",None,2,"Naše služby – ikony"),
 "p24": ("V","priestor","priestor",None,2,"Priestor pre oddych"),
 "p25": ("V","masaz","uvolnenie",None,3,"Uvoľnenie od hlavy po päty"),
 "p26": ("V","madero","madero",None,2,"Maderoterapia – tmavá"),
 "p27": ("V","masaz","dotyk","dotyk",2,"Dotyk, ktorý uvoľní – chodidlá"),
 "p28": ("V","poukaz","poukaz",None,3,"Darujte oddych – poukaz"),
 "p29": ("T","rezervacia",None,None,3,"Prvá návšteva?"),
 "p30": ("V","citat","telomysel","telo",2,"Telo v pohode – s fotkou"),
 "p31": ("T","recenzie","recenzia",None,2,"Vaše slová nás tešia (doplniť reálnu recenziu)"),
 "p32": ("T","rezervacia","rezerv",None,2,"Rezervujte si chvíľu pre seba"),
 "p33": ("V","priestor",None,None,3,"Pokojné súkromné štúdio v Piešťanoch"),
 "p34": ("V","masaz","doprajte",None,2,"Doprajte telu regeneráciu (variant)"),
 "p35": ("V","madero","madero",None,2,"Maderoterapia – svetlá"),
 "p36": ("V","poukaz","poukaz",None,3,"Darčekový poukaz"),
 "p37": ("V","sluzby","sluzby",None,2,"Naše služby – variant"),
 "p38": ("T","znacka","logo",None,2,"Logo s oblúkom"),
 "p39": ("O","priestor",None,None,3,"Sviečky a banky"),
 "p40": ("F","masaz",None,None,3,"Masáž chrbta"),
 "p41": ("T","citat","dotyk","dotyk",2,"Dotyk, ktorý vracia telo k sebe"),
 "p42": ("T","znacka","telo","telo",2,"Telo v pohode – Piešťany"),
 "p43": ("V","priestor","priestor",None,2,"Priestor pre pokoj"),
 "p44": ("V","madero","madero",None,2,"Maderoterapia – oblúk"),
 "p45": ("T","recenzie","recenzia",None,1,"Vaše recenzie (doplniť reálnu recenziu)"),
 "p46": ("T","rezervacia","rezerv",None,1,"Rezervujte si svoj čas"),
 "p47": ("F","priestor",None,None,3,"Miestnosť so svetielkami"),
 "p48": ("T","citat","dotyk","dotyk",1,"Dotyk, ktorý navracia rovnováhu"),
 "p49": ("O","priestor",None,None,3,"Sviečka a difuzér"),
 "p50": ("O","masaz",None,None,3,"Masáž chodidiel"),
 "p52": ("F","priestor",None,None,2,"Lounge – sedačka"),
}
PARKED = ["p13", "p31", "p45"]          # vymyslené recenzie -> najprv reálny text
START = ["p03","p52","p02", "p47","p06","p05", "p50","p41","p49"]   # podľa referencie (bez „Viac než masáž“)
posts, thumbs = [], {}
for pid, (kind, cat, grp, head, q, title) in T.items():
    im = Image.open(SRC / f"{pid}.png").convert("RGB")
    full = im.resize((1080, 1350), Image.LANCZOS); full.save(ROOT / "export" / f"{pid}.jpg", quality=90)
    th = im.resize((540, 675), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    th.save(ROOT / "thumbs" / f"{pid}.webp", quality=88)
    b = io.BytesIO(); th.save(b, "WEBP", quality=80); thumbs[pid] = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
    a = np.asarray(im.convert("L").resize((200, 250))).astype(float)
    L = a.mean(); dark = (a < 80).mean()
    e = np.concatenate([a[:8].ravel(), a[-8:].ravel(), a[:, :8].ravel(), a[:, -8:].ravel()]).mean()
    posts.append(dict(id=pid, cat=cat, kind=kind, grp=grp, title=title, tone="dark" if L < 125 else "light",
                      L=round(L), red=0, head=head, q=q, edge=round(e), darkShare=round(dark, 2)))
(ROOT / "data.js").write_text("window.POSTS=" + json.dumps(posts, ensure_ascii=False) + ";\n", encoding="utf-8")
(ROOT / "thumbs-data.js").write_text("window.THUMBS=" + json.dumps(thumbs) + ";\n", encoding="utf-8")
(ROOT / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
# návrh: prvé 3 riadky zamknuté podľa referencie, zvyšok optimalizuje rhythm.js
js = """
require('./rhythm.js');const R=globalThis.Rhythm||require('./rhythm.js');const P=require('./posts.json');const by=Object.fromEntries(P.map((p,i)=>[p.id,i]));
const START=%s, PARK=new Set(%s);
const rest=P.map((_,i)=>i).filter(i=>!START.includes(P[i].id)&&!PARK.has(P[i].id));
const order=[...START.map(id=>by[id]),...rest];const locked=new Set(START.map(id=>by[id]));
let best=null;for(const seed of [3,7,11,19,23,31]){const r=R.optimize(order,P,R.DEFAULTS,{seed,locked,iters:80000});if(!best||r.cost<best.cost)best=r;}
const ev=R.evaluate(best.order,P,R.DEFAULTS,true);
console.log(JSON.stringify({order:best.order.map(i=>P[i].id),cost:best.cost,issues:ev.issues.length}));
""" % (json.dumps(START), json.dumps(PARKED))
(ROOT / "_plan.cjs").write_text(js, encoding="utf-8")
out = json.loads(subprocess.run(["node", "_plan.cjs"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
(ROOT / "proposal.js").write_text(f"window.PROPOSAL={json.dumps(out['order'])};\nwindow.PROPOSAL_PARKED={json.dumps(PARKED)};\n", encoding="utf-8")
print("posts", len(posts), "cost", out["cost"], "issues", out["issues"])
# avatar: logo na krémovom kruhu
logo = Image.open(r"C:\Users\samue\laura-ejupi-web-v3\img\brand\layla_monogram_black.svg") if False else None
