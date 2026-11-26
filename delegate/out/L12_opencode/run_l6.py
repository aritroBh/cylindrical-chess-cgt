import sys,time
sys.path.insert(0,'delegate/out/L12_opencode')
from solver import *
envX=make_env(('off','count'), cyl8)
print("shape comps", len(cyl8.components(posX)))
print("passed W", hasPassed(envX[0],cyl8,posX,W), "B", hasPassed(envX[0],cyl8,posX,B))
t0=time.time()
print("W white:", wholeBoard(envX,400,posX,W))
print("W black:", wholeBoard(envX,400,posX,B))
print("W time", time.time()-t0)
t0=time.time()
print("S white big256:", Sfun(envX,100,posX,W))
print("S black big256:", Sfun(envX,100,posX,B))
print("S time", time.time()-t0)
# big24
envX24=make_env(('off','count'), cyl8)
envX24=(envX24[0],envX24[1],24,envX24[3])
print("S white big24:", Sfun(envX24,100,posX,W))
print("S black big24:", Sfun(envX24,100,posX,B))
