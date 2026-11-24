"""Cold referee check. Run from the project root; standard library only."""
from functools import cache
from fractions import Fraction
from itertools import count
from pathlib import Path
import re
import sys
sys.setrecursionlimit(6000)

# Short games are interned pairs of option sets. Conway comparison and
# reversibility use the complete option sets before any proposed bypass.
options = []
ids = {}
names = {}
numeric = {}


def node(left=(), right=()):
    pair = tuple(sorted(set(left))), tuple(sorted(set(right)))
    if pair not in ids:
        ids[pair] = len(options)
        options.append(pair)
    return ids[pair]


@cache
def num(q):
    q = Fraction(q)
    if q.denominator == 1:
        result = node([num(q-1)] if q > 0 else [], [num(q+1)] if q < 0 else [])
    else:
        step = Fraction(1, q.denominator)
        result = node([num(q-step)], [num(q+step)])
    names[result] = str(q)
    numeric[result] = q
    return result


@cache
def le(x, y):
    if x == y:
        return True
    if x in numeric and y in numeric:
        return numeric[x] <= numeric[y]
    return (not any(le(y, a) for a in options[x][0])
            and not any(le(b, x) for b in options[y][1]))


@cache
def canonical(g):
    left, right = map(set, options[g])
    while True:
        left = {a for a in left if not any(a != b and le(a, b) for b in left)}
        right = {a for a in right if not any(a != b and le(b, a) for b in right)}
        current = node(left, right)
        for side, group in enumerate((left, right)):
            for a in sorted(group):
                for b in options[a][1-side]:
                    if le(b, current) if side == 0 else le(current, b):
                        group.remove(a)
                        group.update(options[b][side])
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            return current


@cache
def plus(x, y):
    if x in numeric and y in numeric:
        return num(numeric[x] + numeric[y])
    if x == zero:
        return y
    if y == zero:
        return x
    return canonical(node(*([plus(a,y) for a in options[x][s]]
                             + [plus(x,b) for b in options[y][s]] for s in (0,1))))


def show(g):
    if g in names:
        return names[g]
    return '{' + '|'.join(','.join(map(show, group)) for group in options[g]) + '}'


zero = num(0)
for i in range(1, 258):
    num(i)
    num(-i)
for d in (2, 4, 8, 16):
    for i in range(-d, d):
        num(Fraction(i, d))

star = node([zero], [zero])
two = node([zero,star], [zero,star])
three = node([zero,star,two], [zero,star,two])
up, down = node([zero],[star]), node([star],[zero])
up2star = node([zero,star],[down])
switch = node([zero],[num(-1)])
tiny = node([zero],[switch])
hotleft, hotright = node([num(3)],[num(1)]), node([num(-1)],[num(-3)])
hot = node([hotleft],[hotright])
for g, title in [(star,'*'), (two,'*2'), (three,'*3'), (up,'up'), (down,'down'),
                 (plus(plus(up,up),star),'2up+*'), (up2star,'up-second+*'),
                 (switch,'{0|-1}'), (tiny,'Tiny(1)'), (hotleft,'2+/-1'),
                 (hotright,'-2+/-1'), (hot,'{2+/-1|-2+/-1}')]:
    names[g] = title


def square(s):
    return ord(s[0])-97, int(s[1:])


def board(w, b):
    return tuple(frozenset(map(square, men.split())) for men in (w,b))


def notation(s):
    return chr(97+s[0])+str(s[1])


class Pawns:
    def __init__(self, width=8, height=8, wrap=False, ep='aware', rule='count', split=True):
        self.width, self.height, self.ep, self.rule, self.split = width, height, ep, rule, split
        self.near = []
        for f in range(width):
            neighbors = {f-1,f+1}
            self.near.append({x % width for x in neighbors} - {f} if wrap
                             else {x for x in neighbors if 0 <= x < width})
        self.solve = cache(self._solve)

    def moves(self, p, side, flag=None):
        own, enemy = p[side], p[1-side]
        step = 1-2*side
        for x in own:
            f,r = x
            dest = (f,r+step)
            if not 1 <= dest[1] <= self.height:
                continue
            candidates = []
            if dest not in own|enemy:
                candidates.append((dest,None,None))
                double = (f,r+2*step)
                if r == (2,self.height-1)[side] and double not in own|enemy:
                    candidates.append((double,None,double if self.ep != 'off' else None))
            for h in self.near[f]:
                dest = (h,r+step)
                if dest in enemy:
                    candidates.append((dest,dest,None))
                elif (h,r) == flag and flag in enemy and dest not in own:
                    candidates.append((dest,flag,None))
            for y, victim, newflag in candidates:
                nxt = [own-{x}|{y}, enemy-{victim}]
                yield notation(x)+notation(y), tuple(nxt if side==0 else reversed(nxt)), newflag

    def distances(self,p,side,flag):
        step = 1-2*side
        own,enemy = p[side],p[1-side]
        for f,r in own:
            if any((h==f or h in self.near[f]) and (t-r)*step>0 for h,t in enemy):
                continue
            if self.ep=='aware' and (f,r)==flag and (f,r-step) not in own|enemy and any(
                    (h,r) in enemy for h in self.near[f]):
                continue
            yield abs((self.height,1)[side]-r) - (r == (2,self.height-1)[side])

    def terminal(self,p,flag,mover):
        a,b = [min(self.distances(p,s,flag),default=10000) for s in (0,1)]
        if a==b==10000:
            return None
        if max(a,b)==10000 or self.rule=='count' and a!=b:
            winner = int(b<a)
        elif self.rule in ('white','black'):
            winner = int(self.rule=='black')
        else:
            winner = mover if self.rule=='mover' else 1-mover
        return num((256,-256)[winner])

    def components(self,p):
        pending = {f for group in p for f,r in group}
        while pending:
            files = {pending.pop()}
            stack = list(files)
            while stack:
                new = pending & self.near[stack.pop()]
                files.update(new)
                stack.extend(new)
                pending -= new
            yield tuple(frozenset(x for x in men if x[0] in files) for men in p)

    def _solve(self,p,flag=None,mover=0):
        end = self.terminal(p,flag,mover)
        if end is not None:
            return end
        parts = list(self.components(p)) if self.split else [p]
        if len(parts)>1:
            total = zero
            for part in parts:
                total = plus(total, self.solve(part,flag,mover))
            return total
        return canonical(node(*([self.solve(q,e,s) for _,q,e in self.moves(p,s,flag)]
                                for s in (0,1))))

    def line(self,p,side,line):
        flag = None
        for move in line.split():
            legal = {m:(q,e) for m,q,e in self.moves(p,side,flag)}
            p,flag = legal[move]
            print(move,show(self.solve(p,flag,side)),end='  ')
            side = 1-side
        print()
        return p,flag


def roots():
    cases = [
        ('ep diagram','a2','b4',8,False), ('extra b3','a2 b3','b4',8,False),
        ('seam zero','a4 h3','a5 h6',8,True), ('seam one','a4 h2','a5 h6',8,True),
        ('seam two','a5 h2','a6 h7',8,True), ('seam tiny','a4 h2 h4','a5 a6 a7 h3',8,True),
        ('eighth','a2 b2 b3','a5 a6 b6',8,False), ('up-second star','a2 b2 b6','a6 b7 c5',8,False),
        ('flat tiny','a2 b2 b6','a6 b7 c6',8,False), ('candidate','a2 c2','b7 d7',8,False),
        ('A','a4 b3 d2 d3','a7 b7 c5',8,False), ('B','b4 c2 d2','a6 a7 c6 d5',8,False),
        ('ring 3','a2 a3 b2','b7 c6 c7',3,True)]
    for name,w,b,n,wrap in cases:
        vals = []
        for ep in ['aware','text','off']:
            for rule in ['count','mover','opponent']:
                game = Pawns(n,wrap=wrap,ep=ep,rule=rule)
                result=game.solve(board(w,b))
                vals.append(show(result))
                if name in ('eighth','up-second star','flat tiny','candidate','A','B'):
                    whole=Pawns(n,wrap=wrap,ep=ep,rule=rule,split=False)
                    other=whole.solve(board(w,b))
                    if name in ('A','B'):
                        assert (other==two)==(result==two)
                    else:
                        assert result==other
                    whole.solve.cache_clear()
                game.solve.cache_clear()
        if name in ('A','B'):
            assert [v=='*2' for v in vals] == [True,True,False,True,True,False,False,False,False]
        if name=='candidate':
            assert vals == [show(hot),show(hot),'0','*2','*2','0','*2','*2','0']
        if name in ('eighth','up-second star'):
            assert len(set(vals))==1 and vals[0]==('1/8' if name=='eighth' else 'up-second+*')
        print(name,vals,flush=True)
    for ep in ('aware','text','off'):
        for rule in ('white','black'):
            game = Pawns(ep=ep,rule=rule)
            assert game.solve(board('a2 b2 b3','a5 a6 b6')) == num(Fraction(1,8))
    print('eighth, lower and upper race assignments: 1/8 at every endpoint')


def lines():
    for name,w,b,wrap,ep,side,line in [
        ('Fig 2a','a2','b4',False,'aware',0,'a2a4 b4a3'),
        ('II-D direct','a2 b3','b4',False,'aware',0,'a2a3 b4a3'),
        ('II-D ep','a2 b3','b4',False,'aware',0,'a2a4 b4a3'),
        ('III white','a4 h3','a5 h6',True,'aware',0,'h3h4 a5h4'),
        ('III black','a4 h3','a5 h6',True,'aware',1,'h6h5 a4h5'),
        ('III ep','a5 h2','a6 h7',True,'aware',1,'h7h5 a5h6'),
        ('III tiny','a4 h2 h4','a5 a6 a7 h3',True,'aware',0,'h4a5'),
        ('III rejected','a4 h2 h4','a5 a6 a7 h3',True,'aware',0,'h4h5 a6h5'),
        ('III lock','a4 h2 h4','a5 a6 a7 h3',True,'aware',1,'a5h4 a4a5'),
        ('III spare (black branch)','a4 h2','h3 h4 a6 a7',True,'aware',1,'a6a5'),
        ('V puzzle 1, local component','a4 a5 h2 h3','a7 h6',True,'aware',1,'h6a5'),
        ('VIII textbook plan, as separate branch','a2 c2','b4 d7',False,'text',0,'a2a4'),
        ('VIII aware plan','a2 c2','b4 d7',False,'aware',0,'a2a4 b4a3'),
        ('VIII A','a4 b3 d2 d3','a7 b7 c5',False,'aware',0,'d3d4 c5d4 b3b4'),
        ('VIII A','a4 b3 d2 d3','a7 b7 c5',False,'aware',0,'b3b4 c5b4'),
        ('VIII A','a4 b3 d2 d3','a7 b7 c5',False,'aware',1,'c5c4 d3c4')]:
        game=Pawns(wrap=wrap,ep=ep)
        print(name, end=': ')
        game.line(board(w,b),side,line)
    for label,w,b,ep in [
            ('VII eighth','a2 b2 b3','a5 a6 b6','aware'), ('VII up2*','a2 b2 b6','a6 b7 c5','aware'),
            ('VII tiny','a2 b2 b6','a6 b7 c6','aware'), ('VIII candidate','a2 c2','b7 d7','text'),
            ('VIII candidate','a2 c2','b7 d7','aware'),('VIII candidate staggered','a2 c2','b4 d7','aware'),
            ('VIII A','a4 b3 d2 d3','a7 b7 c5','aware')]:
        g=Pawns(ep=ep)
        p=board(w,b)
        print(label,ep,show(g.solve(p)))
        for s in (0,1):
            for m,q,e in sorted(g.moves(p,s)):
                print(m,show(g.solve(q,e,s)),end='; ')
                if label=='VIII A' and m in ('a7a6','b7b5','d3d4'):
                    print([(move,show(g.solve(r,f,1-s))) for move,r,f in sorted(g.moves(q,1-s,e))],end=' ')
            print()


def mex(values):
    return next(k for k in count() if k not in values)


def dawson():
    strip=[0]
    octal=[0]
    old=[0]
    for n in range(1,301):
        # Push each possible file, then delete its closed neighborhood.
        strip.append(mex({strip[max(0,i-1)]^strip[max(0,n-i-2)] for i in range(n)}))
        # Decode octal digits: bit j permits j nonempty heaps after removal.
        vals=set()
        for take,digit in enumerate((1,3,7),1):
            rem=n-take
            if rem==0 and digit&1: vals.add(0)
            if rem>=1 and digit&2: vals.add(octal[rem])
            if digit&4: vals.update(octal[j]^octal[rem-j] for j in range(1,rem))
        octal.append(mex(vals))
        offcuts={strip[a]^strip[n-3-a] for a in range(n-2)}
        assert strip[n]==(1 if n==1 else mex(offcuts|{strip[n-2]}))
        old.append(mex({old[a]^old[n-3-a] for a in range(n-2)}))
    assert strip==octal
    src=Path('dist/tog/figures/src/dawson_grundy.tex').read_text()
    points=[[(int(x),int(y)) for x,y in re.findall(r'\((\d+),(\d+)\)',row)]
            for row in src.splitlines() if row.startswith(r'\addplot')]
    assert points==[list(enumerate(strip[:81])),[(n,0) for n in range(81) if not strip[n]]]
    for n in range(0,81,10): print(n,strip[n:min(n+10,81)])
    print('exceptions',[n for n in range(267) if strip[n]!=strip[n+34]],'51,85',strip[51],strip[85])
    assert all(strip[n]==strip[n+34] for n in range(52,141))
    assert all(any(strip[n]!=strip[n+d] for n in range(52,86)) for d in range(1,34))
    print('ring wins to 80',[n for n in range(3,81) if strip[n-3]==0])
    wrong=[n for n in range(3,301) if bool(old[n-3])!=bool(strip[n-3])]
    print('old agreement',sum(a==b for a,b in zip(old,strip)), 'ring errors',len(wrong), 'first',min(wrong))


if __name__=='__main__':
    for arg in sys.argv[1:]:
        {'roots':roots, 'lines':lines, 'dawson':dawson}[arg]()
