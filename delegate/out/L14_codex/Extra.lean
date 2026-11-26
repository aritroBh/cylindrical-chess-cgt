import CylChess.Claims.L7a_NamedRings
import CylChess.Claims.L7a_S6Rings
import CylChess.Claims.L7b_Mobius
import CylChess.Census
import CylChess.Dawson

open CylChess CylChess.Claims
namespace Referee
def diag := Position.ofSquares [(0,2),(1,4)] [(0,4),(0,7)]
def beforeFlag := Position.ofSquares [(0,2),(1,2)] [(0,4),(0,7)]
def withFlag : Position := {diag with ep := some (1,4)}
#eval (moves Settings.default Census.board beforeFlag .white).contains withFlag
#eval [beforeFlag, diag, withFlag].map fun p =>
  (!(hasPassed Settings.default Census.board p .white || hasPassed Settings.default Census.board p .black),
   p.normalize Settings.default Census.board == p)
#eval [diag, withFlag].map fun p => Search.isValue Census.env 400 p Tree.zero
#eval [Color.white, .black].map fun c => Game.wins Census.env 400 (Comp.ofPosition Census.env withFlag) c

def C11 := S6 [('c',4),('d',6),('e',3),('h',3),('i',2),('k',2)]
  [('a',4),('b',7),('d',7),('f',7),('g',6),('j',6)]
#eval Wide.sigString (Wide.defEnv (Wide.cylinder 11)) 5000 C11 4
#eval allSettings.map fun s => (s.ep,s.race,Wide.sigString (env s cyl3) 400 ring6 4)
end Referee

open CylChess.Dawson in
#eval (grundy (Board.strip 1) 10 [.w,.e,.e] .white,
       grundy (Board.strip 1) 10 [.w,.e,.e] .black)

namespace Referee
def tallDuels : Board := {files := 5, ranks := 1005, topology := .flat}
def duels := Position.ofSquares [(0,1001),(4,1001)] [(1,1002),(3,1002)]
def duelEnv := env Settings.default tallDuels
#eval (duels.valid tallDuels, hasPassed Settings.default tallDuels duels .white,
  hasPassed Settings.default tallDuels duels .black,
  Wide.WH duelEnv 10 duels 0 .black, Wide.wideRun duelEnv 10 duels 0 .black)
end Referee
