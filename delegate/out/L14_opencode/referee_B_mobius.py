# Independent check of Möbius part of B. No cylcgt/lean imports.
import sys
exec(open('delegate/out/L14_opencode/referee_A.py').read().split('# ---------- witness lines ----------')[0])

# ---------- raceWinner ----------
def isFront(pos,p):
    # no pawn of either colour ahead on same file
    for q in pos.white+pos.black:
        if q[0]==p[0] and q is not p:
            if isAhead(p[2],p[1],q[1]):
                return False
    return True

def raceDistance(settings,b,pos,color):
    dists=[]
    for p in pos.pawns(color):
        if passed(settings,b,pos,color,p) and isFront(pos,p):
            # Board.distance
            d = b.ranks-p[1] if p[2] else p[1]-1
            if p[1]==homeRank(b,p[2]) and d>=2:
                d-=1
            dists.append(d)
    if not dists: return None
    return min(dists)

def leInf(a,b):
    # None as infinity
    if b is None: return True
    if a is None: return False
    return a<=b

def raceWinner(settings,b,pos,mover):
    rule=settings[1]
    if rule=='mover': return mover
    if rule=='opponent': return 'black' if mover=='white' else 'white'
    # count
    do=raceDistance(settings,b,pos,'black' if mover=='white' else 'white')
    dm=raceDistance(settings,b,pos,mover)
    if leInf(do,dm):
        return 'black' if mover=='white' else 'white'
    return mover

def verdict(settings,b,pos,mover):
    hw=hasPassed(settings,b,pos,'white'); hb=hasPassed(settings,b,pos,'black')
    if not hw and not hb: return ('open',)
    if hw and not hb: return ('decided','white')
    if (not hw) and hb: return ('decided','black')
    w=raceWinner(settings,b,pos,mover)
    return ('decided',w)  # race decided by rule (default no undefined since table total)

# ---------- WH ----------
memo={}
def WH(settings,b,fuel,pos,h,color):
    key=(settings,b.files,b.ranks,b.topology,fuel,pos.white,pos.black,pos.ep,h,color)
    if key in memo: return memo[key]
    if fuel==0:
        memo[key]=None; return None
    opts=moves(settings,b,pos,color)
    child_results=[]
    for q in opts:
        v=verdict(settings,b,q,color)
        if v[0]=='open':
            r=WH(settings,b,fuel-1,q,h,'black' if color=='white' else 'white')
            child_results.append(None if r is None else (not r))
        elif v[0]=='decided':
            w=v[1]
            child_results.append(w==color)
        else:
            child_results.append(None)
    heap_results=[]
    for i in range(h):
        r=WH(settings,b,fuel-1,pos,i,'black' if color=='white' else 'white')
        heap_results.append(None if r is None else (not r))
    allr=child_results+heap_results
    # anyOpt
    def anyOpt(lst):
        if not lst: return False
        o=lst[0]; rest=lst[1:]
        if o is True: return True
        if o is False: return anyOpt(rest)
        r=anyOpt(rest)
        if r is True: return True
        return None
    r=anyOpt(allr)
    memo[key]=r
    return r

def cls(w,b):
    if w is True and b is True: return 'N'
    if w is False and b is False: return 'P'
    if w is True and b is False: return 'L'
    if w is False and b is True: return 'R'
    return '?'

def star_outcomes(settings,b,pos,k,hmax):
    res=[]
    for h in range(hmax+1):
        w=WH(settings,b,200,pos,h,'white')
        bb=WH(settings,b,200,pos,h,'black')
        res.append((w,bb))
    return res

def sig(settings,b,pos,hmax=4):
    return ''.join(cls(w,bb) for (w,bb) in [(WH(settings,b,200,pos,h,'white'),WH(settings,b,200,pos,h,'black')) for h in range(hmax+1)])

# ---------- parse families ----------
memo.clear()
def parse_file(f,s):
    up=True; w=[]; blk=[]
    for ch in s:
        if ch=='W': up=True
        elif ch=='B': up=False
        else:
            r=int(ch)
            if up: w.append((f,r,True))
            else: blk.append((f,r,False))
    return w,blk

def of_files(fs):
    w=[]; b=[]
    for i,s in enumerate(fs):
        wi,bi=parse_file(i,s)
        w+=wi; b+=bi
    return Pos(tuple(sorted(w)),tuple(sorted(b)),None)

def rep(k,xs):
    out=[]
    for _ in range(k):
        out+=xs
    return out

def f1(m): return rep(m,["B4","W2"])+["B6","W2","W3","B6","B7","W3","B7","W5"]
def f2(m): return f1(m)+["B7"]
def f3(m): return ["B6","W2","W3","B6","B7","W3"]+rep(m,["B7","W5"])+["W6B7"]
def tt(m): return ["B5","W2","W6B7","W3","B7","B6","W3","W2","B6","W2"]+rep(m,["B4","W2"])
def ss(m): return ["B6","W3"]+rep(m,["W2","B4"])+["W6B7","W3","B7","B6","W3","W2","B6","W2","B4"]

settings=('aware','count')

# Check one family member F1 m=1
m=0
fs=f3(m)
pos=of_files(fs)
b=Board(len(fs),8,'mobius')
print("F1 m=1 width", len(fs), "pawns", len(pos.white)+len(pos.black))
print("hasPassed W/B", hasPassed(settings,b,pos,'white'), hasPassed(settings,b,pos,'black'))
outs=star_outcomes(settings,b,pos,2,4)
print("F3 m=0 outcomes h=0..4:", [( 'T' if w is True else ('F' if w is False else '?'), 'T' if bb is True else ('F' if bb is False else '?')) for (w,bb) in outs])
# star property for k=2
ok=True
for h,(w,bb) in enumerate(outs):
    want = (h!=2)
    if not (w is want and bb is want):
        ok=False
print("F3 m=0 is *2 for h=0..4:", ok)

# Controls
for name,fam,m in [("F1",f1,0),("F2",f2,0),("TT",tt,0)]:
    fs=fam(m)
    pos=of_files(fs)
    b=Board(len(fs),8,'mobius')
    s=sig(settings,b,pos,4)
    print(f"control {name} m={m} width={len(fs)} pawns={len(pos.white)+len(pos.black)} sig(0..4)={s}")
