from kb import B
from cert import Cert
import subprocess
Bd=B(7,6,True); C=Cert(Bd,[0,1,2])
cands=["Kf5 kc6 Pe4 pb3 w -","Kf5 kc6 Pe3 pb3 w -","Kf5 kc6 Pe4 pb3 b -"]
for t in cands[:2]:
    Q=Bd.parse(t); print(t,"minT",C.minT(Q,6,qs=True),"mu",C.mu(Q),"L3(2)",C.L3(Q,2,qs=True))
out=subprocess.run(["./kp","--board","cyl:7x6","--ep","on","--promote","Q","--pmodel"],input="\n".join(cands[:2])+"\n",capture_output=True,text=True).stdout
print(out)
