import json, sys
rows=[]
for f in sys.argv[1:]:
    rows+=json.load(open(f))
import os
Tmax=int(os.environ.get("TMAX","5"))
n=len(rows); l1=0; viol=[]; need3=[]; need2=[]; optA=[]; safeq=[]; lc_total=0; lcA_total=0
for r in rows:
    if r['TP'] is None: continue
    l1+=1
    TP=r['TP']; muB=r['muB']; muA=r['muA']
    L3={int(k):v for k,v in r['L3'].items()}
    okT=[T for T in range(TP,Tmax+1) if muB>=T+1 and L3.get(T,(False,False))[0]]
    okA=[T for T in range(TP,Tmax+1) if muA>=T+1 and L3.get(T,(False,False))[0]]
    if okT:
        lc_total+=1
        if not r['sbar_wins']: viol.append(r)
        if okT and not okA: optA.append(r)
        if r['TQ'] is None or r['TQ']>min(okT): safeq.append(r)
    if okA: lcA_total+=1
    # (L3) needed: L1,L2 hold at T but L3 fails, not win
    if not r['sbar_wins']:
        if any(muB>=T+1 and not L3.get(T,(True,True))[0] for T in range(TP,Tmax+1)) and not okT: need3.append(r)
        if muB<=TP: need2.append(r)
print("rows",n,"L1 holds",l1,"LC holds",lc_total,"LC(optionA) holds",lcA_total)
print("VIOLATIONS",len(viol))
for v in viol[:10]: print(v)
print("need L3 (L1,L2 ok, L3 fails, not win):",len(need3))
for v in need3[:5]: print(v['Y'],v['m'],v['r'],v['Q'],v['TP'],v['muB'],v['L3'],v['P'])
print("need L2 (L1 ok, mu<=T, not win):",len(need2))
for v in need2[:5]: print(v['Y'],v['m'],v['r'],v['Q'],v['TP'],v['muB'],v['P'])
print("LC(B) holds, LC(A) fails:",len(optA))
for v in optA[:5]: print(v['Y'],v['m'],v['r'],v['Q'],v['TP'],v['muB'],v['muA'],v['P'])
print("LC_P holds but safe-queen L1 later/never:",len(safeq))
for v in safeq[:5]: print(v['Y'],v['m'],v['r'],v['Q'],v['TP'],v['TQ'],v['P'])
