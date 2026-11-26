import CylChess.SearchWide
import CylChess.Families
def q2 := CylChess.Position.ofSquares [(1,2),(2,4),(5,3),(6,6)] [(0,4),(3,6),(4,7),(6,7)]
#eval CylChess.hasPassed CylChess.Settings.default (CylChess.Wide.mobius 7) q2 CylChess.Color.white
#eval CylChess.hasPassed CylChess.Settings.default (CylChess.Wide.mobius 7) q2 CylChess.Color.black
