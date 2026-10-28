"""mkdoc.py -- assemble PROOF.md (hand proof of Theorem A) from the generated parts.
usage: mkdoc.py children_all.txt roots.txt > PROOF.md"""
import sys
sys.path.insert(0,'/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts')
import pm, mkproof, io, contextlib

lines=[l.rstrip('\n').split('#') for l in open(sys.argv[1])][:26]
roots=[l.strip() for l in open(sys.argv[2]) if l.strip()][:8]

IDEA={
 ('Kb2-a1',1):"The king gives up the blockade of c3. Black plays c4-c3, and the pair b3+c3 beats a king on the first rank. White has no counterplay: Pa3 is blocked by ka4, and b4-b5 only delays (the king takes it, or the pair goes on).",
 ('Kb2-b1',1):"As above.",
 ('Kb2-c1',1):"As above.",
 ('b4-b5',1):"b4-b5 is captured, Ka4xb5: White has lost a pawn. Black then threatens c4-c3, b3-b2 and Ka4xa3 and the White king cannot meet them all; the Black king uses its shuttle as a waiting move (Kb5-a4) where that puts White in zugzwang. a3-a4+ only costs Black one capture.",
 ('c4-c3',2):"c4-c3 is captured, Kb2xc3 (c3 is not protected): Black has lost a pawn. If Kxa3 then b4-b5 runs and promotes (the Black king is too far); if b3-b2 then Kxb2; if Kb5 then Kc3xb3 and the king and pawns win.",
 ('Kb2-a1',3):"Black king on b5. The same plan c4-c3; the only extra resource of White is the check a3-a4+, which Black answers by capturing (Kxa4, or Kxb4 when that wins faster).",
 ('Kb2-b1',3):"As above.",
 ('Kb2-c1',3):"As above.",
 ('a3-a4',3):"a3-a4+ is a check; Black takes the other pawn, Kb5xb4 (not Kxa4). Black has won a pawn and again has b3+c4 against the king, with Pa4 harmless.",
 ('Kb5-a6',4):"The Black king leaves the b5/a4 guard. White's pawns a3, b4 march (a3-a4, a4-a5+, b4-b5+), supported by the king; Black's c4-c3+ and b3 are captured by the king with tempo.",
 ('Kb5-b6',4):"As above.",
 ('Kb5-c6',4):"As above.",
 ('c4-c3',4):"c4-c3 is answered by Kb2xb3 (b3 lost its protector when the pawn left c4, and the Black king b5 does not guard it); the king then also deals with the c-pawn while the two White pawns run.",
 ('Kc3xc4',5):"After any White move that leaves c3 and gives up control of b2, Black plays b3-b2 and b2-b1=Q cannot be stopped (3 plies).",
 ('Kc3-d2',5):"As above.",
 ('Kc3-d4',5):"As above.",
 ('b4-b5',5):"b4-b5 is captured, Ka4xb5. White has lost a pawn; Black's king goes back to a4 to attack a3 while the White king is forced to give way (zugzwang on b2/c3), and then c4-c3 or b3-b2 decides.",
 ('Ka4xa3',6):"Black has captured a3; the White b-pawn is free and Black's king on a3 is too far from b5: b4-b5 and b5-b6=Q.",
 ('b3-b2',6):"b3-b2 is captured by the king (Kxb2), after which Black has one pawn against two and White's king and pawns win the race.",
 ('Kc3-d2',7):"Black king on b5. b3-b2 wins; the check a3-a4+ gains one tempo for White only, answered by Kxb4 or Kxa4.",
 ('Kc3-d4',7):"As above.",
 ('a3-a4',7):"a3-a4 is captured by Kb5xa4; then b3-b2 / c4-c3 break through against the lone king.",
 ('Kb5-a6',8):"The Black king leaves b5/a4: a3-a4 and the pawns a4, b4 run with check on a5/b5.",
 ('Kb5-b6',8):"As above.",
 ('Kb5-c6',8):"As above.",
 ('b3-b2',8):"b3-b2 is captured (Kc3xb2); the White king then returns to b3/c4 in time and the two White pawns win.",
}

def section(i, ln):
    p=pm.parse(ln[0].strip())
    rootstr=ln[1].strip(); mv=ln[2].strip()
    ridx=roots.index(rootstr)+1
    out,ids=mkproof.render_case(p)
    s=[]
    s.append('#### C%02d. Root Z%d, move %s. Position after the move: `%s`'%(i+1,ridx,mv,pm.show(p)))
    s.append('')
    s.append('*Idea.* '+IDEA[(mv,ridx)])
    s.append('')
    s.append('Certificate (%d entries; the winner is %s):'%(len(out),'Black' if p[5]==1 else 'White'))
    s.append('')
    for o in out: s.append('- '+o)
    s.append('')
    return '\n'.join(s)

buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    pass
roots_txt=[]
import subprocess
rt=subprocess.run(['/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python','/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts/mkroots.py',sys.argv[2]],capture_output=True,text=True,env={'PYTHONPATH':'/Users/aritro/Downloads/Research/Chessendgames'}).stdout.strip().split('\n')

cases=[section(i,ln) for i,ln in enumerate(lines)]
total_entries=0

HEAD=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts/proof_head.md').read()
TAIL=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts/proof_tail.md').read()
print(HEAD)
print('## 4. The legal moves at the eight roots\n')
print('Each root is listed with every legal move of the side to move (the shuttle and the other moves) and, in brackets, the reasons why the other moves a reader might expect are illegal. A pawn that stands next to the other king does not protect itself: a king may not capture a pawn that is protected by a pawn or is adjacent to the other king.\n')
for r in rt: print('- '+r)
print('\nThat is 4 + 4 + 4 + 3 = 15 White non-shuttle moves (roots Z1, Z3, Z5, Z7) and 1 + 4 + 2 + 4 = 11 Black ones (Z2, Z4, Z6, Z8), 26 in all. (The task text and K14 say 27; the solver move lists, kpp and ref3m, and this list all give 26.)\n')
print(open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27/scripts/proof_sec5.md').read())
print('## 6. The 26 deviations\n')
print('Entries are written `N<k>` (a node whose replies are listed and lead to further entries or to a promotion), `R<k>` (a node whose replies all allow an immediate promotion). Square lists "cannot go to" are the reasons for the exclusion of moves. `d` is the number of plies, counted from the entry and including the winner\'s next move, within which the winner promotes (or mates): along every arrow `d` drops by at least 2.\n')
for c in cases: print(c)
print(TAIL)
