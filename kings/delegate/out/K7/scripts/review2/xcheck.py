import sys, json, random
sys.path.insert(0,'..')
sys.path.insert(0,'../..')
sys.path.insert(0,'../../w')
import importlib.util
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
kpgen=load('kpgen','/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/kpgen.py')
sys.modules['kpgen']=kpgen
lcd=load('lcd','/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/lc.py')
from hc import Geo, Cert
rows=json.load(open('hunt_A101.json'))
random.seed(1); random.shuffle(rows)
g=Geo(7,6,True); C=Cert(g,[0,1,2])
B=kpgen.Board(7,6,True); D=lcd.Cert(B,[0,1,2])
bad=0
for r in rows[:300]:
    Q=g.parse(r['Q'])
    Qd=(Q[0],Q[1],Q[2],Q[3],Q[4],Q[5])
    T1=D.L1(Qd,qsafe=False,Tmax=5)
    mu=D.mu(Qd,False)
    if T1!=r['T1'] or min(mu,99)!=min(r['m_no'],99) and not (mu>=7 and r['m_no']>=7):
        bad+=1; print("DIFF",r['Q'],T1,r['T1'],mu,r['m_no'])
print("compared 300, diffs",bad)
