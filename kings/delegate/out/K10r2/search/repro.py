# reproduce the note's "parked" counts: Ka1 and black king at the top of the a-file, pawns on c..W-2 (0-based), <=3 a side
import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import chk
from sweep import *
def run(W,H,maxper,eps,lab):
    B=Bd(W,H); T=Tally()
    files=list(range(2,W-1))
    kings=[((0,1),(0,H))]
    pos=set(); 
    def g():
        for y in gen_exhaustive(B,files,maxper,kings,eps=eps): yield y
    process(B,g(),T,lab,dedupe=False)
    print(lab,'legal positions',T.pos_generated,'certified positions(with stm)',T.pos_tested,'instances',T.inst_cert,'viol',len(T.violations),'X',len(T.xs),'rss',chk.MAXRSS//2**20,flush=True)
    return T
for (W,H,mp) in [(6,6,3),(7,6,2),(8,6,2),(6,7,3),(6,5,3)]:
    run(W,H,mp,False,'repro_noep_%dx%d_%d'%(W,H,mp))
    run(W,H,mp,True,'repro_ep_%dx%d_%d'%(W,H,mp))
