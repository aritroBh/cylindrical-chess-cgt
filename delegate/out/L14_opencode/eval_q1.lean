import CylChess.SearchWide
import CylChess.Families
def q1 := CylChess.Position.ofSquares [(1,2),(2,4),(5,3),(6,6)] [(0,5),(3,6),(4,7),(6,7)]
#eval CylChess.Wide.wideRun (CylChess.Wide.defEnv (CylChess.Wide.mobius 7)) 1000 q1 2 CylChess.Color.white
