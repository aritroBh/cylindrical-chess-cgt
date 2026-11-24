"""Replays of literal moves, evidence tables and the ordinary-game history sketches."""
from collections import Counter
from functools import cache
from pathlib import Path
import gzip
import json
import re

from check import Pawns, board, square, notation, num, node, zero, star, two, le, canonical, show


def paths(square_, directions, occupied, slide=False, wrap=True):
    for dx,dy in directions:
        x,y = square_
        for _ in range(7 if slide else 1):
            x,y = x+dx,y+dy
            if wrap:
                x %= 8
            if not (0<=x<8 and 1<=y<=8):
                break
            yield x,y
            if (x,y) in occupied:
                break


king = [(x,y) for x in (-1,0,1) for y in (-1,0,1) if x or y]


def reach(pos, pc, p, wrap):
    kind = pc.upper()
    directions = {'P':[(-1,1 if pc.isupper() else -1),(1,1 if pc.isupper() else -1)],
                  'K':king, 'Q':king, 'B':[(x,y) for x,y in king if x*y],
                  'R':[(x,y) for x,y in king if not x*y],
                  'N':[(x,y) for x in (-2,-1,1,2) for y in (-2,-1,1,2) if abs(x*y)==2]}[kind]
    return set(paths(pos,directions,p,kind in 'BRQ',wrap))


def attacked(p,target,white,wrap=True):
    return any(target in reach(pos,pc,p,wrap) for pos,pc in p.items() if pc.isupper()==white)


def moves(p,white,wrap=False):
    # ponytail: played ordinary lines need neither castling nor e.p.; the
    # pawn-model replay in check.py handles e.p., including across the seam.
    for a,pc in p.items():
        if pc.isupper()!=white: continue
        dest=reach(a,pc,p,wrap)
        if pc.upper()=='P':
            dest &= p.keys()
            d=1 if white else -1
            one=(a[0],a[1]+d)
            if 1<=one[1]<=8 and one not in p:
                dest.add(one)
                two=(a[0],a[1]+2*d)
                if a[1]==(2 if white else 7) and two not in p: dest.add(two)
        for b in dest:
            if b in p and p[b].isupper()==white: continue
            for piece in ('QRBN' if white else 'qrbn') if pc.upper()=='P' and b[1] in (1,8) else (pc,):
                q=p.copy()
                del q[a]
                q[b]=piece
                kingpos=next(s for s,v in q.items() if v==('K' if white else 'k'))
                if not attacked(q,kingpos,not white,wrap):
                    yield notation(a)+notation(b)+(piece.lower() if pc!=piece else ''),q


def cylinder_line(pieces,line):
    p={square(t[1:]):t[0] for t in pieces.split()}
    for i,m in enumerate(line.split()):
        p=dict(moves(p,i%2==0,True))[m]
    return p


def escapes(p):
    bk=next(s for s,pc in p.items() if pc=='k')
    out=[]
    for b in paths(bk,king,p):
        q=p.copy()
        q[b]=q.pop(bk)
        if not attacked(q,b,True): out.append(notation(b))
    return out


def chess_lines():
    for start in ('a1','h1','h4'):
        pc={'a1':'K','h1':'N','h4':'P'}[start]
        targets={'a1':['h2'],'h1':['a3','b2'],'h4':['a5']}[start]
        assert all(attacked({square(start):pc},square(t),True) for t in targets)
    assert all(attacked({square('h1'):'K'},square(t),True) for t in ('a1','a2'))
    for pieces,line in [
            ('Ka3 Rb2 ka1','b2b3 a1h1 b3g3 h1a1 g3g1'),
            ('Ke6 Be1 Bf1 ke8',''), ('Ka3 Bc2 Ng1 ka1','g1h3 a1h1 c2e4')]:
        p=cylinder_line(pieces,line)
        bk=next(s for s,v in p.items() if v=='k')
        assert attacked(p,bk,True) and not escapes(p)
        print('cylinder mate',pieces,line,'flights',escapes(p))
    # T's defensive squares before each king abandons its pawn.
    for white in (True,False):
        p={square(t[1:]):t[0] for t in 'Kh5 Pa4 kb4 pa5'.split()}
        k = square('h5' if white else 'b4')
        target=square('a4' if white else 'a5')
        own,foe=('K','k') if white else ('k','K')
        legal=[]
        for nxt in paths(k,king,p):
            if nxt in p and p[nxt].isupper()==white: continue
            q=p.copy()
            q[nxt]=q.pop(k)
            if attacked(q,nxt,not white): continue
            assert target in paths(next(s for s,v in q.items() if v==foe),king,q)
            assert not attacked(q,target,white)
            legal.append(notation(nxt))
        print('Fig 3a',own,sorted(legal),'all concede',notation(target))
    start={(f,r):pc for r,row in [(1,'RNBQKBNR'),(2,'P'*8),(7,'p'*8),(8,'rnbqkbnr')]
           for f,pc in enumerate(row)}
    for game,targets in [
        ('e2e3 b8c6 b1c3 c6a5 g1h3 a5b3 c2b3 a7a5 f1a6 b7a6 c3a4 h7h6 a4b6 c7b6','a2 b2 b3 / a5 a6 b6'),
        ('e2e3 b8c6 g1f3 c6a5 f1d3 a5b3 c2b3 a7a6 b3b4 d7d6 b4b5 h7h6 b5b6 c7c5','a2 b2 b6 / a6 b7 c5'),
        ('e2e3 b8c6 g1f3 c6a5 f1d3 a5b3 c2b3 a7a6 b3b4 d7d6 b4b5 h7h6 b5b6 c7c6','a2 b2 b6 / a6 b7 c6')]:
        b=start
        for i,m in enumerate(game.split()):
            b=dict(moves(b,i%2==0))[m]
        for pc,men in zip('Pp',targets.split(' / ')):
            assert all(b[square(s)]==pc for s in men.split())
        print('legal pawn trajectories',game)
    b={square(t[1:]):t[0] for t in 'Kf5 Pg4 kh4 pg5 Pa2 Pc2 pb7 pd7'.split()}
    for white in (True,False):
        print('IX legal root moves',sorted(m for m,_ in moves(b,white)))
    b={square(t[1:]):t[0] for t in 'Ka4 Pb7 ka6'.split()}
    for move,q in moves(b,True):
        if not move.startswith('b7b8'): continue
        replies=list(dict(moves(q,False)))
        print('KPK promotion',move,'stalemate',not replies and not attacked(q,square('a6'),True,False),'black replies',replies)
    p={square(t[1:]):t[0] for t in 'Ka1 Bb4 Bc4 kb5'.split()}
    assert 'b4' in escapes(p)
    print('Black can take the b4 bishop')


def micro(n,wrap,misere):
    """Bitboards per color and rank. Raw plies, compulsory captures, no macro rule."""
    start=(1<<n)-1
    @cache
    def win(p,s):
        return any(not win(q,1-s) for _,q in available) if (available:=moves(p,s)) else misere
    def moves(p,s):
        turn=1-2*s
        pushes=[]
        takes=[]
        for r in range(s*2,2*(1-s),turn):
            for i in range(n):
                src=1<<i
                if not (p[3*s+r]&src): continue
                for off in (-1,0,1):
                    j=i+off
                    if wrap: j%=n
                    if not 0<=j<n: continue
                    dest=1<<j
                    t=r+turn
                    victim=p[3*(1-s)+t]&dest
                    if p[3*s+t]&dest or bool(off)!=bool(victim): continue
                    q=list(p)
                    q[3*s+r]^=src
                    q[3*s+t]|=dest
                    q[3*(1-s)+t]^=victim
                    (takes if off else pushes).append((notation((i,r+1))+notation((j,t+1)),tuple(q)))
        return takes or pushes
    p=(start,0,0,0,0,start)
    if n==4 and wrap and not misere:
        for i,m in enumerate('c1c2 b3c2 d1c2 d3c2 b1c2'.split()):
            p=dict(moves(p,i%2))[m]
        assert p==(1,4,0,0,0,5) and list(dict(moves(p,1)))==['a3a2']
        print('Dawson five plies leave one untouched file, Black has a3a2')
        p=(start,0,0,0,0,start)
    result=win(p,0)
    assert win(p,1)==result
    win.cache_clear()
    return result


def records():
    keys=['0','*','*2','1/8','1/16','1/32','{0 | ↓*}','{0, * | ↓}','tiny(1)']
    for f in ('values.jsonl.gz','values_aware.jsonl.gz'):
        with gzip.open(Path('atlas/flat8')/f,'rt') as stream:
            c=Counter(row['value'] for row in map(json.loads,stream))
        print(f,sum(c.values()),[c[k] for k in keys])
    p=Pawns(ep='text')
    print('temperature witness',show(p.solve(board('a2','a5 b3'))))
    p=Pawns()
    pos=board('a2','a4 b3')
    opt=[[p.solve(q,e,s) for _,q,e in p.moves(pos,s)] for s in (0,1)]
    v=p.solve(pos)
    a=next(p.solve(q,e,0) for m,q,e in p.moves(pos,0) if m=='a2b3')
    pruned=canonical(node(set(opt[0])-{a},opt[1]))
    assert not(le(v,pruned) and le(pruned,v))
    print('losing capture, before/after deletion',show(v),show(pruned))
    epd=[row for f in sorted(Path('engine/suite').glob('cgt_*.epd')) for row in f.read_text().splitlines() if row.strip()]
    changes=[]
    for row in epd:
        men=re.search(r'component W: (.*?) / B: (.*?) on files',row).groups()
        p=board(*men)
        a,b=[Pawns(4,ep=ep).solve(p) for ep in ('text','aware')]
        if a!=b:
            changes.append(re.search(r'id "([^"]+)"',row)[1])
        if 'id "cgt128"' in row:
            print('cgt128 textbook/aware',show(a),show(b))
    print('suite exact class inputs changed',len(changes),changes)
    print('distinct pawn components',len({re.search(r'component (.*?) on files',row)[1] for row in epd}))
    for t in ('plane_RR','cyl_R','torus_RB'):
        print((Path('tablebase/replica/results')/(t+'.txt')).read_text().strip())
    print('raw slots',sum(map(int,re.findall(r'positions (\d+):',Path('tablebase/replica/position_compare.txt').read_text()))))


if __name__=='__main__':
    chess_lines()
    for misere in (False,True):
        strip=[micro(n,False,misere) for n in range(14)]
        rings=[micro(n,True,misere) for n in range(3,17)]
        assert rings==[not q for q in strip]
        print('raw pawn ring, misere',misere,rings)
    records()
