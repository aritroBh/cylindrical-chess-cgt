import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mobius_rings_proof'))
import rgraph
from fgame import FBoard
rgraph.Board = FBoard
from rgraph import reduced, solve, stats, iso, ins
