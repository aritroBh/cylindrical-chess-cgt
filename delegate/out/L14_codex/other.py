"""Independent tests of the eighth, the threat witnesses and a complete cut instance."""
from functools import cache
from itertools import combinations
from boards import Board, bits


def eighth():
    b = Board(2,'flat')  # No pawn can leave these two occupied files.
    p = b.position(['W2B56','W23B6'])
    for mode in ('off','textbook','aware'):
        races = set()
        @cache
        def win(p, side, ref):
            answers = []
            if (side == 1 and ref) or (side == 0 and ref >= 2):
                q = win(p,1-side,0 if side else ref-1)
                answers.append(None if q is None else not q)
            for x in b.moves(p,side,mode):
                v = b.verdict(x,side,mode,'unknown')
                if v == 2:
                    races.add((x,side))
                    answers.append(None)
                elif v is not None:
                    answers.append(v == side)
                else:
                    a = win(x,1-side,ref)
                    answers.append(None if a is None else not a)
            return True if True in answers else None if None in answers else False
        pair = win(p,0,4), win(p,1,4)
        print('eighth',mode,pair,'unassigned race/mover pairs visited',len(races))
        assert pair == (False,False)


def components(b,p):
    todo = {q//8 for mask in p[:4] for q in bits(mask)}
    result = set()
    while todo:
        group, queue = set(), [next(iter(todo))]
        while queue:
            f = queue.pop()
            if f not in todo:
                continue
            todo.remove(f)
            group.add(f)
            for j in (f-1,f+1):
                if b.topology != 'flat' or 0 <= j < b.n:
                    queue.append(j%b.n)
        mask = sum(255<<(8*f) for f in group)
        result.add(tuple(m & mask for m in p[:4]) + (p[4] if p[4]//8 in group else -1,))
    return result


def witnesses():
    b = Board(8,'cylinder')
    def position(w, black):
        p = [0,0,0,0,-1]
        for group, pieces in ((0,w),(3,black)):
            for f,r in pieces.split():
                p[group] |= 1 << (8*(ord(f)-ord('a'))+int(r)-1)
        return tuple(p)
    def line(start, steps):
        p = start
        for side, w, black in steps:
            assert b.verdict(p,0,'off','count') is None
            child = position(w,black)
            assert child in b.moves(p,side,'off')
            p = child
        return p
    p = line(position('b2 d4 g3 h5','a7 c7 f7 g4'), [
        (0,'b2 d4 g3 h6','a7 c7 f7 g4'),(1,'b2 d4 g3','c7 f7 g4 h6')])
    bd, fh = position('b2 d4','c7'), position('g3','f7 g4 h6')
    assert b.verdict(p,0,'off','count') is None and components(b,p) == {bd,fh}
    for label, start, moves, want in [
        ('bd',bd,[(0,'b2 d5','c7'),(1,'b2 d5','c5')],(True,False)),
        ('fh',fh,[(1,'g3','f5 g4 h6'),(1,'g3','f4 g4 h6'),(1,'g3','f3 g4 h6')],(False,True)),
        ('fh race',fh,[(1,'g3','f7 g4 h5'),(1,'g3','f7 g4 h4'),(0,'h4','f7 g4')],(True,True))]:
        end = line(start,moves)
        flags = tuple(bool(list(b.passers(end,s,'off'))) for s in (0,1))
        assert flags == want
        print('threat',label,flags)


def cut():
    n = 6
    cyl, flat = Board(n,'cylinder'), Board(n-1,'flat')
    for empty in range(n):
        order = [(empty+i)%n for i in range(1,n)]
        def relabel(p):
            masks = tuple(sum(((v>>(8*f))&255)<<(8*i) for i,f in enumerate(order)) for v in p[:4])
            return masks+(8*order.index(p[4]//8)+p[4]%8 if p[4]>=0 else -1,)
        base = set()
        choices = [(s,8*f+r) for s in (0,3) for f in order for r in range(8)
                   if (s == 0 and r>0) or (s == 3 and r<7)]
        for k in range(3):
            for items in combinations(choices,k):
                if len({q for s,q in items}) != k:
                    continue
                p = [0,0,0,0,-1]
                for s,q in items:
                    p[s] |= 1<<q
                base.add(tuple(p))
        flagged = {q for p in base for s in (0,1) for q in cyl.moves(p,s,'aware') if q[4]>=0}
        for mode in ('off','textbook','aware'):
            family = base if mode=='off' else base | flagged
            for p in family:
                q = relabel(p)
                assert {relabel(c) for c in components(cyl,p)} == components(flat,q)
                for s in (0,1):
                    m = set(cyl.moves(p,s,mode))
                    assert m <= family
                    assert {relabel(x) for x in m} == set(flat.moves(q,s,mode))
                    old = {(order.index(x//8),x%8,d) for x,d in cyl.passers(p,s,mode)}
                    assert old == {(x//8,x%8,d) for x,d in flat.passers(q,s,mode)}
                    for race in ('count','mover','opponent'):
                        assert cyl.verdict(p,s,mode,race) == flat.verdict(q,s,mode,race)
        print('cut',empty,'no flag',len(base),'extra usable flags',len(flagged),flush=True)


if __name__ == '__main__':
    eighth()
    witnesses()
    cut()
