import sys,os,json,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import chk
from sweep import *
from ablate import ablation
OUT=os.path.dirname(os.path.abspath(__file__))
names=sys.argv[1:]
def log(*a):
    print(time.strftime('%H:%M:%S'),*a,flush=True)

def finish(label,B,T,secs):
    d={'label':label,'generated_legal':T.pos_generated,'positions_tested':T.pos_tested,'instances_certified':T.inst_cert,
       'violations':T.violations[:50],'n_viol':len(T.violations),'kp_X':len(T.xs),'kp_X_examples':T.xs[:5],'both_colours_certified':len(T.both),
       'features':dict(T.feat),'secs':secs,'maxrss_kb':chk.MAXRSS}
    json.dump(d,open(os.path.join(OUT,'res_%s.json'%label),'w'),indent=1)
    log(label,'legal',T.pos_generated,'tested',T.pos_tested,'inst',T.inst_cert,'VIOL',len(T.violations),'X',len(T.xs),'both',len(T.both),'rss(MB)',chk.MAXRSS//1048576,'%.0fs'%secs)

def task_random(W,H,n,seed):
    B=Bd(W,H); T=Tally(); lab='scene_%dx%d'%(W,H)
    t=process(B,gen_random_scenes(B,n,seed),T,lab); finish(lab,B,T,t)
def task_uniform(W,H,n,seed,parked):
    B=Bd(W,H); T=Tally(); lab='uni_%s_%dx%d'%('parked' if parked else 'free',W,H)
    t=process(B,gen_uniform(B,n,seed,parked=parked),T,lab); finish(lab,B,T,t)
def task_exh(W,H,files,maxper,kings,lab,freekings=False):
    B=Bd(W,H); T=Tally()
    if kings=='a': kp_=kingpairs_afile(B)
    else:
        kp_=[]
        sq=[(f,r) for f in range(W) for r in range(1,H+1)]
        for a in sq:
            for b in sq:
                if B.kdist(a,b)>=2: kp_.append((a,b))
    t=process(B,gen_exhaustive(B,files,maxper,kp_),T,lab,dedupe=False); finish(lab,B,T,t)
def task_ablate(W,H,n,seed):
    B=Bd(W,H); lab='ablate_%dx%d'%(W,H)
    r=ablation(B,gen_random_scenes(B,n,seed),lab)
    json.dump({k:list(v) for k,v in r.items()},open(os.path.join(OUT,'res_%s.json'%lab),'w'),indent=1)
    log(lab,json.dumps({k:(v[0],v[1]) for k,v in r.items()}))

TASKS={
 'scene': lambda: [task_random(W,H,600000,11+i) for i,(W,H) in enumerate([(5,6),(6,6),(7,6),(8,6),(6,7),(6,5)])],
 'uni_free': lambda: [task_uniform(W,H,500000,21+i,False) for i,(W,H) in enumerate([(5,6),(6,6),(7,6),(8,6),(6,7)])],
 'uni_parked': lambda: [task_uniform(W,H,500000,31+i,True) for i,(W,H) in enumerate([(5,6),(6,6),(7,6),(8,6),(6,7)])],
 'exh_parked': lambda: [
    task_exh(5,6,[2,3],3,'a','exh_a_5x6_cd3'),
    task_exh(6,6,[2,3,4],3,'a','exh_a_6x6_cde3'),
    task_exh(7,6,[2,3,4,5],2,'a','exh_a_7x6_cdef2'),
    task_exh(8,6,[2,3,4,5,6],2,'a','exh_a_8x6_cdefg2'),
    task_exh(6,7,[2,3,4],2,'a','exh_a_6x7_cde2')],
 'exh_free': lambda: [
    task_exh(5,6,[2,3],3,'free','exh_free_5x6_cd3'),
    task_exh(4,6,[2,3],3,'free','exh_free_4x6_cd3')],
 'ablate': lambda: [task_ablate(W,H,400000,41+i) for i,(W,H) in enumerate([(5,6),(6,6),(7,6),(8,6),(6,7)])],
}
for n in names:
    log('START',n); TASKS[n](); log('DONE',n)
