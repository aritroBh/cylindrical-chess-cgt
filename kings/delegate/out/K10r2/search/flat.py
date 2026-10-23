import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import chk
from sweep import *
def fin(lab,T):
    print(lab,'legal',T.pos_generated,'tested',T.pos_tested,'inst',T.inst_cert,'VIOL',len(T.violations),'X',len(T.xs),'both',len(T.both),T.violations[:3],T.xs[:2],flush=True)
for i,(W,H) in enumerate([(5,6),(6,6),(7,6),(6,7)]):
    B=Bd(W,H,False)
    T=Tally(); process(B,gen_random_scenes(B,300000,71+i),T,'flat_scene_%dx%d'%(W,H)); fin('flat_scene_%dx%d'%(W,H),T)
    T=Tally(); process(B,gen_uniform(B,300000,81+i),T,'flat_uni_%dx%d'%(W,H)); fin('flat_uni_%dx%d'%(W,H),T)
# flat exhaustive small, kings free-ish: a-file parked and pawns on b..W-2
B=Bd(6,6,False); T=Tally()
process(B,gen_exhaustive(B,[1,2,3,4],2,kingpairs_afile(B)),T,'flat_exh_6x6',dedupe=False); fin('flat_exh_6x6',T)
# 7x6 cylinder parked, <=3 a side (reproduces K10's 496,848 count)
B=Bd(7,6); T=Tally()
process(B,gen_exhaustive(B,[2,3,4,5],3,[((0,1),(0,6))],eps=False),T,'repro_7x6_3',dedupe=False); fin('repro_7x6_3',T)
