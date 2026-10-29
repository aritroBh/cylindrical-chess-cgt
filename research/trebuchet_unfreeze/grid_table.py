import glob,os,re
names={'0':'nothing','1':'nothing','2':'Hm1','3':'Hm1','4':'Hp1','5':'Hp1','6':'H*','7':'H*','8':'H*2','9':'H*2','10':'H0','11':'H0'}
cols=['chessQ_c2','chessQ_stale1_c2','chessQ_stale2_c2','m2_Q_c2','m3_Q_c2','m4_Q_c2','P_QRBN','P_stale1','P_stale2','flat_chessQ_c2','flat_P']
def load(c):
    f=f'logs/g_{c}.txt'
    if not os.path.exists(f) or not os.path.getsize(f): return None
    out=[]
    for l in open(f):
        if l.startswith('['): continue
        out.append(l.split('|')[1].split()[0])
    return out
data={c:load(c) for c in cols}
print('context  stm | '+' '.join(f'{c[:14]:>14}' for c in cols))
ctx=['nothing','Hm1','Hp1','H*','H*2','H0']
for i in range(12):
    print(f"{ctx[i//2]:8} {'w' if i%2==0 else 'b'}   | "+' '.join(f"{(data[c][i] if data[c] else '-'):>14}" for c in cols))
