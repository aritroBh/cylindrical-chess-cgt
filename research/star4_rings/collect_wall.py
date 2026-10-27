import re, itertools

hits_path = "/Users/aritro/Downloads/Research/Chessendgames/research/star26_rings/c8/p10_5_5_hits.tsv"
pairs = [("W2","B4"),("B4","W2"),("W3","B5"),("B5","W3"),("W2","B5"),("B5","W2"),("W3","B4"),("B4","W3")]

def parse_pos(line):
    # "W: a3 b3 ... / B: b6 ..."
    left, right = line.split("/")
    wpart = left.split(":",1)[1].split()
    bpart = right.split(":",1)[1].split()
    files = list("abcdefgh")
    wt = {f:[] for f in files}
    bt = {f:[] for f in files}
    for sq in wpart:
        wt[sq[0]].append(int(sq[1:]))
    for sq in bpart:
        bt[sq[0]].append(int(sq[1:]))
    toks=[]
    for f in files:
        t=""
        if wt[f]: t += "W" + "".join(str(r) for r in sorted(wt[f]))
        if bt[f]: t += "B" + "".join(str(r) for r in sorted(bt[f]))
        toks.append(t if t else "-")
    return toks

out=[]
cid=0
with open(hits_path) as fh:
    for line in fh:
        line=line.strip()
        if not line: continue
        toks=parse_pos(line.split("\t")[0])
        for ins in range(8):
            for pa,pb in pairs:
                new = toks[:ins] + [pa,pb] + toks[ins:]
                out.append((cid, 10, " ".join(new)))
                cid+=1
with open("wall_candidates.txt","w") as fh:
    for cid,n,pos in out:
        fh.write(f"{cid}\t{n}\t{pos}\n")
print("generated", len(out))
