"""Pawn rules from the paper. Each army has a bitboard for each heading."""
from functools import lru_cache


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask -= low


class Board:
    def __init__(self, n, topology):
        self.n, self.topology = n, topology
        self.front, self.blockers, self.diag = {}, {}, {}
        for q in range(8*n):
            f, r = divmod(q, 8)
            for down in (0, 1):
                step = 1-2*down
                ranks = list(range(r+step, -1 if down else 8, step))
                self.front[q,down] = sum(1 << (8*f+i) for i in ranks)
                mask = self.front[q,down]
                diag = []
                for neighbor in (f-1, f+1):
                    seam = not 0 <= neighbor < n
                    if seam and topology == 'flat':
                        continue
                    flip = seam and topology == 'mobius'
                    mapped = [8*(neighbor%n)+(7-i if flip else i) for i in ranks]
                    for t in mapped:
                        mask |= 1 << t
                    if mapped:
                        diag.append((mapped[0], int(flip)))
                self.blockers[q,down], self.diag[q,down] = mask, diag

    def position(self, files):
        assert len(files) == self.n
        groups = [0]*4
        for f, word in enumerate(files):
            group = None
            for ch in word:
                if ch in 'WB':
                    group = 0 if ch == 'W' else 3
                else:
                    groups[group] |= 1 << (8*f+int(ch)-1)
        return (*groups, -1)

    def passers(self, p, side, mode):
        foe = p[2] | p[3] if side == 0 else p[0] | p[1]
        for d in (0, 1):
            for q in bits(p[2*side+d]):
                if not (self.blockers[q,d] & foe) and (mode != 'aware' or q != p[4]):
                    yield q, d

    def distance(self, p, side, mode):
        occ = p[0] | p[1] | p[2] | p[3]
        best = None
        for q, d in self.passers(p,side,mode):
            t = q%8 if d else 7-q%8
            t = 99 if self.front[q,d] & occ else t - int(t == 6)
            best = t if best is None else min(best,t)
        return best

    def verdict(self, p, mover, mode, race):
        a, b = self.distance(p,0,mode), self.distance(p,1,mode)
        if a is None:
            return None if b is None else 1
        if b is None:
            return 0
        if race == 'unknown':
            return 2
        if race == 'mover':
            return mover
        if race == 'opponent' or a == b:
            return 1-mover
        return int(b<a)

    def moves(self, p, side, mode):
        occ = p[0] | p[1] | p[2] | p[3]
        foe = (2,3) if side == 0 else (0,1)
        for d in (0,1):
            group = 2*side + d
            step = 1-2*d
            for q in bits(p[group]):
                if not self.front[q,d]:
                    continue
                dest = q+step
                base = list(p)
                base[group] ^= 1 << q
                base[4] = -1
                if not occ & (1<<dest):
                    child = base.copy()
                    child[group] |= 1 << dest
                    yield tuple(child)
                    landing = dest+step
                    if q%8 == (6 if d else 1) and not occ & (1<<landing):
                        child = base.copy()
                        child[group] |= 1 << landing
                        # An enemy diagonal must hit the skipped square even across the twist.
                        if mode != 'off' and any(t == dest for j in foe for x in bits(p[j])
                                                 for t,_ in self.diag[x,j%2]):
                            child[4] = landing
                        yield tuple(child)
                for dest, flip in self.diag[q,d]:
                    for j in foe:
                        if p[j] & (1<<dest):
                            victim = dest
                        elif (mode != 'off' and p[4]>=0 and p[j] & (1<<p[4])
                              and dest == p[4]-(1-2*(j%2)) and not occ & (1<<dest)):
                            victim = p[4]
                        else:
                            continue
                        child = base.copy()
                        child[j] ^= 1 << victim
                        child[group^flip] |= 1 << dest
                        yield tuple(child)

    def signature(self, root, mode='aware', size=4, race='count'):
        assert self.verdict(root,0,mode,race) is None
        @lru_cache(maxsize=16384)
        def options(p, s):
            opened = []
            for q in self.moves(p,s,mode):
                end = self.verdict(q,s,mode,race)
                if end == s:
                    return True, ()
                if end is None:
                    opened.append(q)
            return False, tuple(opened)

        @lru_cache(maxsize=200000)
        def win(p, s, h):
            immediate, children = options(p,s)
            return immediate or any(not win(p,1-s,j) for j in range(h)) or any(
                not win(q,1-s,h) for q in children)
        classes = {(True,True):'N',(False,False):'P',(True,False):'L',(False,True):'R'}
        ans = ''.join(classes[win(root,0,h), win(root,1,h)] for h in range(size+1))
        win.cache_clear()
        options.cache_clear()
        return ans


def examples():
    for n in range(5,11):
        word = (['W23B4','B5','W2B5'] + ['W3','B5']*((n-3)//2) if n%2 else
                ['B5','W2B5','W35B6','W2'] + ['B4','W2']*((n-4)//2))
        b = Board(n,'cylinder')
        print('wall', n, b.signature(b.position(word)), flush=True)
    core = 'B6 W2 W3 B6 B7 W3 B7 W5'.split()
    for label, topo, word, mode in [
        ('M10','cylinder',['B4','W2']+core,'aware'),
        ('O11','cylinder','B4 B7 W5 B7 W3 B7 B6 W3 W2 B6 W2'.split(),'aware'),
        ('ring6','cylinder','W23 W2B7 B67'.split(),'aware'),
        ('ring6','cylinder','W23 W2B7 B67'.split(),'off'),
        ('C11 twelve pawns','cylinder','B4 B7 W4 W6B7 W3 B7 B6 W3 W2 B6 W2'.split(),'aware'),
        ('F1(1)','mobius',['B4','W2']+core,'aware'),
        ('F1(0)','mobius',core,'aware'), ('F2(0)','mobius',core+['B7'],'aware'),
        ('TT(0)','mobius','B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2'.split(),'aware')]:
        b = Board(len(word),topo)
        print(label,mode,b.signature(b.position(word),mode),flush=True)

    for label, word in [
        ('R9', 'W5 B7 W2 W3B6 W3 W2B5 B5 W2 B4'),
        ('Qo9', 'W4 B7 W2 W3B6 W3 W2B5 B5 W2 B4'),
        ('M8', 'B6 W2 W3 B6 B7 W3 B7 W5'), ('O9', 'B4 B7 W3 B7 B6 W3 W2 B6 W2'),
        ('T10', 'B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2'),
        ('S11', 'B4 B6 W3 W6B7 W3 B7 B6 W3 W2 B6 W2')]:
        files = word.split()
        b = Board(len(files),'cylinder')
        print('cylinder control',label,b.signature(b.position(files)),flush=True)
    b = Board(3,'cylinder')
    p = b.position('W23 W2B7 B67'.split())
    for mode in ('off','textbook','aware'):
        for race in ('count','mover','opponent'):
            print('ring6',mode,race,b.signature(p,mode,race=race),flush=True)


if __name__ == '__main__':
    examples()
