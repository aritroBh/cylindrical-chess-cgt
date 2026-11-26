import sys,time
sys.path.insert(0,'delegate/out/L12_opencode')
from solver import *
posGMirror = Position_ofSquares([sqr('b',2),sqr('a',2),sqr('a',3)],
                               [sqr('b',5),sqr('b',6),sqr('a',6)], flat8)
env_default=make_env(('aware','count'), flat8)
print("mirror default isValue:", isValue(env_default,400,posGMirror,EIGHTH))
for ep in ['aware','textbook','off']:
    for r in ['count','mover','opponent']:
        e=make_env((ep,r), flat8)
        print(ep,r, "mirror isValue:", isValue(e,400,posGMirror,EIGHTH))
