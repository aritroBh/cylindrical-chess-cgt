# Independent referee check for Part A (no cylcgt/lean imports).
# Implements a small pawn game from the paper's rules for flat 8 and cylinder 8.

from functools import lru_cache

# ---------- board ----------
class Board:
    def __init__(self, files, ranks, topology):
        self.files=files; self.ranks=ranks; self.topology=topology
    def valid(self):
        if self.topology=='flat': return True
        return self.files>=3
    def onBoard(self,r): return 1<=r<=self.ranks
    def mirror(self,r): return self.ranks+1-r
    def beside(self,f,right):
        if right:
            if f+1 < self.files: return (f+1,False)
            # across seam
            if self.topology=='flat': return None
            if self.topology=='cylinder': return (0,False)
            if self.topology=='mobius': return (0,True)
        else:
            if f>0: return (f-1,False)
            if self.topology=='flat': return None
            if self.topology=='cylinder': return (self.files-1,False)
            if self.topology=='mobius': return (self.files-1,True)
    def captureTo(self,p,right):
        b=self.beside(p[0],right)
        if b is None: return None
        g,flip=b
        r = p[1]+1 if p[2] else p[1]-1
        if not self.onBoard(r): return None
        if flip:
            return (g,self.mirror(r),not p[2])
        return (g,r,p[2])
    def captureTargets(self,p):
        out=[]
        for right in (True,False):
            t=self.captureTo(p,right)
            if t is not None: out.append(t)
        return out
    def homeRank(self,up): return 2 if up else self.ranks-1
    def distance(self,p):
        d = self.ranks-p[1] if p[2] else p[1]-1
        if p[1]==self.homeRank(p[2]) and d>=2: d-=1
        return d
    def blocks(self,p,q):
        # p pawn of color c? We'll pass p,q pawns; ahead relation depends on p.up
        def isAhead(up,r,s):
            return r<s if up else s<r
        if q[0]==p[0] and isAhead(p[2],p[1],q[1]): return True
        for right in (True,False):
            b=self.beside(p[0],right)
            if b is None: continue
            g,flip=b
            if q[0]==g:
                rr = self.mirror(q[1]) if flip else q[1]
                if isAhead(p[2],p[1],rr): return True
        return False
    def epCaptures(self,pos,owner_color,v):
        # capturers are opponent of owner_color
        capturer_color = 'black' if owner_color=='white' else 'white'
        capturers = pos.pawns(capturer_color)
        skipped=(v[0], v[1]+1 if not v[2] else v[1]-1)  # ahead(!up)
        # Wait ahead(!up, rank): if not up -> rank+1? ahead(up,r)= if up r+1 else r-1. For !up: if not up? Let's define:
        pass
    # We'll implement epCaptures separately below.

def ahead(up,r):
    return r+1 if up else r-1

def isAhead(up,r,s):
    return r<s if up else s<r

def mirror(b,r): return b.ranks+1-r

def onBoard(b,r): return 1<=r<=b.ranks

def homeRank(b,up): return 2 if up else b.ranks-1

def blocks(b,p,q):
    # p,q pawns (file,rank,up)
    def ia(up,r,s): return r<s if up else s<r
    if q[0]==p[0] and ia(p[2],p[1],q[1]): return True
    for right in (True,False):
        # beside
        if right:
            if p[0]+1 < b.files:
                g=p[0]+1; flip=False
            else:
                if b.topology=='flat': 
                    g=None
                elif b.topology=='cylinder':
                    g=0; flip=False
                else:
                    g=0; flip=True
        else:
            if p[0]>0:
                g=p[0]-1; flip=False
            else:
                if b.topology=='flat':
                    g=None
                elif b.topology=='cylinder':
                    g=b.files-1; flip=False
                else:
                    g=b.files-1; flip=True
        if g is None: continue
        rr = mirror(b,q[1]) if flip else q[1]
        if q[0]==g and ia(p[2],p[1],rr): return True
    return False

def captureTo(b,p,right):
    if right:
        if p[0]+1 < b.files:
            g=p[0]+1; flip=False
        else:
            if b.topology=='flat': return None
            if b.topology=='cylinder': g=0; flip=False
            else: g=0; flip=True
    else:
        if p[0]>0:
            g=p[0]-1; flip=False
        else:
            if b.topology=='flat': return None
            if b.topology=='cylinder': g=b.files-1; flip=False
            else: g=b.files-1; flip=True
    r=ahead(p[2],p[1])
    if not onBoard(b,r): return None
    if flip:
        return (g,mirror(b,r),not p[2])
    return (g,r,p[2])

def captureTargets(b,p):
    out=[]
    for right in (True,False):
        t=captureTo(b,p,right)
        if t is not None: out.append(t)
    # dedup? Rules may produce duplicates across seam? keep as set via tuple
    uniq=[]
    seen=set()
    for t in out:
        if t not in seen:
            seen.add(t); uniq.append(t)
    return uniq

def epCaptures(b,pos,owner_color,v):
    # capturers are opponent of owner_color
    capturer_color = 'black' if owner_color=='white' else 'white'
    capturers = pos.pawns(capturer_color)
    skipped=(v[0], ahead(not v[2], v[1]))
    out=[]
    for q in capturers:
        for t in captureTargets(b,q):
            if t[0]==skipped[0] and t[1]==skipped[1]:
                out.append((q,t))
    return out

# ---------- position ----------
class Pos:
    def __init__(self, white, black, ep=None):
        # white/black: list of (file,rank,up)
        self.white=tuple(sorted(white))
        self.black=tuple(sorted(black))
        self.ep=ep  # (file,rank) or None
    def pawns(self,color):
        return self.white if color=='white' else self.black
    def allPawns(self):
        return list(self.white)+list(self.black)
    def occupied(self,sq):
        return any((p[0],p[1])==sq for p in self.allPawns())
    def at(self,sq):
        for p in self.white:
            if (p[0],p[1])==sq: return ('white',p)
        for p in self.black:
            if (p[0],p[1])==sq: return ('black',p)
        return None

def build(b, color, mine, theirs, ep):
    # sort
    def key(p): return (p[0],p[1])
    mine_s=sorted(mine,key=key)
    theirs_s=sorted(theirs,key=key)
    if color=='white':
        return Pos(mine_s,theirs_s,ep)
    else:
        return Pos(theirs_s,mine_s,ep)

def moves(settings, b, pos, color):
    ep_rule=settings[0]; # 'off','textbook','aware'
    # settings as (ep, race) but race unused here
    mine=list(pos.pawns(color))
    theirs=list(pos.pawns('black' if color=='white' else 'white'))
    other='black' if color=='white' else 'white'
    res=[]
    seen=set()
    for p in mine:
        # step
        r1=ahead(p[2],p[1])
        if onBoard(b,r1) and not pos.occupied((p[0],r1)):
            q=build(b,color,[pp if pp!=p else (p[0],r1,p[2]) for pp in mine], theirs, None)
            # careful: replace p
            q=build(b,color,[(pp[0],pp[1],pp[2]) if pp!=p else (p[0],r1,p[2]) for pp in mine], theirs, None)
            add(q)
        # double step
        r1=ahead(p[2],p[1]); r2=ahead(p[2],r1)
        if p[1]==homeRank(b,p[2]) and onBoard(b,r1) and onBoard(b,r2) and not pos.occupied((p[0],r1)) and not pos.occupied((p[0],r2)):
            p2=(p[0],r2,p[2])
            after=build(b,color,[(pp[0],pp[1],pp[2]) if pp!=p else p2 for pp in mine], theirs, None)
            # ep condition
            ep=None
            if ep_rule!='off':
                caps=epCaptures(b,after,color,p2)
                if caps:
                    ep=(p2[0],p2[1])
            q=Pos(after.white, after.black, ep)
            add(q)
        # capture
        for t in captureTargets(b,p):
            # find enemy on t square
            enemy=[q for q in theirs if (q[0],q[1])==(t[0],t[1])]
            if enemy:
                qe=enemy[0]
                newmine=[pp for pp in mine if pp!=p]+[t]
                newtheirs=[q for q in theirs if q!=qe]
                q=build(b,color,newmine,newtheirs,None)
                add(q)
        # ep
        if pos.ep is not None:
            e=pos.ep
            # find v in theirs with sq==e
            vs=[v for v in theirs if (v[0],v[1])==e]
            if vs and ep_rule!='off':
                v=vs[0]
                # epCaptures from owner perspective: owner_color = other (color of v)
                caps=epCaptures(b,pos,other,v)
                for (qcap,tcap) in caps:
                    if qcap==p:
                        newmine=[pp for pp in mine if pp!=p]+[tcap]
                        newtheirs=[q for q in theirs if q!=v]
                        q=build(b,color,newmine,newtheirs,None)
                        add(q)
    def add(q):
        key=(q.white,q.black,q.ep)
        if key not in seen:
            seen.add(key); res.append(q)
    return res

# Need fix closure issue: define add before loop? We'll restructure by collecting then dedup.

# Rewrite moves cleanly:
def moves(settings, b, pos, color):
    ep_rule=settings[0]
    mine=list(pos.pawns(color))
    theirs=list(pos.pawns('black' if color=='white' else 'white'))
    other='black' if color=='white' else 'white'
    res=[]
    seen=set()
    def add(q):
        key=(q.white,q.black,q.ep)
        if key not in seen:
            seen.add(key); res.append(q)
    for p in mine:
        # step
        r1=ahead(p[2],p[1])
        if onBoard(b,r1) and not pos.occupied((p[0],r1)):
            newmine=[(pp[0],pp[1],pp[2]) if pp!=p else (p[0],r1,p[2]) for pp in mine]
            q=build(b,color,newmine,theirs,None)
            add(q)
        # double
        r1=ahead(p[2],p[1]); r2=ahead(p[2],r1)
        if p[1]==homeRank(b,p[2]) and onBoard(b,r1) and onBoard(b,r2) and not pos.occupied((p[0],r1)) and not pos.occupied((p[0],r2)):
            p2=(p[0],r2,p[2])
            newmine=[(pp[0],pp[1],pp[2]) if pp!=p else p2 for pp in mine]
            after=build(b,color,newmine,theirs,None)
            ep=None
            if ep_rule!='off':
                caps=epCaptures(b,after,color,p2)
                if caps:
                    ep=(p2[0],p2[1])
            q=Pos(after.white, after.black, ep)
            add(q)
        # capture
        for t in captureTargets(b,p):
            enemies=[q for q in theirs if (q[0],q[1])==(t[0],t[1])]
            if enemies:
                qe=enemies[0]
                newmine=[pp for pp in mine if pp!=p]+[t]
                newtheirs=[q for q in theirs if q!=qe]
                q=build(b,color,newmine,newtheirs,None)
                add(q)
        # ep
        if pos.ep is not None:
            e=pos.ep
            vs=[v for v in theirs if (v[0],v[1])==e]
            if vs and ep_rule!='off':
                v=vs[0]
                caps=epCaptures(b,pos,other,v)
                for (qcap,tcap) in caps:
                    if qcap==p:
                        newmine=[pp for pp in mine if pp!=p]+[tcap]
                        newtheirs=[q for q in theirs if q!=v]
                        q=build(b,color,newmine,newtheirs,None)
                        add(q)
    return res

def textbookPassed(b,pos,color,p):
    other='black' if color=='white' else 'white'
    enemies=pos.pawns(other)
    return all(not blocks(b,p,q) for q in enemies)

def epCapturable(b,pos,color,p):
    # color owner of p
    if pos.ep != (p[0],p[1]): return False
    other='black' if color=='white' else 'white'
    # enemy is other? capturers are opponent of owner = other? Wait owner color; capturers are other color (opponent)
    caps=epCaptures(b,pos,color,p)  # owner color passed as owner_color
    return len(caps)>0

def passed(settings, b, pos, color, p):
    ep_rule=settings[0]
    tp=textbookPassed(b,pos,color,p)
    if ep_rule=='aware':
        if epCapturable(b,pos,color,p):
            return False
    return tp

def hasPassed(settings,b,pos,color):
    return any(passed(settings,b,pos,color,p) for p in pos.pawns(color))

def components(b,pos):
    occ=[f for f in range(b.files) if any(p[0]==f for p in pos.allPawns())]
    # runs
    groups=[]
    for f in occ:
        if not groups or groups[-1][-1]+1 != f:
            groups.append([f])
        else:
            groups[-1].append(f)
    # seam merge if topology != flat
    if b.topology!='flat' and len(groups)>=2:
        first=groups[0]; last=groups[-1]
        if first and first[0]==0 and last and last[-1]==b.files-1:
            merged=last+first
            groups= [merged] + groups[1:-1]
    def restrict(fs):
        w=[p for p in pos.white if p[0] in fs]
        blk=[p for p in pos.black if p[0] in fs]
        ep=pos.ep if (pos.ep is not None and pos.ep[0] in fs) else None
        return Pos(w,blk,ep)
    return [restrict(g) for g in groups]

def verdict(settings,b,pos,mover):
    # returns 'open','decided_white','decided_black','undefined'
    hw=hasPassed(settings,b,pos,'white')
    hb=hasPassed(settings,b,pos,'black')
    if not hw and not hb: return ('open',)
    if hw and not hb: return ('decided','white')
    if (not hw) and hb: return ('decided','black')
    # race
    # raceWinner needed; for undefined races we always undefined in this check? 
    # For posG races are undecided by table; env race none -> undefined.
    return ('undefined',)

# For independent check of 1/8, races are undefined always.
def verdict_undef(settings,b,pos,mover):
    hw=hasPassed(settings,b,pos,'white'); hb=hasPassed(settings,b,pos,'black')
    if not hw and not hb: return ('open',)
    if hw and not hb: return ('decided','white')
    if (not hw) and hb: return ('decided','black')
    return ('undefined',)

# ---------- trees ----------
def T_zero(): return ('node',[],[])
def T_star(k):
    stars=[T_star(i) for i in range(k)]
    return ('node', list(stars), list(stars))
def T_dy(k):
    if k==0:
        return ('node',[T_zero()],[])
    return ('node',[T_zero()],[T_dy(k-1)])
def T_neg(t):
    L,R=t[1],t[2]
    return ('node',[T_neg(x) for x in R],[T_neg(x) for x in L])

T_eighth=T_dy(3)
T_neg_eighth=T_neg(T_eighth)

# ---------- comp options ----------
BIG=256
def comp_options(settings,b,c,comp,env_race_none=True):
    # comp: ('num',n) or ('tree',t) or ('pawns',pos)
    if comp[0]=='num':
        n=comp[1]
        if c=='white':
            if n>0: return [ [('num',n-1)] ]
            return []
        else:
            if n<0: return [ [('num',n+1)] ]
            return []
    if comp[0]=='tree':
        t=comp[1]
        L,R=t[1],t[2]
        opts = L if c=='white' else R
        return [ [('tree',x)] for x in opts ]
    if comp[0]=='pawns':
        pos=comp[1]
        opts_pos=moves(settings,b,pos,c)
        out=[]
        for q in opts_pos:
            v=verdict_undef(settings,b,q,c)
            if v[0]=='open':
                comps=components(b,q)
                out.append([('pawns',pp) for pp in comps])
            elif v[0]=='decided':
                w=v[1]
                if w=='white':
                    out.append([('num',BIG)])
                else:
                    out.append([('num',-BIG)])
            else:
                out.append(None)
        return out
    raise Exception(comp)

def sum_options(settings,b,c,comps):
    # comps list of comp
    if not comps:
        return []
    x=comps[0]; xs=comps[1:]
    opts_x=comp_options(settings,b,c,x)
    # map append xs
    res=[ (o if o is None else o+ [ ('pawns' if False else cc) for cc in [] ] ) for o in [] ]  # placeholder
    # proper:
    res=[]
    for o in opts_x:
        if o is None:
            res.append(None)
        else:
            res.append(list(o)+[('wrap',cc) for cc in []])  # no
    # Let's do simpler: represent components as tuples; append xs comps objects.
    res=[]
    for o in opts_x:
        if o is None:
            res.append(None)
        else:
            res.append(list(o)+list(xs))
    # plus moves in xs
    rest=sum_options(settings,b,c,xs)
    for o in rest:
        if o is None:
            res.append(None)
        else:
            res.append([comps[0]]+list(o))
    return res

# Wait sum_options should map each xs option by prepending x. Above rest already includes x? Need follow Game.Sum.options:
# (x.options).map (·.map (· ++ xs)) ++ (Sum.options xs).map (·.map (x :: ·))
# So first part: x move -> option list (move comps) ++ xs. second: xs move -> x :: moved xs.
# Our first loop did o+xs (good). second loop should prepend comps[0] to o (good). But xs move o is list of comps for xs after move; prepend original x. Good.

def anyOpt(lst):
    # lst: list of Option Bool (None or bool)
    # returns None/True/False as Python None/True/False? Use None for unknown, True/False
    # anyOpt [] = some false
    if not lst:
        return False
    o=lst[0]
    rest=lst[1:]
    if o is True:
        return True
    if o is False:
        return anyOpt(rest)
    # None
    r=anyOpt(rest)
    if r is True:
        return True
    return None

# memoized wins
from functools import lru_cache

def _tkey(t):
    if isinstance(t, list):
        return tuple(_tkey(x) for x in t)
    if isinstance(t, tuple):
        return tuple(_tkey(x) for x in t)
    return t
def comp_key(c):
    if c[0]=='pawns':
        p=c[1]
        return ('pawns', p.white, p.black, p.ep)
    if c[0]=='tree':
        return ('tree', _tkey(c[1]))
    return tuple(_tkey(x) for x in c)

def wins(settings, b, fuel, comps, color):
    # comps: list or tuple of comp objects
    comps_t=tuple(comps)
    try:
        _ck=tuple(comp_key(c) for c in comps_t)
    except Exception as e:
        print('comp_key error',e,[type(c) for c in comps_t])
        raise
    key=(settings, b.files, b.ranks, b.topology, fuel, _ck, color)
    if key in _memo: return _memo[key]
    if fuel==0:
        _memo[key]=None; return None
    comps_list=list(comps_t)
    opts=sum_options(settings,b,color,comps_list)
    child_results=[]
    for o in opts:
        if o is None:
            child_results.append(None)
        else:
            ct=list(o)
            r=wins(settings,b,fuel-1,ct,'black' if color=='white' else 'white')
            if r is None:
                child_results.append(None)
            else:
                child_results.append(not r)
    r=anyOpt(child_results)
    _memo[key]=r
    return r

def normalize_comp(c):
    if c[0]=='pawns':
        p=c[1]
        return ('pawns', p.white, p.black, p.ep)
    if c[0]=='wrap':
        # shouldn't happen
        return c
    return tuple(c)

_memo={}

def comp_of_position(settings,b,pos):
    cs=components(b,pos)
    return tuple(('pawns', pp) for pp in cs)

def outcome(settings,b,fuel,pos,t,color):
    comps=list(comp_of_position(settings,b,pos))+[('tree',t)]
    return wins(settings,b,fuel,comps,color)

def isValue(settings,b,fuel,pos,v):
    if hasPassed(settings,b,pos,'white') or hasPassed(settings,b,pos,'black'):
        return False
    o1=outcome(settings,b,fuel,pos,v,color='white')  # X + (-v), white to move
    # Wait outcome(pos, neg v): wins X + (-v). isValue uses outcome e fuel pos v.neg c.
    # our outcome takes t and computes X + t. Pass neg v.
    o_white=outcome(settings,b,fuel,pos,T_neg(v),'white')
    o_black=outcome(settings,b,fuel,pos,T_neg(v),'black')
    return (o_white is False) and (o_black is False)

# ---------- settings ----------
# settings as (ep, race) but race unused (undefined)
def all_settings():
    for ep in ('aware','textbook','off'):
        for race in ('count','mover','opponent'):
            yield (ep,race)

# ---------- positions ----------
def P(white,black,ep=None):
    return Pos(tuple(sorted(white)), tuple(sorted(black)), ep)

def sq(f,r): return (f,r)  # file 0-based? We'll use file letters converted.

def of_squares(w,b):
    # w,b list of (fileIndex, rank)
    white=[(f,r,True) for (f,r) in w]
    black=[(f,r,False) for (f,r) in b]
    return Pos(tuple(sorted(white)), tuple(sorted(black)), None)

flat8=Board(8,8,'flat')
cyl8=Board(8,8,'cylinder')

# posG: W a2 b2 b3 / B a5 a6 b6  (files a=0,b=1)
posG=of_squares([(0,2),(1,2),(1,3)],[(0,5),(0,6),(1,6)])

print("posG components:", [ (c.white,c.black,c.ep) for c in components(flat8,posG)])

# Check 1/8 for all settings with race undefined (verdict_undef already)
for s in all_settings():
    val=isValue(s,flat8,40,posG,T_dy(3))
    print("setting",s,"isValue 1/8:",val)

# ---------- witness lines ----------
env_settings=('off','count')
def lineOK(settings,b,pos,steps):
    # steps list of (color, qpos)
    cur=pos
    for (c,q) in steps:
        if hasPassed(settings,b,cur,'white') or hasPassed(settings,b,cur,'black'):
            return False
        ms=moves(settings,b,cur,c)
        if not any((mm.white,mm.black,mm.ep)==(q.white,q.black,q.ep) for mm in ms):
            return False
        cur=q
    return True

# positions from L6
def pos_from_sqs(w,b,ep=None):
    white=[(ord(x[0])-97, int(x[1:]), True) for x in w] if False else None

# Use tuples directly
def Sq(f,r): return (f,r)
# L6 positions:
posX=Pos(((1,2,True),(3,4,True),(6,3,True),(7,5,True)), ((0,7,False),(2,7,False),(5,7,False),(6,4,False)), None)
# Actually Pos expects sorted tuples of pawns; above lists are (file,rank,up). Need sort.
def mkpos(w,b,ep=None):
    ws=sorted(w); bs=sorted(b)
    return Pos(tuple(ws),tuple(bs),ep)
posX=mkpos([(1,2,True),(3,4,True),(6,3,True),(7,5,True)],
           [(0,7,False),(2,7,False),(5,7,False),(6,4,False)])
x1=mkpos([(1,2,True),(3,4,True),(6,3,True),(7,6,True)],
          [(0,7,False),(2,7,False),(5,7,False),(6,4,False)])
x2=mkpos([(1,2,True),(3,4,True),(6,3,True)],
          [(7,6,False),(2,7,False),(5,7,False),(6,4,False)])
bd=mkpos([(1,2,True),(3,4,True)],[(2,7,False)])
bd1=mkpos([(1,2,True),(3,5,True)],[(2,7,False)])
bd2=mkpos([(1,2,True),(3,5,True)],[(2,5,False)])
fh=mkpos([(6,3,True)],[(5,7,False),(6,4,False),(7,6,False)])
fh1=mkpos([(6,3,True)],[(5,5,False),(6,4,False),(7,6,False)])
fh2=mkpos([(6,3,True)],[(5,4,False),(6,4,False),(7,6,False)])
fh3=mkpos([(6,3,True)],[(5,3,False),(6,4,False),(7,6,False)])
fhr1=mkpos([(6,3,True)],[(5,7,False),(6,4,False),(7,5,False)])
fhr2=mkpos([(6,3,True)],[(5,7,False),(6,4,False),(7,4,False)])
fhr3=mkpos([(7,4,True)],[(5,7,False),(6,4,False)])

print("posX moves white:", len(moves(env_settings,cyl8,posX,'white')))
print("x1 candidate in moves:", x1 in moves(env_settings,cyl8,posX,'white'))
for q in moves(env_settings,cyl8,posX,'white'):
    if q.white==x1.white and q.black==x1.black:
        print("found x1 with ep", q.ep)
print("posX hasPassed", hasPassed(env_settings,cyl8,posX,'white'), hasPassed(env_settings,cyl8,posX,'black'))
print("posX open both?", not hasPassed(env_settings,cyl8,posX,'white') and not hasPassed(env_settings,cyl8,posX,'black'))
print("x2 components:", [(c.white,c.black) for c in components(cyl8,x2)])
print("way_in lineOK:", lineOK(env_settings,cyl8,posX,[('white',x1),('black',x2)]))
print("x2 no passed W/B:", not hasPassed(env_settings,cyl8,x2,'white'), not hasPassed(env_settings,cyl8,x2,'black'))
print("bd threat:", lineOK(env_settings,cyl8,bd,[('white',bd1),('black',bd2)]),
      "bd2 W passed:", hasPassed(env_settings,cyl8,bd2,'white'), "B passed:", hasPassed(env_settings,cyl8,bd2,'black'))
print("fh threat:", lineOK(env_settings,cyl8,fh,[('black',fh1),('black',fh2),('black',fh3)]),
      "fh3 B passed:", hasPassed(env_settings,cyl8,fh3,'black'), "W passed:", hasPassed(env_settings,cyl8,fh3,'white'))
print("fh race line:", lineOK(env_settings,cyl8,fh,[('black',fhr1),('black',fhr2),('white',fhr3)]),
      "fhr3 B passed:", hasPassed(env_settings,cyl8,fhr3,'black'), "W passed:", hasPassed(env_settings,cyl8,fhr3,'white'))
