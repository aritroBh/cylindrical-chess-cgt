"""children.py: print every non-shuttle child of the 16 roots (Z_B and mirror) as 'position | root | move' lines.
usage: children.py roots.txt > children.txt   (shuttle = the move whose value is D, identified by the K/k move
between the two shuttle squares)"""
import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm
SHUT={'Kb2-c3','Kc3-b2','Ka4-b5','Kb5-a4','Kb2-a3','Ka3-b2','Kb5-c4','Kc4-b5'}
for line in open(sys.argv[1]):
    line=line.strip()
    if not line: continue
    p=pm.parse(line)
    for lab,q in pm.moves(p):
        if lab in SHUT: continue
        if q=='PROMO': print('PROMO',line,lab); continue
        print(pm.show(q),'#',line,'#',lab)
