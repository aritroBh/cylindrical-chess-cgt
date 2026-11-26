import sys, functools

# Colors
W = 0
B = 1
def other(c): return 1-c
COLOR_NAME = {0:'W',1:'B'}

TOPO_FLAT=0; TOPO_CYL=1; TOPO_MOB=2

class Board:
    def __init__(self, files, ranks=8, topo=TOPO_FLAT):
        self.files=files; self.ranks=ranks; self.topo=topo
    def onBoard(self,r): return 1<=r<=self.ranks
    def mirror(self,r): return self.ranks+1-r
    def homeRank(self,up): return 2 if up else self.ranks-1
    def beside(self,f,right):
        if right:
            if f+1 < self.files: return (f+1,False)
            if self.topo==TOPO_FLAT: return None
            if self.topo==TOPO_CYL: return (0,False)
            if self.topo==TOPO_MOB: return (0,True)
        else:
            if 0 < f: return (f-1,False)
            if self.topo==TOPO_FLAT: return None
            if self.topo==TOPO_CYL: return (self.files-1,False)
            if self.topo==TOPO_MOB: return (self.files-1,True)
    def captureTo(self,p,right):
        res=self.beside(p[0],right)
        if res is None: return None
        g,flip=res
        up=p[2]
        r = p[1]+1 if up else p[1]-1
        if not self.onBoard(r): return None
        if flip:
            return (g, self.mirror(r), not up)
        else:
            return (g, r, up)
    def captureTargets(self,p):
        out=[]
        for right in (True,False):
            t=self.captureTo(p,right)
            if t is not None: out.append(t)
        return out
    def epCaptures(self,pos,c,v):
        # c is color of v (double stepper); capturers are other(c)
        skipped=(v[0], v[1]+1 if (not v[2]) else v[1]-1)  # ahead(!v.up, v.rank)
        # ahead(up,r): if up r+1 else r-1; !v.up
        upv = not v[2]
        skipped_rank = v[1]+1 if upv else v[1]-1
        skipped=(v[0], skipped_rank)
        capturers = pos.pawns(other(c))
        out=[]
        for q in capturers:
            for t in self.captureTargets(q):
                if t[0]==skipped[0] and t[1]==skipped[1]:
                    out.append((q,t))
        return out
    def blocks(self,p,q):
        # p owned by mover, q enemy
        up=p[2]
        # same file ahead
        if q[0]==p[0]:
            if (p[1] < q[1]) if up else (q[1] < p[1]):
                return True
        for right in (True,False):
            res=self.beside(p[0],right)
            if res is None: continue
            g,flip=res
            if q[0]!=g: continue
            qr = self.mirror(q[1]) if flip else q[1]
            if (p[1] < qr) if up else (qr < p[1]):
                return True
        return False
    def distance(self,p):
        up=p[2]
        if up:
            d=self.ranks-p[1]
        else:
            d=p[1]-1
        home=self.homeRank(up)
        if p[1]==home and d>=2:
            d=d-1
        return d
    def components(self,pos):
        occ=[f for f in range(self.files) if any(p[0]==f for p in (pos.white+pos.black))]
        # runs
        groups=[]
        for f in occ:
            if groups and groups[-1] and groups[-1][-1]==f-1:
                groups[-1].append(f)
            else:
                groups.append([f])
        # merge across seam for non-flat
        if self.topo!=TOPO_FLAT and len(groups)>=2:
            first=groups[0]; last=groups[-1]
            if first and first[0]==0 and last and last[-1]==self.files-1:
                merged=last+first
                groups=[merged]+groups[1:-1]
        out=[]
        for g in groups:
            fs=set(g)
            w=[p for p in pos.white if p[0] in fs]
            b=[p for p in pos.black if p[0] in fs]
            ep = pos.ep if (pos.ep is not None and pos.ep[0] in fs) else None
            out.append(Position(w,b,ep,self))
        return out

def ahead(up,r):
    return r+1 if up else r-1

def isAhead(up,r,s):
    return r < s if up else s < r

class Position:
    def __init__(self, white, black, ep=None, board=None):
        # white/black lists of (file,rank,up)
        self.white=sorted(white)
        self.black=sorted(black)
        self.ep=ep
        self.board=board
    @property
    def white(self): return self._white
    @white.setter
    def white(self,v): self._white=sorted(v)
    @property
    def black(self): return self._black
    @black.setter
    def black(self,v): self._black=sorted(v)
    def pawns(self,c):
        return self.white if c==W else self.black
    def occupied(self,sq):
        return any(p[0]==sq[0] and p[1]==sq[1] for p in (self.white+self.black))
    def at(self,sq):
        for p in self.white:
            if p[0]==sq[0] and p[1]==sq[1]: return (W,p)
        for p in self.black:
            if p[0]==sq[0] and p[1]==sq[1]: return (B,p)
        return None
    def restrict(self,fs):
        fs=set(fs)
        w=[p for p in self.white if p[0] in fs]
        b=[p for p in self.black if p[0] in fs]
        ep=self.ep if (self.ep is not None and self.ep[0] in fs) else None
        return Position(w,b,ep,self.board)
    def key(self):
        return (tuple(self.white), tuple(self.black), self.ep)

def sort_pawns(ps):
    return sorted(ps)

def build_pos(c, mine, theirs, ep, board):
    m=sorted(mine); t=sorted(theirs)
    if c==W:
        return Position(m,t,ep,board)
    else:
        return Position(t,m,ep,board)

def Position_ofSquares(w,b,board):
    white=[(sq[0],sq[1],True) for sq in w]
    black=[(sq[0],sq[1],False) for sq in b]
    return Position(white,black,None,board)

# Square helper
def sqr(letter, rank):
    return (ord(letter)-ord('a'), rank)

def other(c): return 1-c

# Settings as tuple (ep, race)
# ep: 'off','textbook','aware'; race: 'count','mover','opponent'
DEFAULT_SETTINGS = ('aware','count')

def hasPassed(s,b,pos,c):
    for p in pos.pawns(c):
        if passed(s,b,pos,c,p):
            return True
    return False

def textbookPassed(b,pos,c,p):
    opp=other(c)
    for q in pos.pawns(opp):
        if b.blocks(p,q):
            return False
    return True

def epCapturable(b,pos,c,p):
    # c owner of p
    if pos.ep is None: return False
    if pos.ep != p[0:2]: return False
    caps = b.epCaptures(pos,c,p)
    return len(caps)>0

def passed(s,b,pos,c,p):
    tp = textbookPassed(b,pos,c,p)
    if not tp: return False
    if s[0]=='aware' and epCapturable(b,pos,c,p):
        return False
    return True

def isFront(pos,p):
    for q in (pos.white+pos.black):
        if q[0]==p[0] and isAhead(p[2], p[1], q[1]):
            return False
    return True

def raceDistance(s,b,pos,c):
    ds=[]
    for p in pos.pawns(c):
        if passed(s,b,pos,c,p) and isFront(pos,p):
            ds.append(b.distance(p))
    if not ds: return None
    return min(ds)

def leInf(a,b):
    # None = infinity
    if b is None: return True
    if a is None: return False
    return a<=b

def raceWinner(s,b,pos,mover):
    race=s[1]
    if race=='mover': return mover
    if race=='opponent': return other(mover)
    # count
    d_other = raceDistance(s,b,pos,other(mover))
    d_mover = raceDistance(s,b,pos,mover)
    if leInf(d_other, d_mover):
        return other(mover)
    else:
        return mover

def classify(s,b,pos,mover):
    wp=hasPassed(s,b,pos,W)
    bp=hasPassed(s,b,pos,B)
    if not wp and not bp: return ('open',)
    if wp and not bp: return ('decided',W)
    if (not wp) and bp: return ('decided',B)
    # both
    w=raceWinner(s,b,pos,mover)
    return ('decided',w)

def moves(s,b,pos,c):
    out=set()
    opp=other(c)
    for p in pos.pawns(c):
        # step
        r1 = ahead(p[2], p[1])
        if b.onBoard(r1) and not pos.occupied((p[0],r1)):
            mine=[x for x in pos.pawns(c) if x!=p]+[(p[0],r1,p[2])]
            newp=build_pos(c, mine, pos.pawns(opp), None, b)
            out.add(newp.key() and newp or newp)
        # double
        r1=ahead(p[2],p[1])
        r2=ahead(p[2],r1)
        home=b.homeRank(p[2])
        if p[1]==home and b.onBoard(r1) and b.onBoard(r2) and not pos.occupied((p[0],r1)) and not pos.occupied((p[0],r2)):
            p2=(p[0],r2,p[2])
            mine=[x for x in pos.pawns(c) if x!=p]+[p2]
            after=build_pos(c, mine, pos.pawns(opp), None, b)
            ep=None
            if s[0]!='off':
                caps=b.epCaptures(after,c,p2)
                if len(caps)>0:
                    ep=p2[0:2]
            after2=Position(list(after.white), list(after.black), ep, b)
            # rebuild sorted via Position constructor already sorts
            out.add(after2)
        # capture
        for t in b.captureTargets(p):
            # enemy on t
            enemies=pos.pawns(opp)
            q=None
            for e in enemies:
                if e[0]==t[0] and e[1]==t[1]:
                    q=e; break
            if q is not None:
                mine=[x for x in pos.pawns(c) if x!=p]+[t]
                theirs=[x for x in enemies if x!=q]
                newp=build_pos(c, mine, theirs, None, b)
                out.add(newp)
        # ep
        if pos.ep is not None:
            e=pos.ep
            enemies=pos.pawns(opp)
            v=None
            for en in enemies:
                if en[0]==e[0] and en[1]==e[1]:
                    v=en; break
            if v is not None and s[0]!='off':
                caps=b.epCaptures(pos, opp, v)  # c.owner? v owned by opp; epCaptures(b,pos,color_of_v=v's color=opp, v)
                # Wait epCaptures signature (pos, c, v) where c is color of v. v owned by opp. So c=opp.
                # But earlier formula Board.epCaptures(b,pos,c,v) with c=color of v. Here v owned by opp, so c=opp. Good.
                for (q,t) in caps:
                    if q==p:
                        mine=[x for x in pos.pawns(c) if x!=p]+[t]
                        theirs=[x for x in enemies if x!=v]
                        newp=build_pos(c, mine, theirs, None, b)
                        out.add(newp)
    # Convert set of Position to list; but set needs hashable. Position not hashable. Use key dedup.
    # We'll dedup by key.
    seen=set()
    res=[]
    for p in out:
        k=p.key()
        if k in seen: continue
        seen.add(k)
        res.append(p)
    return res

# Note: in moves, 'out' contains Position objects; set() failed? We used set() on Position -> error. Let's fix: use list+dedup.
# Rewrite moves cleanly:

def moves(s,b,pos,c):
    out=[]
    opp=other(c)
    seen=set()
    def add(newp):
        k=newp.key()
        if k in seen: return
        seen.add(k)
        out.append(newp)
    for p in pos.pawns(c):
        # step
        r1 = ahead(p[2], p[1])
        if b.onBoard(r1) and not pos.occupied((p[0],r1)):
            mine=[x for x in pos.pawns(c) if x!=p]+[(p[0],r1,p[2])]
            newp=build_pos(c, mine, pos.pawns(opp), None, b)
            add(newp)
        # double
        r1=ahead(p[2],p[1])
        r2=ahead(p[2],r1)
        home=b.homeRank(p[2])
        if p[1]==home and b.onBoard(r1) and b.onBoard(r2) and not pos.occupied((p[0],r1)) and not pos.occupied((p[0],r2)):
            p2=(p[0],r2,p[2])
            mine=[x for x in pos.pawns(c) if x!=p]+[p2]
            after=build_pos(c, mine, pos.pawns(opp), None, b)
            ep=None
            if s[0]!='off':
                caps=b.epCaptures(after,c,p2)
                if len(caps)>0:
                    ep=p2[0:2]
            after2=Position(list(after.white), list(after.black), ep, b)
            add(after2)
        # capture
        for t in b.captureTargets(p):
            enemies=pos.pawns(opp)
            q=None
            for e in enemies:
                if e[0]==t[0] and e[1]==t[1]:
                    q=e; break
            if q is not None:
                mine=[x for x in pos.pawns(c) if x!=p]+[t]
                theirs=[x for x in enemies if x!=q]
                newp=build_pos(c, mine, theirs, None, b)
                add(newp)
        # ep
        if pos.ep is not None:
            e=pos.ep
            enemies=pos.pawns(opp)
            v=None
            for en in enemies:
                if en[0]==e[0] and en[1]==e[1]:
                    v=en; break
            if v is not None and s[0]!='off':
                caps=b.epCaptures(pos, opp, v)
                for (q,t) in caps:
                    if q==p:
                        mine=[x for x in pos.pawns(c) if x!=p]+[t]
                        theirs=[x for x in enemies if x!=v]
                        newp=build_pos(c, mine, theirs, None, b)
                        add(newp)
    return out

# epCaptures method on Board needs fix: implement as function
def epCaptures_func(b,pos,c,v):
    upv = not v[2]
    skipped_rank = v[1]+1 if upv else v[1]-1
    skipped=(v[0], skipped_rank)
    capturers = pos.pawns(other(c)) if False else pos.pawns(other(c))
    # c is color of v; capturers are other(c)
    capturers = pos.pawns(1-c) if c==0 else pos.pawns(0)  # other
    # simpler:
    capturers = pos.pawns(W if c==B else B)
    out=[]
    for q in capturers:
        for t in b.captureTargets(q):
            if t[0]==skipped[0] and t[1]==skipped[1]:
                out.append((q,t))
    return out

# monkeypatch
Board.epCaptures = lambda self,pos,c,v: epCaptures_func(self,pos,c,v)

# classify verdict
def verdict(s,b,pos,mover):
    # returns string
    wp=hasPassed(s,b,pos,W)
    bp=hasPassed(s,b,pos,B)
    if not wp and not bp: return ('open',)
    if wp and not bp: return ('decided',W)
    if (not wp) and bp: return ('decided',B)
    w=raceWinner(s,b,pos,mover)
    return ('decided',w)

# normalize not needed

# comp helpers
def components_list(b,pos):
    return b.components(pos)

def restrict(pos,fs):
    return pos.restrict(fs)

# Tree helpers
def neg_tree(t):
    # t tuple ('node', left_tuple, right_tuple)
    left = tuple(neg_tree(x) for x in t[2])  # right becomes left
    right = tuple(neg_tree(x) for x in t[1])
    return ('node', left, right)

ZERO = ('node', (), ())
def stars_list(k):
    if k==0: return []
    return stars_list(k-1)+[star(k-1)]
def star(k):
    ch=tuple(stars_list(k))
    return ('node', ch, ch)
def dy(k):
    if k==0:
        return ('node', (ZERO,), ())
    return ('node', (ZERO,), (dy(k-1),))
EIGHTH = dy(3)

def tree_children(t,c):
    return t[1] if c==W else t[2]

# Comp as tuple
def comp_pawns(pos): return ('pawns', pos)
def comp_num(n): return ('num', n)
def comp_tree(t): return ('tree', t)

def norm_cs(cs):
    n=0
    rest=[]
    for c in cs:
        if c[0]=='num':
            n+=c[1]
        elif c[0]=='tree' and c[1][1]==() and c[1][2]==():
            # zero tree node [] [] -> drop
            continue
        else:
            rest.append(c)
    if n!=0:
        rest=rest+[('num',n)]
    return tuple(rest)

def sum_options(e, c, cs):
    # cs list of comps
    cs=list(cs)
    out=[]
    for i,x in enumerate(cs):
        opts_x = comp_options(e,c,x)
        for o in opts_x:
            if o is None:
                out.append(None)
            else:
                # prepend others
                others = cs[:i]+cs[i+1:]
                newcs = o + others
                out.append(newcs)
    # also moves in other components handled by recursion over i; above loops i covers all
    # Wait need include moves in each component; yes i loop.
    return out

def comp_options(e,c,comp):
    s=e[0]; b=e[1]; big=e[2]; racefn=e[3]
    env=(s,b,big,racefn)
    if comp[0]=='num':
        n=comp[1]
        if c==W:
            if n>0: return [[('num',n-1)]]
            return []
        else:
            if n<0: return [[('num',n+1)]]
            return []
    if comp[0]=='tree':
        t=comp[1]
        ch = t[1] if c==W else t[2]
        return [[('tree',cc)] for cc in ch]
    if comp[0]=='pawns':
        pos=comp[1]
        res=[]
        for q in moves(s,b,pos,c):
            v=verdict(s,b,q,c)  # q reached by move of c
            # verdict returns ('open',) or ('decided', color)
            if v[0]=='open':
                comps=[('pawns', pp) for pp in b.components(q)]
                res.append(comps)
            elif v[0]=='decided':
                w=v[1]
                if w==W:
                    res.append([('num',big)])
                else:
                    res.append([('num',-big)])
            else:
                res.append(None)
        # return list of options (each None or list comps)
        return res
    raise Exception('bad comp')

# Need verdict returns for q reached by mover c; classify uses mover c. But classify signature (s,b,pos,mover). Here pos=q, mover=c.
def verdict(s,b,pos,mover):
    v=classify(s,b,pos,mover)
    return v

# Fix classify returns ('open',) or ('decided', color)
def classify(s,b,pos,mover):
    wp=hasPassed(s,b,pos,W)
    bp=hasPassed(s,b,pos,B)
    if not wp and not bp: return ('open',)
    if wp and not bp: return ('decided',W)
    if (not wp) and bp: return ('decided',B)
    w=raceWinner(s,b,pos,mover)
    return ('decided',w)

# Env as tuple (s,b,big,racefn). racefn(pos,mover)->color or None
def make_env(s,b,big=256,race_table=None):
    if race_table is None:
        def rf(pos,mover): return raceWinner(s,b,pos,mover)
    else:
        def rf(pos,mover):
            # lookup in table list of ((poskey,mover), color)
            key=(pos.key(), mover)
            for (k,col) in race_table:
                if k==key:
                    return col
            return None
    return (s,b,big,rf)

def env_verdict(e,pos,mover):
    s,b,big,rf=e
    wp=hasPassed(s,b,pos,W)
    bp=hasPassed(s,b,pos,B)
    if not wp and not bp: return ('open',)
    if wp and not bp: return ('decided',W)
    if (not wp) and bp: return ('decided',B)
    w=rf(pos,mover)
    if w is None: return ('undefined',)
    return ('decided',w)

# Reimplement comp_options using env_verdict
def comp_options(e,c,comp):
    s,b,big,rf=e
    if comp[0]=='num':
        n=comp[1]
        if c==W:
            if n>0: return [[('num',n-1)]]
            return []
        else:
            if n<0: return [[('num',n+1)]]
            return []
    if comp[0]=='tree':
        t=comp[1]
        ch = t[1] if c==W else t[2]
        return [[('tree',cc)] for cc in ch]
    if comp[0]=='pawns':
        pos=comp[1]
        res=[]
        for q in moves(s,b,pos,c):
            v=env_verdict(e,q,c)
            if v[0]=='open':
                comps=[('pawns', pp) for pp in b.components(q)]
                res.append(comps)
            elif v[0]=='decided':
                w=v[1]
                if w==W:
                    res.append([('num',big)])
                else:
                    res.append([('num',-big)])
            else:
                res.append(None)
        return res
    raise Exception('bad comp')

def sum_options(e,c,cs):
    cs=list(cs)
    out=[]
    for i,x in enumerate(cs):
        opts_x=comp_options(e,c,x)
        for o in opts_x:
            if o is None:
                out.append(None)
            else:
                others=cs[:i]+cs[i+1:]
                out.append(list(o)+list(others))
    return out

# memoized wins
def wins(e, fuel, cs, c, memo):
    s,b,big,rf=e
    cs=norm_cs(cs)
    key=(cs,c)
    if key in memo:
        return memo[key]
    if fuel==0:
        return None
    opts=sum_options(e,c,cs)
    results=[]
    for o in opts:
        if o is None:
            results.append(None)
            continue
        r=wins(e,fuel-1,o,other(c),memo)
        if r is None:
            results.append(None)
        else:
            results.append(not r)
    # anyOpt
    ao=None
    has_true=False
    all_false=True
    unknown=False
    for r in results:
        if r is True:
            has_true=True
            all_false=False
        elif r is False:
            pass
        else:
            all_false=False
            unknown=True
    if has_true:
        ao=True
    elif len(results)==0:
        ao=False
    elif unknown:
        ao=None
    else:
        # all false
        ao=False
    if ao is not None:
        memo[key]=ao
    return ao

def isValue(e,fuel,pos,v):
    s,b,big,rf=e
    if hasPassed(s,b,pos,W) or hasPassed(s,b,pos,B):
        return False
    cs=list(b.components(pos)) if False else None
    # comps of pos
    comps=[('pawns',pp) for pp in b.components(pos)]
    vn=neg_tree(v)
    csW=comps+[('tree',vn)]
    csB=list(csW)
    memo={}
    ow=wins(e,fuel,csW,W,memo)
    memo2={}
    ob=wins(e,fuel,csB,B,memo2)
    return (ow is False) and (ob is False)

def notValue(e,fuel,pos,v):
    s,b,big,rf=e
    comps=[('pawns',pp) for pp in b.components(pos)]
    vn=neg_tree(v)
    cs=comps+[('tree',vn)]
    memo={}
    ow=wins(e,fuel,cs,W,memo)
    memo2={}
    ob=wins(e,fuel,cs,B,memo2)
    return (ow is True) or (ob is True)

# W whole-board
def Wfun(e,fuel,pos,c,memo):
    s,b,big,rf=e
    key=(pos.key(),c)
    if key in memo: return memo[key]
    if fuel==0:
        return None
    moves_list=moves(s,b,pos,c)
    res_win=False
    unknown=False
    for q in moves_list:
        v=env_verdict(e,q,c)
        if v[0]=='open':
            sub=Wfun(e,fuel-1,q,other(c),memo)
            if sub is None:
                unknown=True
            else:
                if not sub:
                    res_win=True; break
        elif v[0]=='decided':
            w=v[1]
            if w==c:
                res_win=True; break
        else:
            unknown=True
    if res_win:
        out=True
    elif unknown:
        out=None
    else:
        out=False
    if out is not None:
        memo[key]=out
    return out

def wholeBoard(e,fuel,pos,c):
    memo={}
    return Wfun(e,fuel,pos,c,memo)

def Sfun(e,fuel,pos,c):
    s,b,big,rf=e
    comps=[('pawns',pp) for pp in b.components(pos)]
    memo={}
    return wins(e,fuel,comps,c,memo)

# raceKeys BFS
def raceKeys(e,pos):
    s,b,big,rf=e
    # BFS over component positions
    from collections import deque
    seen=set()
    todo=list(b.components(pos))
    acc=[]
    # We need track positions as Position objects; use key for seen
    # Use list todo of positions
    todo=list(b.components(pos))
    seen_keys=set()
    # iterative with fuel 100000
    steps=0
    maxsteps=100000
    while todo and steps<maxsteps:
        steps+=1
        p=todo.pop(0)
        pk=p.key()
        if pk in seen_keys:
            continue
        seen_keys.add(pk)
        for c in (W,B):
            for q in moves(s,b,p,c):
                v=env_verdict(e,q,c)
                # race if both passed
                if hasPassed(s,b,q,W) and hasPassed(s,b,q,B):
                    key=(q.key(), c)
                    if key not in [ (x[0].key() if hasattr(x[0],'key') else x[0], x[1]) for x in acc]:
                        acc.append((q,c))
                # open moves: split components
                if (not hasPassed(s,b,q,W)) and (not hasPassed(s,b,q,B)):
                    for comp in b.components(q):
                        if comp.key() not in seen_keys:
                            todo.append(comp)
    return acc

def allWinners(k):
    if k==0: return [[]]
    prev=allWinners(k-1)
    out=[]
    for l in prev:
        out.append([W]+l)
        out.append([B]+l)
    return out

def eighthForAllAssignments(ep, pos, board):
    s=(ep,'count')
    b=board
    e0=make_env(s,b)
    keys=raceKeys(e0,pos)
    k=len(keys)
    # build table mapping
    for ws in allWinners(k):
        table=[]
        for (q,c),w in zip(keys,ws):
            table.append(((q.key(),c), w))  # store key
        # envTable race function looks up by pos.key() and mover
        def rf(pos,mover):
            key=(pos.key(),mover)
            for (k2,col) in table:
                if k2==key:
                    return col
            return None
        e=(s,b,256,rf)
        # isValue with this env
        if not isValue(e,400,pos,EIGHTH):
            return False
    return True

# Test positions
flat8 = Board(8,8,TOPO_FLAT)
cyl8 = Board(8,8,TOPO_CYL)

def pos_from_str(w,b,board):
    # w: list of (letter,rank)
    ws=[sqr(l,r) for (l,r) in w]
    bs=[sqr(l,r) for (l,r) in b]
    return Position_ofSquares(ws,bs,board)

# L4 positions
posA = Position_ofSquares([sqr('a',4),sqr('b',3),sqr('d',2),sqr('d',3)],
                           [sqr('a',7),sqr('b',7),sqr('c',5)], flat8)
posB = Position_ofSquares([sqr('b',4),sqr('c',2),sqr('d',2)],
                           [sqr('a',6),sqr('a',7),sqr('c',6),sqr('d',5)], flat8)

# L5
posG = Position_ofSquares([sqr('a',2),sqr('b',2),sqr('b',3)],
                           [sqr('a',5),sqr('a',6),sqr('b',6)], flat8)

# L6
posX = Position_ofSquares([sqr('b',2),sqr('d',4),sqr('g',3),sqr('h',5)],
                           [sqr('a',7),sqr('c',7),sqr('f',7),sqr('g',4)], cyl8)

if __name__=='__main__':
    print("loaded")
