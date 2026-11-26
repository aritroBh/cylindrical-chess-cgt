import CylChess.SearchWide
import CylChess.Families
def q2 := CylChess.Position.ofSquares [(1,2),(2,4),(5,3),(6,6)] [(0,4),(3,6),(4,7),(6,7)]
#eval CylChess.Wide.wideRun (CylChess.Wide.defEnv (CylChess.Wide.mobius 7)) 1000 q2 0 CylChess.Color.white
