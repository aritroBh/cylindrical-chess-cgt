import CylChess.SearchWide
import CylChess.Families
def q := CylChess.Position.ofSquares [(1,2),(2,4),(5,3),(6,6)] [(0,6),(3,6),(4,7),(6,7)]
#eval (CylChess.moves CylChess.Settings.default (CylChess.Wide.mobius 7) q CylChess.Color.black).length
