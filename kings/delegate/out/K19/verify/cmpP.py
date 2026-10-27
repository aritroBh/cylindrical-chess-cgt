from lg import *
import subprocess
cases=[('cyl:8x8',8,8,True,'b','Kg4 ka4 pa5','w'),('cyl:8x8',8,8,True,'b','Kh6 ka4 pa5','w'),('cyl:8x8',8,8,True,'b','Kg6 ka4 pa5','w'),('cyl:8x8',8,8,True,'b','Ka6 ka4 pa5','w'),
('cyl:8x8',8,8,True,'b','Kd5 kd7 pe7','w'),('cyl:8x8',8,8,True,'b','Kf7 kd7 pe7','w'),('cyl:8x8',8,8,True,'b','Ke5 kd7 pe7','w'),('cyl:8x8',8,8,True,'b','Kf5 kd7 pe7','w'),
('cyl:8x6',8,6,True,'w','Kb3 Pb2 kd3','b'),('cyl:8x6',8,6,True,'w','Kb3 Pb2 kc5','b'),('cyl:8x6',8,6,True,'w','Kb3 Pb2 kd4','b'),('cyl:8x6',8,6,True,'w','Kb3 Pb2 kd5','b'),
('flat:8x8',8,8,False,'b','Ke6 kg4 pg5','w'),('cyl:7x6',7,6,True,'b','Kd5 kb5 pc5','w'),('cyl:7x6',7,6,True,'b','Kb3 kb5 pc5','w')]
for board,W,H,wrap,A,pos,stm in cases:
    G=Game(W,H,wrap,A,set(range(W)),queen=False,mate=True,confine=False)
    T=G.T(parse(pos),0,tmax=(12 if pos in ('Kf7 kd7 pe7','Kg4 ka4 pa5','Kh6 ka4 pa5','Kg6 ka4 pa5','Ka6 ka4 pa5','Kb3 Pb2 kd3','Kb3 Pb2 kd4','Kb3 Pb2 kd5','Ke6 kg4 pg5','Kd5 kb5 pc5') else 8))
    lg_win = T is not None
    out=subprocess.run(['./kp_p','--board',board,'--ep','on','--promote','QRBN','--cap','1','--pmodel'],input=pos+f' {stm} -\n',capture_output=True,text=True).stdout.strip().splitlines()[-1]
    res=out.split('|')[1].split()[0]
    kp_win = (res=='L') if A=='b' else (res=='W')
    print(flush=True,*[f'{board:9s} {pos:16s} {stm}  lg T={T}  kp_p={res}  {"OK" if kp_win==lg_win else "MISMATCH"}'])
