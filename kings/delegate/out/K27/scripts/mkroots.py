import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, mkproof
SHUT={'Kb2-c3','Kc3-b2','Ka4-b5','Kb5-a4'}
for i,l in enumerate(open(sys.argv[1])):
    if i>=8: break
    p=pm.parse(l.strip())
    ms=pm.moves(p)
    sh=[lab for lab,q in ms if lab in SHUT]
    ot=[lab for lab,q in ms if lab not in SHUT]
    side='White' if p[5]==0 else 'Black'
    print('Z%d. %s -- %s to move. Shuttle %s. Other legal moves (all of them): %s. [%s]'%(i+1,mkproof.desc(p),side,sh[0],', '.join(ot),mkproof.whynot(p)))
