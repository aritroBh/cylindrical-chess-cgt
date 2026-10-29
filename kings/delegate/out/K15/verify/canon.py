import sys,re
def parse_state(s,W,H):
    wp=set();bp=set();wk=bk=None
    for t in s.split():
        if len(t)<3 or t[0] not in 'KkPp': continue
        f=ord(t[1])-97; r=int(t[2:])-1
        if t[0]=='K': wk=(f,r)
        elif t[0]=='k': bk=(f,r)
        elif t[0]=='P': wp.add((f,r))
        else: bp.add((f,r))
    return (wk,bk,frozenset(wp),frozenset(bp))
def transform(st,W,H,shift,mirror,flip,cyl):
    wk,bk,wp,bp=st
    def f_(p):
        f,r=p
        if mirror: f=-f
        f=f+shift
        if cyl: f%=W
        if flip: r=H-1-r
        return (f,r)
    wk2,bk2=f_(wk),f_(bk); wp2=frozenset(map(f_,wp)); bp2=frozenset(map(f_,bp))
    if flip: wk2,bk2,wp2,bp2=bk2,wk2,bp2,wp2   # colour swap
    return (wk2,bk2,wp2,bp2)
FW=3
def canon(closure,W,H,cyl):
    best=None
    shifts=range(W) if cyl else [0]
    for sh in shifts:
        for mi in (0,1):
            for fl in (0,1):
                if not cyl:
                    # flat: mirror about the board: f -> W-1-f
                    pass
                key=[]
                for st in closure:
                    if cyl: t=transform(st,W,H,sh,mi,fl,True)
                    else:
                        wk,bk,wp,bp=st
                        def g(p):
                            f,r=p
                            if mi: f=FW-1-f
                            if fl: r=H-1-r
                            return (f,r)
                        t=(g(wk),g(bk),frozenset(map(g,wp)),frozenset(map(g,bp)))
                        if fl: t=(t[1],t[0],t[3],t[2])
                    key.append((t[0],t[1],tuple(sorted(t[2])),tuple(sorted(t[3]))))
                key=tuple(sorted(set(key)))
                if best is None or key<best: best=key
    return best
if __name__=='__main__':
    W=int(sys.argv[1]);H=int(sys.argv[2]);cyl=sys.argv[3]=='cyl'
    seen={}
    n=0
    for fn in sys.argv[4:]:
        for ln in open(fn):
            root,cl=ln.rstrip('\n').split('\t')
            states=[parse_state(x,W,H) for x in cl.split('|')]
            states=list(set(states))
            c=canon(states,W,H,cyl); n+=1
            seen.setdefault(c,[]).append(root)
    print('dud roots',n,'distinct groups',len(seen))
    for c,r in seen.items(): print(len(r),r[0])
