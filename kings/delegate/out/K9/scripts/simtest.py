import random, sys
def trial(rng):
    nP = rng.randint(3,9); nD = rng.randint(2,6)
    # sigma moves at even-indexed P layer? use explicit mover array
    mover = [rng.choice([0,1]) for _ in range(nP)]   # 0 = sigma, 1 = loser
    check = [rng.random()<0.3 for _ in range(nP)]
    moves = []
    for y in range(nP):
        ms=[]
        for _ in range(rng.randint(0,3)):
            if rng.random()<0.2: ms.append(('promo',None))
            else:
                ys=[z for z in range(nP) if mover[z]!=mover[y]]
                if ys: ms.append(('n',rng.choice(ys)))
        moves.append(ms)
    # D game: positions (d,mover); options: ('t',0) sigma terminal,('t',1) loser terminal, ('p',d')
    dm = [rng.choice([0,1]) for _ in range(nD)]
    opts=[]
    for d in range(nD):
        o=set()
        for _ in range(rng.randint(0,3)):
            r=rng.random()
            if r<0.15: o.add(('t',0))
            elif r<0.25: o.add(('t',1))
            else:
                ds=[e for e in range(nD) if dm[e]!=dm[d]]
                if ds: o.add(('p',rng.choice(ds)))
        opts.append(o)
    pi=[rng.choice([d for d in range(nD) if dm[d]==mover[y]] or [None]) for y in range(nP)]
    if any(p is None for p in pi): return None
    # D win set with rank
    rank={}
    changed=True; n=0
    while changed:
        changed=False; n+=1; new={}
        for d in range(nD):
            if d in rank: continue
            if dm[d]==0:
                if any(o==('t',0) or (o[0]=='p' and o[1] in rank) for o in opts[d]): new[d]=n
            else:
                if all(o==('t',0) or (o[0]=='p' and o[1] in rank) for o in opts[d]): new[d]=n
        if new: rank.update(new); changed=True
    # P win set
    PW=set(); changed=True
    while changed:
        changed=False
        for y in range(nP):
            if y in PW: continue
            if mover[y]==0:
                ok=any(m[0]=='promo' or m[1] in PW for m in moves[y])
            else:
                ok=(len(moves[y])>0 or check[y]) and all(m[0]=='n' and m[1] in PW for m in moves[y])
            if ok: PW.add(y); changed=True
    N={y for y in range(nP) if pi[y] in rank}
    changed=True
    while changed:
        changed=False
        for y in list(N):
            if mover[y]==0:
                ok=any(m[0]=='promo' or m[1] in PW or (m[1] in N and ('p',pi[m[1]]) in opts[pi[y]] and rank[pi[m[1]]]<rank[pi[y]]) for m in moves[y])
            else:
                ok=(len(moves[y])>0 or check[y]) and all(m[0]=='n' and (m[1] in PW or (m[1] in N and ('p',pi[m[1]]) in opts[pi[y]])) for m in moves[y])
            if not ok: N.discard(y); changed=True
    bad = N-PW
    return len(N), len(bad)
rng=random.Random(1); tot=0; nn=0; bad=0
for _ in range(300000):
    r=trial(rng)
    if r is None: continue
    tot+=1; nn+= r[0]>0; bad+= r[1]>0
print(tot, "trials;", nn, "with nonempty certified set;", bad, "violations")
