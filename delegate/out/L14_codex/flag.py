"""Find a legal live en passant right omitted by a diagram-only root enumeration."""
from itertools import combinations
from census import canonical, game, moves, nimber, terminal


def squares(pieces):
    return ' '.join(chr(97+q//8)+str(1+q%8) for q in pieces)


def find():
    for k in range(2,7):
        for n in range(2,5):
            allq = [8*f+r for f in range(n) for r in range(1,7)]
            for sq in combinations(allq,k):
                if sq[0]//8 or sq[-1]//8 != n-1:
                    continue
                for cnt in range(1,k):
                    for w in combinations(sq,cnt):
                        b = tuple(q for q in sq if q not in w)
                        if terminal(w,b,-1,0) is not None:
                            continue
                        for s in (0,1):
                            for u,v,flag in moves(w,b,-1,s):
                                if flag < 0 or terminal(u,v,flag,s) is not None or terminal(u,v,-1,s) is not None:
                                    continue
                                with_ep = nimber(canonical(game(u,v,flag)))
                                without_ep = nimber(canonical(game(u,v,-1)))
                                if with_ep != without_ep:
                                    print('before',squares(w),'/',squares(b),'mover',s)
                                    print('after',squares(u),'/',squares(v),'flag',squares([flag]))
                                    print('nimber (-1 = nonnimber), live and absent',with_ep,without_ep)
                                    return
    raise AssertionError('no witness')



def extra(n):
    """Root with a real last double step from an open, flag-free predecessor."""
    from itertools import product
    for k in range(2,7):
        count = zero = star = higher = 0
        for side in (0,1):
            step = 1 if side == 0 else -1
            for f in range(n):
                flag = 8*f+(3 if side == 0 else 4)
                for j in (f-1,f+1):
                    if not 0 <= j < n:
                        continue
                    capturer = flag+8*(j-f)
                    free = [8*i+r for i in range(n) for r in range(1,7)
                            if 8*i+r not in (flag,capturer,flag-step,flag-2*step)]
                    for rest in combinations(free,k-2):
                        if min(*rest,flag,capturer)//8 or max(*rest,flag,capturer)//8 != n-1:
                            continue
                        for colors in product(range(2),repeat=k-2):
                            us = tuple(sorted([flag]+[x for x,c in zip(rest,colors) if c==side]))
                            them = tuple(sorted([capturer]+[x for x,c in zip(rest,colors) if c!=side]))
                            if any(x < capturer and abs(x-flag)==8 for x in them):
                                continue
                            w,b = (us,them) if side==0 else (them,us)
                            mir = lambda x: 8*(n-1-x//8)+x%8
                            mirror = tuple(sorted(map(mir,w))),tuple(sorted(map(mir,b))),mir(flag)
                            if (w,b,flag)>mirror or terminal(w,b,flag,side) is not None:
                                continue
                            prev = tuple(sorted(set(us)-{flag}|{flag-2*step}))
                            pw,pb = (prev,them) if side==0 else (them,prev)
                            if terminal(pw,pb,-1,1-side) is not None:
                                continue
                            assert (w,b,flag) in moves(pw,pb,-1,side)
                            nim = nimber(canonical(game(w,b,flag)))
                            if nim >= 2 and higher == 0:
                                print('first higher',n,k,squares(w),'/',squares(b),'flag',squares([flag]),nim)
                            count += 1
                            zero += nim == 0
                            star += nim == 1
                            higher += nim >= 2
        print('live roots',n,k,count,zero,star,higher,flush=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        extra(int(sys.argv[1]))
    else:
        find()
