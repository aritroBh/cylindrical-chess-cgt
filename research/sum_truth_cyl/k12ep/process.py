import json, os, sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import pawns as P
import checker as C

OUT=os.path.dirname(os.path.abspath(__file__))

def promote_distance_beta(W,H,beta,Wp,Bp,pos,stm):
    # beta credited side; compute dp(beta) using cylcgt promote_distance for beta
    board=P.Board(W,H,True,True)
    # promote_distance expects pos with side? It uses pos and side. Use board,pos,beta
    return P.promote_distance(board,pos,beta)

def beta_for_root(root):
    W=root['W']; H=root['H']; Wp=root['Wp']; Bp=root['Bp']; ep=root['ep']; stm=root['stm']
    board=P.Board(W,H,True,True)
    pos=C.make_pos(Wp,Bp,ep,W,H)
    wp = C.has_passed_side(board,pos,'W',W,H) if False else (len(C.passed_pawns_list(board,pos,'W',W,H))>0)
    bp = len(C.passed_pawns_list(board,pos,'B',W,H))>0
    # single
    if wp and not bp:
        return 'W'
    if bp and not wp:
        return 'B'
    if wp and bp:
        # race: use Corollary rule N side to move
        # dp for both
        dpN = P.promote_distance(board,pos,stm)
        other = 'B' if stm=='W' else 'W'
        dpM = P.promote_distance(board,pos,other)
        # b = N if dp(N) <= dp(M) else M
        if dpN <= dpM:
            return stm
        else:
            return other
    return None

def kpsolve_line(root):
    W=root['W']; H=root['H']; Wp=root['Wp']; Bp=root['Bp']; ep=root['ep']; stm=root['stm']
    tokens=[]
    for (f,r) in Wp:
        tokens.append(f"K" if False else f"P{chr(ord('a')+f)}{r}")
    # fix piece letters
    tokens=[]
    for (f,r) in Wp:
        tokens.append(f"P{chr(ord('a')+f)}{r}".replace('P','P'))  # placeholder
    # Actually uppercase P
    tokens=[]
    for (f,r) in Wp:
        tokens.append(f"P{chr(ord('a')+f)}{r}".upper() if False else f"p".upper()+chr(ord('a')+f)+str(r))
    # White pawns uppercase P
    toks=[]
    for (f,r) in Wp:
        toks.append(f"P{chr(ord('a')+f)}{r}")
    for (f,r) in Bp:
        toks.append(f"p{chr(ord('a')+f)}{r}")
    toks.append(f"K{chr(ord('a')+0)}1")
    toks.append(f"k{chr(ord('a')+0)}{H}")
    # side to move
    side = 'w' if stm=='W' else 'b'
    # ep target
    if ep is None:
        epstr='-'
    else:
        t=ep[0]; epstr=f"{chr(ord('a')+t[0])}{t[1]}"
    return " ".join(toks) + f" {side} {epstr}"

def main():
    with open(os.path.join(OUT,'roots.json')) as f:
        roots=json.load(f)
    # self-test passed on every root
    mism=0
    rows=[]
    for root in roots:
        W=root['W']; H=root['H']; Wp=root['Wp']; Bp=root['Bp']; ep=root['ep']; stm=root['stm']
        board=P.Board(W,H,True,True)
        pos=C.make_pos(Wp,Bp,ep,W,H)
        # cylcgt passed
        cW = P.passed(board,pos,'W')
        cB = P.passed(board,pos,'B')
        # our passed
        oW = len(C.passed_pawns_list(board,pos,'W',W,H))>0
        oB = len(C.passed_pawns_list(board,pos,'B',W,H))>0
        if cW!=oW or cB!=oB:
            mism+=1
        beta=beta_for_root(root)
        cert = C.check_certified(W,H,Wp,Bp,ep,stm,beta)
        # has passer?
        hasp = oW or oB
        single = (oW ^ oB)
        race = (oW and oB)
        rows.append({'root':root,'beta':beta,'certified':cert,'single':single,'race':race,'wp':oW,'bp':oB,'line':kpsolve_line(root)})
    print('passed mismatches',mism,'of',len(roots))
    # save rows summary (without root maybe)
    # save lines
    with open(os.path.join(OUT,'kpin.txt'),'w') as f:
        for r in rows:
            f.write(r['line']+"\n")
    # save metadata
    meta=[]
    for r in rows:
        meta.append({'W':r['root']['W'],'H':r['root']['H'],'stm':r['root']['stm'],'beta':r['beta'],'certified':r['certified'],'single':r['single'],'race':r['race'],'line':r['line']})
    with open(os.path.join(OUT,'meta.json'),'w') as f:
        json.dump(meta,f)
    # print counts
    from collections import Counter
    for key in ['W','H']:
        pass
    # board-level table
    for (W,H) in sorted(set((r['root']['W'],r['root']['H']) for r in rows)):
        sub=[r for r in rows if r['root']['W']==W and r['root']['H']==H]
        print(W,H,'roots',len(sub),'single',sum(r['single'] for r in sub),'race',sum(r['race'] for r in sub),'cert',sum(r['certified'] for r in sub))

if __name__=='__main__':
    main()
