# Build per-king-move table from engine/suite/results.json (tablebase truth, cached; no network).
import json,re,sys,collections
R='/Users/aritro/Downloads/Research/Chessendgames/engine/suite/'
res=json.load(open(R+'results.json'))
def ids(f): return {re.search(r'id "([^"]+)"',l).group(1) for l in open(R+f) if l.strip()}
epd=ids('cgt_verified.epd')|ids('cgt_disagree.epd')
def parse_fen(fen):
    rows=fen.split()[0].split('/'); b={}
    for ri,row in enumerate(rows):
        f=0
        for ch in row:
            if ch.isdigit(): f+=int(ch)
            else: b[(f,7-ri)]=ch; f+=1
    return b
def sq(s): return (ord(s[0])-97,int(s[1])-1)
def cheb(a,b): return max(abs(a[0]-b[0]),abs(a[1]-b[1]))
rows=[]
INF=9
def promo_dist(b,color):
    best=INF
    for (f,rk),p in b.items():
        if f>3 or p.lower()!='p' or (p=='P')!=(color=='W'): continue
        # passed: no enemy pawn on files f-1..f+1 ahead (any square strictly ahead)
        ahead=lambda r2: r2>rk if color=='W' else r2<rk
        enemy='p' if color=='W' else 'P'
        if any(q==enemy and abs(f2-f)<=1 and ahead(r2) for (f2,r2),q in b.items() if f2<=3): continue
        steps=(7-rk) if color=='W' else (rk-0)   # rk 0-indexed rank
        if (color=='W' and rk==1) or (color=='B' and rk==6): steps-=1
        best=min(best,steps)
    return best
def numval(v):
    try: return float(v)
    except: pass
    m=re.fullmatch(r'(-?\d+)/(\d+)',v)
    return int(m.group(1))/int(m.group(2)) if m else None
for x in res:
    b=parse_fen(x['fen']); stm=x['stm']
    own='K' if stm=='W' else 'k'
    kpos=[s for s,p in b.items() if p==own][0]
    okpos=[s for s,p in b.items() if p==own.swapcase()][0]
    comp=[s for s,p in b.items() if p in 'Pp' and s[0]<=3]   # component pawns: files a-d
    treb=[s for s,p in b.items() if p in 'Pp' and s[0]>=6]
    r=int(x['treb'][1])
    Rm=promo_dist(b,stm); Ro=promo_dist(b,'B' if stm=='W' else 'W'); nv=numval(x['value']['count'])
    nW=sum(1 for s_,p in b.items() if p=='P' and s_[0]<=3); nB=sum(1 for s_,p in b.items() if p=='p' and s_[0]<=3)
    enemy_pawns=[s_ for s_,p in b.items() if p in 'Pp' and s_[0]<=3 and (p=='p')==(stm=='W')]
    own_pawns=[s_ for s_,p in b.items() if p in 'Pp' and s_[0]<=3 and (p=='P')==(stm=='W')]
    okd=min(cheb(okpos,c) for c in comp)
    npred=len(x['rules']['count']['pred_win'])
    for mv,v in x['king_move_results'].items():
        to=sq(mv[2:4]); fr=sq(mv[0:2])
        dc=min(cheb(to,c) for c in comp)
        de=min(cheb(to,c) for c in enemy_pawns) if enemy_pawns else 9
        do=min(cheb(to,c) for c in own_pawns) if own_pawns else 9
        dc0=min(cheb(fr,c) for c in comp)
        rows.append(dict(id=x['id'],in_epd=x['id'] in epd,treb=x['treb'],side=stm,r=r,tier=x['tier'],root=x['tb_root'],move=mv,
            res=v,dcomp=dc,dcomp_from=dc0,approach=dc0-dc,tofile=to[0],fromfile=fr[0],
            ncomp=len(comp),maxlen=x['features']['maxlen'],nsol=x['features']['nsol'],cls=x['features']['class'],
            val=x['value']['count'],okdist=cheb(to,okpos),
            nroot_moves=len(x['tb_moves']),Rm=Rm,Ro=Ro,margin=Ro-Rm if Rm<INF or Ro<INF else 0,
            has_pass=int(Rm<INF),opp_pass=int(Ro<INF),tempo=(nv if nv is not None else 0),isnum=int(nv is not None),nW=nW,nB=nB,
            denemy=de,down=do,okd_comp=okd,npred=npred,pred_win=int(npred>0),root_ok=int(x['rules']['count']['root_agree'])))
json.dump(rows,open('data/suite_king_moves.json','w'))
print(len(rows),'king moves from',len({r['id'] for r in rows}),'positions;',sum(r['in_epd'] for r in rows),'in EPD sets')
print(collections.Counter(r['res'] for r in rows))
