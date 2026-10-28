"""mkproof.py -- render per-case certificates (proof DAGs) for the 26 non-shuttle moves of Z_B as text.
usage: mkproof.py children_all.txt [first-n-lines]  > certs.md"""
import sys, importlib
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, greedy

def desc(p):
    wk,bk,wp,bp,ep,stm=p
    w='K'+pm.nm(wk)+''.join(' P'+pm.nm(s) for s in wp)
    b='k'+pm.nm(bk)+''.join(' p'+pm.nm(s) for s in bp)
    return '%s | %s'%(w,b)

def mvtxt(p,lab,q):
    """lab with '+' if it gives check"""
    if q=='PROMO': return lab
    if pm.in_check(q,q[5]): return lab+'+'
    return lab

def build(p):
    importlib.reload(greedy)
    greedy.add(p)
    return greedy.S, greedy.D

def whynot(q):
    """why the side to move at q cannot make the king / pawn moves that a reader might expect"""
    wk,bk,wp,bp,ep,stm=q
    white=stm==0
    ok,ek=(wk,bk) if white else (bk,wk)
    op,ep_=(wp,bp) if white else (bp,wp)
    legal=set(l for l,_ in pm.moves(q))
    kn=('K' if white else 'k')+pm.nm(ok)
    kmoves=set()
    for l in legal:
        if l.startswith('K'): kmoves.add(l[-2:])
    parts=[]
    for t in pm.KN[ok]:
        if pm.nm(t) in kmoves: continue
        if t in op: parts.append('%s own pawn'%pm.nm(t)); continue
        if t in pm.KADJ[ek]: parts.append('%s next to %s'%(pm.nm(t),'k' if white else 'K')); continue
        atk=[pm.nm(s) for s in ep_ if s!=t and t in pm.pawn_attacks(s,not white)]
        if atk: parts.append('%s attacked by %s%s'%(pm.nm(t),'p' if white else 'P',','.join(atk)))
        else: parts.append('%s ?'%pm.nm(t))
    notes=[]
    chk=pm.in_check(q,stm)
    if chk:
        att=[('p' if white else 'P')+pm.nm(s) for s in ep_ if ok in pm.pawn_attacks(s,not white)]
        notes.append('in check from %s: only king moves and captures of the checking pawn are legal'%(','.join(att) if att else 'the king?'))
    if parts: notes.append('%s cannot go to %s'%(kn,'; '.join(parts)))
    d=1 if white else -1
    for s in ([] if chk else op):
        t=pm.mk(pm.f_(s),pm.r_(s)+d)
        names=[l for l in legal if l.startswith(pm.nm(s))]
        if not names:
            who=[]
            if t in ep_: who.append('p' if white else 'P')
            occ=None
            if t==ek: occ=('k' if white else 'K')+pm.nm(t)
            elif t in ep_: occ=('p' if white else 'P')+pm.nm(t)
            elif t in op: occ=('P' if white else 'p')+pm.nm(t)
            if occ: notes.append('%s%s is blocked by %s'%('P' if white else 'p',pm.nm(s),occ))
            else: notes.append('%s%s has no legal move'%('P' if white else 'p',pm.nm(s)))
    return '; '.join(notes)

def kind(S,p):
    lab,q,reps=S[p]
    if q=='PROMO': return 'Q'
    if reps and all(S[q2][1]=='PROMO' for l2,q2 in reps): return 'R'
    return 'N'

def render_case(p):
    S,D=build(p)
    ids={}
    order=[]
    def visit(x):
        if x in ids: return
        k=kind(S,x)
        if k=='Q': return
        ids[x]=len(ids)+1
        order.append(x)
        if k=='N':
            for l2,q2 in S[x][2]: visit(q2)
        elif k=='R':
            pass
    visit(p)
    out=[]
    for x in order:
        lab,q,reps=S[x]
        side='White' if x[5]==0 else 'Black'
        opp='Black' if x[5]==0 else 'White'
        k=kind(S,x)
        head='%s%d. %s -- %s to move [d=%d]: **%s**' % ('R' if k=='R' else 'N', ids[x], desc(x), side, D(x), mvtxt(x,lab,q))
        # group replies
        groups=[]
        for l2,q2 in reps:
            t=mvtxt(q,l2,q2)
            if S[q2][1]=='PROMO':
                tgt='%s wins by %s'%(side,S[q2][0])
            else:
                tgt='->%s%d'%('R' if kind(S,q2)=='R' else 'N',ids[q2])
            if groups and groups[-1][1]==tgt: groups[-1][0].append(t)
            else: groups.append(([t],tgt))
        body='; '.join('%s: %s'%(', '.join(g[0]),g[1]) for g in groups)
        wn=whynot(q) if q!='PROMO' else ''
        out.append(head+'. '+opp+' replies: '+body+'.'+((' ['+wn+']') if wn else ''))
    return out, ids

if __name__=='__main__':
    lines=[l.split('#') for l in open(sys.argv[1])]
    if len(sys.argv)>2: lines=lines[:int(sys.argv[2])]
    for ln in lines:
        p=pm.parse(ln[0].strip())
        out,ids=render_case(p)
        print('### root %s, move %s  (child: %s)  [%d entries]'%(ln[1].strip(),ln[2].strip(),pm.show(p),len(out)))
        print('\n'.join(out))
        print()
