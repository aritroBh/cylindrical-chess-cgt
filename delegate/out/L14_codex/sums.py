"""Play the component sum against a heap, keeping the net integer after passes."""
from functools import lru_cache
from time import monotonic
from boards import Board
from other import components


def check(n, word, k, mode):
    board = Board(n,'cylinder')
    p = board.position(word.split())
    assert board.verdict(p,0,mode,'count') is None

    @lru_cache(maxsize=32768)
    def options(p, side):
        out = []
        for q in board.moves(p,side,mode):
            v = board.verdict(q,side,mode,'count')
            if v is None:
                out.append((0, tuple(sorted(components(board,q)))))
            else:
                out.append((256 if v == 0 else -256, ()))
        return sorted(out,key=lambda move: move[0],reverse=side==0)

    deadline = monotonic()+300
    @lru_cache(maxsize=200000)
    def wins(cs, bank, h, side):
        if monotonic() > deadline:
            raise TimeoutError('five-minute limit for one ring')
        if not cs:
            return (bank>0 if side==0 else bank<0) if bank else h>0
        ordered = [(change,i,extra) for i,x in enumerate(cs) for change,extra in options(x,side)]
        ordered.sort(key=lambda move: move[0],reverse=side==0)
        for change,i,extra in ordered:
            nxt = tuple(sorted(cs[:i]+cs[i+1:]+extra))
            if not wins(nxt,bank+change,h,1-side):
                return True
        if any(not wins(cs,bank,j,1-side) for j in range(h)):
            return True
        step = 1-2*side
        return bank*step>0 and not wins(cs,bank-step,h,1-side)

    cs = tuple(sorted(components(board,p)))
    pair = tuple(wins(cs,0,k,s) for s in (0,1))
    print(n,mode,'heap',k,'mover wins',pair,flush=True)
    assert pair == (False,False)


if __name__ == '__main__':
    check(3,'W23 W2B7 B67',2,'aware')
    check(3,'W23 W2B7 B67',0,'off')
    check(10,'B4 W2 B6 W2 W3 B6 B7 W3 B7 W5',2,'aware')
    check(11,'B4 B7 W5 B7 W3 B7 B6 W3 W2 B6 W2',2,'aware')
