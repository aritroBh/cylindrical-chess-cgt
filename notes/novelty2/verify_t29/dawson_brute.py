# Brute force Dawson's chess on 3xn (flat or cylinder), normal play, compulsory captures, no double step, no promotion.
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)
def solve(n, wrap):
    # state: tuple of length 3*n; index r*n+c ; 0 empty, 1 white, 2 black ; r=0 is white's home rank
    def nb(c,d):
        c2=c+d
        if wrap: return c2%n
        return c2 if 0<=c2<n else None
    def moves(s, side):
        caps=[]; pushes=[]
        for r in range(3):
            for c in range(n):
                p=s[r*n+c]
                if p!=side: continue
                dr = 1 if side==1 else -1
                r2=r+dr
                if not (0<=r2<3): continue
                for d in (-1,1):
                    c2=nb(c,d)
                    if c2 is None: continue
                    if s[r2*n+c2]==3-side:
                        t=list(s); t[r*n+c]=0; t[r2*n+c2]=side; caps.append(tuple(t))
                if s[r2*n+c]==0:
                    # no promotion: cannot move onto the far rank
                    if (side==1 and r2==2) or (side==2 and r2==0): continue
                    t=list(s); t[r*n+c]=0; t[r2*n+c]=side; pushes.append(tuple(t))
        return caps if caps else pushes
    @lru_cache(maxsize=None)
    def win(s, side):  # player 'side' to move wins (normal play)?
        for t in moves(s, side):
            if not win(t, 3-side): return True
        return False
    start=tuple([1]*n+[0]*n+[2]*n)
    return win(start,1)
if __name__=="__main__":
    g=[0, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 0, 5, 2, 2]
    print("n  flat_first_wins  g(n)!=0 | cyl_first_wins  g(n-3)==0")
    for n in range(1,13):
        f=solve(n,False)
        c=solve(n,True) if n>=3 else None
        pred_c = (g[n-3]==0) if n>=3 else None
        print(n, f, g[n]!=0, "|", c, pred_c, "" if c==pred_c else "  <-- MISMATCH" , "" if f==(g[n]!=0) else "  <-- FLAT MISMATCH")
        sys.stdout.flush()
