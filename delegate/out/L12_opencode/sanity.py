import sys
sys.path.insert(0,'delegate/out/L12_opencode')
from solver import *
# W a2 / B b4
p=Position_ofSquares([sqr('a',2)],[sqr('b',4)],flat8)
env=make_env(('aware','count'),flat8)
print("W a2 / B b4 isValue 0?", isValue(env,200,p,ZERO_TREE if False else ('node',(),())))
# zero tree
ZERO_T=('node',(),())
print("value 0?", isValue(env,200,p,ZERO_T))
# *1?
print("value *1?", isValue(env,200,p,star(1)))
