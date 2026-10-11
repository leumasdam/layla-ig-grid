"""Poradie feedu: prísna šachovnica svetlý/tmavý (pri 3 stĺpcoch = striedanie po jednom), potom pestrosť tém.
python rytmus.py -> proposal.js + rytmus.jpg"""
import json, re, math, random, pathlib
import numpy as np
from PIL import Image, ImageDraw
ROOT = pathlib.Path(__file__).parent
P = {p["id"]: p for p in json.load(open(ROOT / "posts.json", encoding="utf-8"))}
old = json.loads(re.search(r"PROPOSAL=(\[.*?\])", (ROOT / "proposal.js").read_text()).group(1))
PARKED = json.loads(re.search(r"PROPOSAL_PARKED=(\[.*?\])", (ROOT / "proposal.js").read_text()).group(1))
L = {p: np.asarray(Image.open(ROOT / "thumbs" / f"{p}.webp").convert("L")).mean() for p in old}
LIGHT_EXTRA = {"p17", "p35"}               # krémové horné pole -> vo feede pôsobia svetlo
light = [p for p in old if L[p] > 170 or p in LIGHT_EXTRA]
dark = [p for p in old if p not in light]
FIRST = "p03"                               # logo LAYLA ako prvý (svetlý) post
HIGH = {"p48": 12, "p46": 12}              # obľúbený štýl (riedke verzálky) -> do prvých 4 riadkov
for p in HIGH: P[p]["q"] = 3
assert len(light) == (len(old) + 1) // 2, (len(light), len(dark))
n, C = len(old), 3

def cost(o):
    t = 0.0
    for i, p in enumerate(o):
        a = P[p]; r, c = divmod(i, C)
        x = i / (n - 1); q = a.get("q", 2)
        t += (x * x * 6 if q == 3 else (1 - x) ** 2 * 5 if q == 1 else 0)
        for j in ([i + 1] if c < C - 1 else []) + [i + C]:   # priami susedia
            if j < n and P[o[j]]["cat"] == a["cat"]: t += 8
        for j in ([i + C + 1] if c < C - 1 else []) + ([i + C - 1] if c > 0 else []):   # diagonála (rovnaký tón)
            if j < n and P[o[j]]["cat"] == a["cat"]: t += 4
        for j in range(i + 1, min(n, i + 13)):
            b = P[o[j]]; rj, cj = divmod(j, C); dist = abs(rj - r) + abs(cj - c)
            if a["grp"] and a["grp"] == b["grp"] and dist <= 4: t += 20 / dist
            elif a["head"] and a["head"] == b["head"] and dist <= 3: t += 9 / dist
        if p in HIGH and i >= HIGH[p]: t += 40 + (i - HIGH[p]) * 4
        if p == "p48":                                         # obe verzálkové od seba aspoň cez riadok
            k = o.index("p46"); d = abs(k // C - r) + abs(k % C - c)
            if d <= 2: t += 30
        if c == 0 and i + 2 < n:                               # pestrý riadok
            t += (3 - len({P[o[k]]["cat"] for k in range(i, i + 3)})) * 1.5
    return t

def solve(seed):
    rnd = random.Random(seed)
    Lp = [p for p in light if p != FIRST]; Dp = dark[:]; rnd.shuffle(Lp); rnd.shuffle(Dp)
    o = []; li = di = 0
    for i in range(n):
        if i == 0: o.append(FIRST)
        elif i % 2 == 0: o.append(Lp[li]); li += 1
        else: o.append(Dp[di]); di += 1
    cur = cost(o); best, bc = o[:], cur; T = 6.0
    for _ in range(60000):
        i = rnd.randrange(1, n); j = rnd.randrange(1, n)
        if i == j or i % 2 != j % 2: continue                  # meníme len v rámci tónu
        o[i], o[j] = o[j], o[i]; c2 = cost(o)
        if c2 <= cur or rnd.random() < math.exp((cur - c2) / T):
            cur = c2
            if c2 < bc: bc, best = c2, o[:]
        else: o[i], o[j] = o[j], o[i]
        T = max(0.03, T * 0.99988)
    return bc, best

bc, best = min(solve(s) for s in (1, 2, 3, 5, 8, 13))
(ROOT / "proposal.js").write_text(f"window.PROPOSAL={json.dumps(best)};\nwindow.PROPOSAL_PARKED={json.dumps(PARKED)};\n", encoding="utf-8")
W, H = 180, 225
s = Image.new("RGB", (3 * W + 8, ((n + 2) // 3) * (H + 4)), "white"); dr = ImageDraw.Draw(s)
for i, p in enumerate(best):
    x, y = (i % 3) * (W + 4), (i // 3) * (H + 4)
    s.paste(Image.open(ROOT / "thumbs" / f"{p}.webp").convert("RGB").resize((W, H)), (x, y))
    dr.rectangle([x, y, x + 92, y + 14], fill="black"); dr.text((x + 2, y + 2), f"{i+1} {p} {P[p]['cat']}", fill="white")
s.save(ROOT.parent / "layla-ig" / "rytmus.jpg", quality=85)
print("cost", round(bc, 1)); print(best)
