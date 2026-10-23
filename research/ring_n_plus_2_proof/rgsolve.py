import subprocess
import os; RG=os.path.join(os.path.dirname(os.path.abspath(__file__)),'rg')
def solve(lines, chunk=40):
    out=[]
    for i in range(0,len(lines),chunk):
        part=lines[i:i+chunk]
        r=subprocess.run([RG,'solve','3'],input='\n'.join(part)+'\n',capture_output=True,text=True)
        o=[x.split()[0] for x in r.stdout.split('\n') if x.strip()]
        if len(o)!=len(part):
            o=[]
            for p in part:
                r=subprocess.run([RG,'solve','3'],input=p+'\n',capture_output=True,text=True)
                x=[y.split()[0] for y in r.stdout.split('\n') if y.strip()]
                o.append(x[0] if x else 'FULL')
        out+=o
    assert len(out)==len(lines)
    return out
