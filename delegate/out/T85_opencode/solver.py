#!/usr/bin/env python3
import argparse, itertools, json, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--H', type=int, required=True)
    ap.add_argument('--ep', type=int, default=1)
    ap.add_argument('--race', choices=['mover','opponent'], default='mover')
    ap.add_argument('--maxpawns', type=int, default=4)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    global EP_AWARE, RACE_RULE, BIG, N, H
    EP_AWARE = bool(args.ep)
    RACE_RULE = args.race
    BIG = 256
    N = args.n
    H = args.H

    squares = [(f,r) for f in range(N) for r in range(2, H)]

    def has_passed(whites, blacks, right):
        wset=set(whites); bset=set(blacks)
        for (f,r) in whites:
            bad=False
            for bf in ((f-1)%N, f, (f+1)%N):
                for (bf2,br) in blacks:
                    if bf2==bf and br>r:
                        bad=True;break
                if bad: break
            if bad: continue
            if EP_AWARE and right is not None and right[0]=='W' and right[1]==(f,r):
                for bf in ((f-1)%N,(f+1)%N):
                    if (bf,r) in bset:
                        bad=True;break
            if not bad:
                return True
        for (f,r) in blacks:
            bad=False
            for bf in ((f-1)%N, f, (f+1)%N):
                for (bf2,br) in whites:
                    if bf2==bf and br<r:
                        bad=True;break
                if bad: break
            if bad: continue
            if EP_AWARE and right is not None and right[0]=='B' and right[1]==(f,r):
                for bf in ((f-1)%N,(f+1)%N):
                    if (bf,r) in wset:
                        bad=True;break
            if not bad:
                return True
        return False

    def passed_sides(whites, blacks, right):
        w=False; b=False
        wset=set(whites); bset=set(blacks)
        for (f,r) in whites:
            bad=False
            for bf in ((f-1)%N, f, (f+1)%N):
                for (bf2,br) in blacks:
                    if bf2==bf and br>r:
                        bad=True;break
                if bad: break
            if bad: continue
            if EP_AWARE and right is not None and right[0]=='W' and right[1]==(f,r):
                for bf in ((f-1)%N,(f+1)%N):
                    if (bf,r) in bset:
                        bad=True;break
            if not bad:
                w=True
        for (f,r) in blacks:
            bad=False
            for bf in ((f-1)%N, f, (f+1)%N):
                for (bf2,br) in whites:
                    if bf2==bf and br<r:
                        bad=True;break
                if bad: break
            if bad: continue
            if EP_AWARE and right is not None and right[0]=='B' and right[1]==(f,r):
                for bf in ((f-1)%N,(f+1)%N):
                    if (bf,r) in wset:
                        bad=True;break
            if not bad:
                b=True
        return (w,b)

    def components_files(whites, blacks):
        occ = set(f for f,r in whites)|set(f for f,r in blacks)
        if not occ:
            return []
        if len(occ)==N:
            return [tuple(range(N))]
        occb=[f in occ for f in range(N)]
        start=None
        for i in range(N):
            if not occb[i]:
                start=i; break
        i=(start+1)%N
        cur=[]
        comps=[]
        visited=0
        while visited<N:
            if occb[i]:
                cur.append(i)
            else:
                if cur:
                    comps.append(tuple(cur)); cur=[]
            i=(i+1)%N
            visited+=1
        if cur:
            comps.append(tuple(cur))
        return comps

    def make_comp(files, whites, blacks, right):
        fs=set(files)
        w=frozenset(sq for sq in whites if sq[0] in fs)
        b=frozenset(sq for sq in blacks if sq[0] in fs)
        r = right if (right is not None and right[1][0] in fs) else None
        return (tuple(sorted(files)), w, b, r)

    def right_key(right):
        if right is None: return None
        return (right[0], right[1])

    def gen_moves(whites, blacks, side, right, allowed_files):
        occ = set(whites)|set(blacks)
        wset=set(whites); bset=set(blacks)
        res=[]
        pawns = list(whites if side=='W' else blacks)
        allfiles = set(range(N))
        allowed = allfiles if allowed_files is None else set(allowed_files)
        for (f,r) in pawns:
            if side=='W':
                nr=r+1
                if nr<=H and (f,nr) not in occ and f in allowed:
                    newW = (wset - {(f,r)}) | {(f,nr)}
                    newB = set(bset)
                    newRight=None
                    res.append(('move', frozenset(newW), frozenset(newB), newRight))
                if r==2 and r+2<=H and (f,r+1) not in occ and (f,r+2) not in occ and f in allowed:
                    newW = (wset - {(f,r)}) | {(f,r+2)}
                    newB = set(bset)
                    newRight = ('W',(f,r+2))
                    res.append(('move', frozenset(newW), frozenset(newB), newRight))
                for df in (-1,1):
                    tf=(f+df)%N
                    if f not in allowed: continue
                    if tf not in allowed: continue
                    nr=r+1
                    if nr>H: continue
                    target=(tf,nr)
                    if target in bset:
                        newW = (wset - {(f,r)}) | {target}
                        newB = bset - {target}
                        newRight=None
                        res.append(('move', frozenset(newW), frozenset(newB), newRight))
                    if EP_AWARE and right is not None and right[0]=='B' and right[1]==(tf,r):
                        po=(tf,r+1)
                        if po not in occ:
                            newW = (wset - {(f,r)}) | {po}
                            newB = bset - {(tf,r)}
                            newRight=None
                            res.append(('move', frozenset(newW), frozenset(newB), newRight))
            else:
                nr=r-1
                if nr>=1 and (f,nr) not in occ and f in allowed:
                    newB = (bset - {(f,r)}) | {(f,nr)}
                    newW = set(wset)
                    newRight=None
                    res.append(('move', frozenset(newW), frozenset(newB), newRight))
                if r==H-1 and r-2>=1 and (f,r-1) not in occ and (f,r-2) not in occ and f in allowed:
                    newB = (bset - {(f,r)}) | {(f,r-2)}
                    newW = set(wset)
                    newRight = ('B',(f,r-2))
                    res.append(('move', frozenset(newW), frozenset(newB), newRight))
                for df in (-1,1):
                    tf=(f+df)%N
                    if f not in allowed: continue
                    if tf not in allowed: continue
                    nr=r-1
                    if nr<1: continue
                    target=(tf,nr)
                    if target in wset:
                        newB = (bset - {(f,r)}) | {target}
                        newW = wset - {target}
                        newRight=None
                        res.append(('move', frozenset(newW), frozenset(newB), newRight))
                    if EP_AWARE and right is not None and right[0]=='W' and right[1]==(tf,r):
                        po=(tf,r-1)
                        if po not in occ:
                            newB = (bset - {(f,r)}) | {po}
                            newW = wset - {(tf,r)}
                            newRight=None
                            res.append(('move', frozenset(newW), frozenset(newB), newRight))
        out=[]
        for (_,nw,nb,nr) in res:
            wps,bps = passed_sides(set(nw),set(nb),nr)
            if wps or bps:
                out.append(('term', wps, bps, side))
            else:
                nside = 'B' if side=='W' else 'W'
                ns = (nw, nb, nside, nr)
                out.append(('move', ns))
        return out

    w_memo={}
    def w_winner(state):
        whites,blacks,side,right = state
        key = (whites, blacks, side, right_key(right))
        if key in w_memo:
            return w_memo[key]
        moves = gen_moves(set(whites), set(blacks), side, right, None)
        win=False
        for m in moves:
            if m[0]=='term':
                wps,bps,mover = m[1],m[2],m[3]
                if wps and bps:
                    if RACE_RULE=='mover':
                        winner=mover
                    elif RACE_RULE=='opponent':
                        winner='B' if mover=='W' else 'W'
                    else:
                        winner=mover
                elif wps:
                    winner='W'
                else:
                    winner='B'
                if winner==side:
                    win=True;break
            else:
                ns=m[1]
                if w_winner(ns)==side:
                    win=True;break
        winner = side if win else ('B' if side=='W' else 'W')
        w_memo[key]=winner
        return winner

    def reach_positions(whites, blacks, right):
        seen=set()
        stack=[]
        for ss in ('W','B'):
            st=(frozenset(whites), frozenset(blacks), ss, right)
            k=(frozenset(whites), frozenset(blacks), ss, right_key(right))
            if k not in seen:
                seen.add(k); stack.append(st)
        out=set()
        while stack:
            st=stack.pop()
            w,b,side,right = st
            out.add((w,b,side,right_key(right)))
            if passed_sides(set(w),set(b),right)[0] or passed_sides(set(w),set(b),right)[1]:
                continue
            moves = gen_moves(set(w),set(b),side,right,None)
            for m in moves:
                if m[0]=='term':
                    continue
                ns=m[1]
                nw,nb,nside,nr = ns
                k=(nw,nb,nside,right_key(nr))
                if k not in seen:
                    seen.add(k); stack.append((nw,nb,nside,nr))
        return out

    def threat2(comp, t):
        files, w0, b0, r0 = comp
        fset=set(files)
        seen=set()
        start_key=(frozenset(w0), frozenset(b0), right_key(r0))
        seen.add(start_key)
        q=[(frozenset(w0), frozenset(b0), r0)]
        while q:
            w,b,right = q.pop()
            wset=set(w); bset=set(b)
            for side in ('W','B'):
                moves = gen_moves(wset, bset, side, right, fset)
                for m in moves:
                    if m[0]=='term':
                        wps,bps,mover = m[1],m[2],m[3]
                        if (t=='W' and wps) or (t=='B' and bps):
                            return True
                    else:
                        ns=m[1]
                        nw,nb,nside,nr = ns
                        key=(nw,nb,right_key(nr))
                        if key not in seen:
                            seen.add(key)
                            q.append((nw,nb,nr))
        return False

    threat = threat2

    def is_hss(whites, blacks, right):
        ws=frozenset(whites); bs=frozenset(blacks)
        allr=reach_positions(ws, bs, right)
        for Y in allr:
            w,b,side,rk = Y
            right=rk
            comps = components_files(set(w), set(b))
            if len(comps)<2: continue
            comp_states=[make_comp(cf, set(w), set(b), right) for cf in comps]
            tW=[threat(c,'W') for c in comp_states]
            tB=[threat(c,'B') for c in comp_states]
            for i in range(len(comps)):
                for j in range(len(comps)):
                    if i==j: continue
                    if tW[i] and tB[j]:
                        return False
        return True

    def condition_E(whites, blacks, right):
        ws=frozenset(whites); bs=frozenset(blacks)
        allr=reach_positions(ws, bs, right)
        for Y in allr:
            w,b,side,rk = Y
            right=rk
            comps = components_files(set(w), set(b))
            if len(comps)<2: continue
            if right is None: continue
            rf = right[1][0]
            cfiles = [cf for cf in comps if rf in set(cf)]
            if not cfiles: continue
            capturer = 'B' if right[0]=='W' else 'W'
            mover_pawns = set(w) if right[0]=='W' else set(b)
            if right[1] not in mover_pawns:
                continue
            enemy_pawns = set(b) if capturer=='B' else set(w)
            f,rr = right[1]
            usable=False
            for df in (-1,1):
                if ((f+df)%N, rr) in enemy_pawns:
                    usable=True;break
            if usable:
                return False
        return True

    def canonicalize_items(items):
        return tuple(sorted(items, key=lambda x: (x[0], str(x))))

    def comp_moves(comp, side):
        files, w0, b0, r0 = comp
        fset=set(files)
        wset=set(w0); bset=set(b0)
        out_moves=[]
        moves = gen_moves(wset, bset, side, r0, fset)
        for m in moves:
            if m[0]=='term':
                wps,bps,mover = m[1],m[2],m[3]
                if wps and bps:
                    if RACE_RULE=='mover':
                        winner=mover
                    elif RACE_RULE=='opponent':
                        winner='B' if mover=='W' else 'W'
                    else:
                        winner=mover
                elif wps:
                    winner='W'
                else:
                    winner='B'
                sign = BIG if winner=='W' else -BIG
                out_moves.append([('Z', sign)])
            else:
                ns=m[1]
                nw,nb,nside,nr = ns
                newW=set(nw); newB=set(nb)
                wps2,bps2 = passed_sides(newW,newB,nr)
                if wps2 or bps2:
                    if wps2 and bps2:
                        if RACE_RULE=='mover':
                            winner=side
                        elif RACE_RULE=='opponent':
                            winner='B' if side=='W' else 'W'
                        else:
                            winner=side
                    elif wps2:
                        winner='W'
                    else:
                        winner='B'
                    sign = BIG if winner=='W' else -BIG
                    out_moves.append([('Z', sign)])
                else:
                    comps = components_files(newW,newB)
                    items=[]
                    for cf in comps:
                        items.append(('C', make_comp(cf, newW, newB, nr)))
                    out_moves.append(items)
        return out_moves

    s_memo={}
    def s_winner(state):
        side, items = state
        key=(side, items)
        if key in s_memo:
            return s_memo[key]
        items_list=list(items)
        moves=[]
        for idx,item in enumerate(items_list):
            if item[0]=='Z':
                k=item[1]
                if side=='W' and k>0:
                    ni=list(items_list)
                    if k-1==0:
                        del ni[idx]
                    else:
                        ni[idx]=('Z', k-1)
                    other='B'
                    moves.append((other, canonicalize_items(ni)))
                if side=='B' and k<0:
                    ni=list(items_list)
                    if k+1==0:
                        del ni[idx]
                    else:
                        ni[idx]=('Z', k+1)
                    other='W'
                    moves.append((other, canonicalize_items(ni)))
            else:
                comp=item[1]
                for repl in comp_moves(comp, side):
                    ni = items_list[:idx] + items_list[idx+1:] + repl
                    other = 'B' if side=='W' else 'W'
                    moves.append((other, canonicalize_items(ni)))
        win=False
        for (ns_side, ns_items) in moves:
            if s_winner((ns_side, ns_items))==side:
                win=True;break
        winner = side if win else ('B' if side=='W' else 'W')
        s_memo[key]=winner
        return winner

    def classify(w_start, b_start):
        if w_start=='W' and b_start=='W': return 'L'
        if w_start=='B' and b_start=='B': return 'R'
        if w_start=='W' and b_start=='B': return 'N'
        if w_start=='B' and b_start=='W': return 'P'

    t0=time.time()
    count_tested=0
    mismatches=[]
    max_examples=5
    for m in range(0, args.maxpawns+1):
        for positions in itertools.combinations(squares, m):
            for colors in itertools.product('WB', repeat=m):
                whites=set(); blacks=set()
                for sq,c in zip(positions,colors):
                    if c=='W': whites.add(sq)
                    else: blacks.add(sq)
                right=None
                wfs=frozenset(whites); bfs=frozenset(blacks)
                if passed_sides(whites,blacks,right)[0] or passed_sides(whites,blacks,right)[1]:
                    continue
                if not is_hss(whites,blacks,right):
                    continue
                if not condition_E(whites,blacks,right):
                    continue
                phiW=sum(H-r for f,r in whites)
                phiB=sum(r-1 for f,r in blacks)
                if not (BIG > max(phiW,phiB)):
                    continue
                count_tested+=1
                wW = w_winner((wfs,bfs,'W',right))
                wB = w_winner((wfs,bfs,'B',right))
                w_class = classify(wW,wB)
                comps = components_files(whites,blacks)
                items=[]
                for cf in comps:
                    items.append(('C', make_comp(cf, whites, blacks, right)))
                ic = canonicalize_items(items)
                sW = s_winner(('W', ic))
                sB = s_winner(('B', ic))
                s_class = classify(sW,sB)
                if w_class != s_class:
                    if len(mismatches) < max_examples:
                        mismatches.append({
                            'positions': positions,
                            'colors': colors,
                            'whites': sorted(whites),
                            'blacks': sorted(blacks),
                            'w_class': w_class, 's_class': s_class,
                            'wW': wW, 'wB': wB, 'sW': sW, 'sB': sB,
                        })
    elapsed=time.time()-t0
    result = {
        'n': N, 'H': H, 'ep_aware': EP_AWARE, 'race': RACE_RULE,
        'maxpawns': args.maxpawns,
        'count_tested': count_tested,
        'num_mismatches': len(mismatches),
        'mismatches': mismatches,
        'elapsed_sec': elapsed,
    }
    with open(args.out,'w') as fh:
        json.dump(result, fh, indent=2, default=str)
    print(json.dumps({k:result[k] for k in ['n','H','count_tested','num_mismatches','elapsed_sec']}, indent=2))

if __name__=='__main__':
    main()
