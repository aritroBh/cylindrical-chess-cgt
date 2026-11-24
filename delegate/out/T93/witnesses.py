"""Independent whole-board heap tests, with the pawn generator of check.py."""
from functools import lru_cache
from math import comb
from check import Pawns, board, show, plus, num, zero, star, two, three, node, le, options, canonical


def verify_heap(game, p, target):
    # ponytail: cap memo memory; old entries can be recomputed without changing the result.
    @lru_cache(maxsize=60000)
    def wins(p, flag, s, heap):
        live = []
        for _, q, e in game.moves(p,s,flag):
            result = game.terminal(q,e,s)
            if result == num((256,-256)[s]):
                return True
            if result is None:
                live.append((q,e))
        return (any(not wins(q,e,1-s,heap) for q,e in live)
                or any(not wins(p,flag,1-s,h) for h in range(heap)))
    sig = ['PLRN'[wins(p,None,0,h)+2*wins(p,None,1,h)] for h in range(target+2)]
    print(''.join(sig),flush=True)
    assert sig == ['P' if h==target else 'N' for h in range(target+2)]
    wins.cache_clear()


def sum_heap(g,p,k):
    """Expand the large component lazily; use exact short games for smaller summands."""
    @lru_cache(maxsize=30000)
    def wins(p,flag,side,extra):
        live=[]
        for _,q,e in g.moves(p,side,flag):
            end=g.terminal(q,e,side)
            if end is not None:
                total=plus(extra,end)
                if (le(zero,total) if side==0 else le(total,zero)):
                    return True
            else:
                live.append((q,e))
        for q,e in live:
            parts=sorted(g.components(q),key=lambda pair:sum(map(len,pair)),reverse=True)
            other=extra
            for part in parts[1:]:
                other=plus(other,g.solve(part,e,side))
            if not wins(parts[0],e,1-side,other):
                return True
        return any(not wins(p,flag,1-side,h) for h in options[extra][side])
    heap=(zero,star,two,three)[k]
    result=tuple(wins(p,None,s,heap) for s in (0,1))
    wins.cache_clear()
    assert result==(False,False),result
    print('also P against the same heap in the component sum',flush=True)


def main():
    for name,w,b,n,r,wrap,k in [
            ('A','a4 b3 d2 d3','a7 b7 c5',4,8,False,2),
            ('B','b4 c2 d2','a6 a7 c6 d5',4,8,False,2),
            ('six-pawn cylinder','a2 a3 b2','b7 c6 c7',3,8,True,2),
            ('seven-rank flat','a2 c2','c3 b6',3,7,False,2),
            ('six-rank flat','a2 b2 d2','a5 c5 d5',4,6,False,2),
            ('seven-rank flat star three','a2 c2 d3','c3 b6 c6',4,7,False,3),
            ('C7 ten-pawn S6 example','a2 a5 c4 e2 f2','a7 b4 d7 e5 g7',7,8,True,3),
            ('C11 twelve-pawn S6 example','c4 d6 e3 h3 i2 k2','a4 b7 d7 f7 g6 j6',11,8,True,3),
            ('nine-pawn flat','a2 b4 c2 d2','a4 a6 a7 c6 d5',4,8,False,3),
            ('M10','b2 d2 e3 h3 j5','a4 c6 f6 g7 i7',10,8,True,2),
            ('O11','c5 e3 h3 i2 k2','a4 b7 d7 f7 g6 j6',11,8,True,2)]:
        print(name,end=' ',flush=True)
        verify_heap(Pawns(n,r,wrap,split=False),board(w,b),k)
        if name in ("M10","O11","nine-pawn flat","C7 ten-pawn S6 example"):
            sum_heap(Pawns(n,r,wrap),board(w,b),k)


def ep_options():
    start=board('a2 a3 b2','b7 c6 c7')
    a=Pawns(3,wrap=True)
    for banned in ('b4a3','b5c6'):
        def moves(p,s,flag=None):
            for m,q,e in Pawns.moves(a,p,s,flag):
                captured=p[1-s]-q[1-s]
                if m==banned and flag is not None and captured=={flag} and flag[1]!=int(m[3]):
                    continue
                yield m,q,e
        a.moves=moves
        a.solve.cache_clear()
        print('C3 omit e.p. option',banned,show(a.solve(start)))
    a=Pawns(3,wrap=True)
    for line in ('a3a4 b7b5 a4a5 b5b4 a2a4 b4a3','a3a4 c6c5 b2b4 c5c4 b4b5 c7c5 b5c6'):
        a.line(start,0,line)


def other():
    for desc,w,b,n,wrap,ep,rule in [
          ('Proposition 7','b2 d4 g3 h5','a7 c7 f7 g4',8,True,'off','count'),
          ('atlas ring','a2 b4','b7 c6',3,True,'text','count'),
          ('atlas mover','a2 b4','b7 c6',3,True,'text','mover'),
          ('flat 3/4 counterexample','a2 a4 b3','a7 b6 b7',2,False,'text','count'),
          ('seven-pawn uniqueness counterexample','a2 b2 d2','a4 d4 e3 e4',5,False,'aware','count'),
          ('sum model example','a5 d3','b6 e4',5,False,'aware','count'),
          ('puzzle 3 shifted','c2 c4 d4','c3 d5 d6 d7',8,True,'aware','count'),
          ('second oracle candidate','a3 b3 c2','b5 b7 c6',8,False,'aware','opponent')]:
        vals=[]
        for split in (True,False):
            g=Pawns(n,wrap=wrap,ep=ep,rule=rule,split=split)
            value=g.solve(board(w,b))
            vals.append((show(value) if desc!='Proposition 7' else 'outcome', 'P' if value==zero else 'L' if le(zero,value)
                         else 'R' if le(value,zero) else 'N'))
        print(desc, vals)
    a=Pawns(5)
    p=board('a2 b2 d2','a4 d4 e3 e4')
    print('separate components',[show(a.solve(part)) for part in a.components(p)])
    assert a.solve(p)==two
    assert {a.solve(part) for part in a.components(p)}=={num(256),plus(num(-256),two)}
    # Two-sided Fisher, conditional on both margins, with exact integer weights.
    for n,b in [(68,55),(57,45),(37,27),(20,12),(17,9)]:
        N,k=27+n,8+b
        mass=[comb(k,i)*comb(N-k,27-i) if 0<=i<=k and 0<=27-i<=N-k else 0
              for i in range(28)]
        print('Fisher',n,sum(m for m in mass if m<=mass[8])/comb(N,27))


if __name__=='__main__':
    other()
    ep_options()
    main()
