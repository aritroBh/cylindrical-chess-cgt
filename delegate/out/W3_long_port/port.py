import re,sys
R=''
P=R+'paper/ieee/sections/'; D=R+'dist/tog/long/'
log=[]
def rep(path,old,new,n=1,tag=''):
    s=open(path).read()
    assert s.count(old)==n,(path,tag,s.count(old))
    ln=s[:s.index(old)].count('\n')+1
    assert old.count('\n')==new.count('\n') or path.startswith(P) or path.endswith('.bib'),(path,tag,'newline')
    s=s.replace(old,new)
    open(path,'w').write(s)
    log.append((tag,path.replace(R,''),ln,old,new))
def both(f,old,new,tag,n=1):
    rep(P+f,old,new,n,tag); rep(D+f,old,new,n,tag)

# 1 Corollary V4 (04_kings in both, identical)
both('04_kings.tex',"If also (V4) $X$ is hereditarily sum-safe (Definition~\\ref{def:hss}) and satisfies condition (E) of\nTheorem~\\ref{thm:hss}, and $\\BIG$ exceeds the number of moves either side can make, the chess result is\nthe outcome class of the components' $\\pm\\BIG$ value.",
"If also (V4) holds, that is, $X$ is hereditarily sum-safe (Definition~\\ref{def:hss}), satisfies condition (E) of\nTheorem~\\ref{thm:hss}, and $\\BIG$ exceeds the number of moves either side can make, then for that side to move\nthe chess result is the one given by the components' $\\pm\\BIG$ value.",'1 Cor V4')
# 2 C2 label
old="\\lab{C2}, two independently written programs agree,\nthe second written from the rules alone;"
rep(P+'01_intro.tex',old,"\\lab{C2}, two separately written programs agree,\nthe second from the rules alone (both AI-written; Section~\\ref{sec:verify}, Acknowledgment);",1,'2 C2 label')
rep(D+'01_intro.tex',old,"\\lab{C2}, two separately written programs agree,\nthe second from the rules alone (both AI-written; Section~S17);",1,'2 C2 label')
# 3 real kings (paper/ieee only)
s=open(P+'05_sums.tex').read()
old="Of the $38$ positions, $19$ are solved exactly\nand all agree with the outcome of the model sum; they include sums of two live components such as\n$\\{1\\mid0\\}+\\{1\\mid0\\}$ and $-1+\\{0\\mid-1\\}$. The other $19$ positions, among them every sum that is a\nsecond-player win, are only bounded, and no bound contradicts the model \\lab{C1}. So this test supports the sum\nmodel where one side wins outright and leaves the zero sums open."
new="Of the $38$ sides to move, $19$ are solved exactly\nand all agree with the outcome of the model sum; they include sums of two live components such as\n$\\{1\\mid0\\}+\\{1\\mid0\\}$ and $-1+\\{0\\mid-1\\}$. The other $19$ have only bounds, each consistent with the\nsum; all $19$ sums share one king placement \\lab{C1}. So this test supports the sum\nmodel where the solver is exact and does not contradict it elsewhere."
rep(P+'05_sums.tex',old,new,1,'3 real kings')
# 4 oracle def (09 identical)
both('09_real.tex',"for white, or as worth $0$; in the last case the end position is $\\game{\\BIG r_W}{\\BIG r_B}$, where\n$r_W,r_B\\in\\{-1,0,1\\}$ are white's results with white and with black to move.",
"for white, or as worth $0$, scoring the end position $\\game{\\BIG r_W}{\\BIG r_B}$ ($r_W,r_B\\in\\{-1,0,1\\}$ are\nwhite's results with white and with black to move; a dead draw is scored $\\star$).",'4 oracle def')
# 5 engines
both('12_engines.tex',"each labeled by its CGT class\n(Table","each labeled by its CGT class in the model\n(Table",'5 engines class label')
both('12_engines.tex',"\\lab{C1}. The classes separate at a small fixed depth\n(Table~\\ref{tab:sf}). At depth~1 the engine reads hot positions, numbers and switches correctly\n$73$--$81\\%$ of the time, but infinitesimals only $30\\%$ ($26\\%$ at depth~2) and nimbers $53\\%$\n\\lab{C1}, consistent with tempo and parity fights, though nimbers and the class \\emph{other} are not clearly\nseparated at this sample size. Both classes reach $100\\%$ by depth~8.",
"\\lab{C1}. A verdict (win, draw or loss at $\\pm150$\\,cp) matches if it agrees with the tablebase.\nAt depth~1 (Table~\\ref{tab:sf}) the engine matches on hot positions, numbers and switches $73$--$81\\%$ of the time,\non infinitesimals $30\\%$ ($8$ of $27$) and on nimbers $53\\%$ \\lab{C1}. Infinitesimals trail the first three classes\n(Fisher's exact test, $p<0.001$ each) but not nimbers or the class \\emph{other}. Infinitesimals and nimbers reach\n$100\\%$ by depth~8.",'5 engines text')
rep(P+'01_intro.tex',"Stockfish at low depth is weakest on infinitesimals \\lab{C1}.","Stockfish at low depth matches the tablebase least often on infinitesimals, significantly less than on hot positions, numbers and switches \\lab{C1}.",1,'5 intro engines bullet')
rep(D+'01_intro.tex',"Stockfish at low depth is weakest on infinitesimals, and on sums","Stockfish at low depth matches the tablebase least often on infinitesimals, significantly less than on hot positions, numbers and switches, and on sums",1,'5 intro engines bullet')
# 6 2,154 and 92.5
both('04_kings.tex',"Of the $2{,}154$ $8\\times8$ positions beside a tr\\'ebuchet whose real results we know, $105$ are","Of the $2{,}154$ $8\\times8$ positions beside a tr\\'ebuchet whose real results we could compute (not a random sample), $105$ are",'6 2154')
rep(P+'14_conclusion.tex',"The model names the real winner in $92.5\\%$ of $2{,}049$ decisive $8\\times8$ positions; on six ranks a","On $2{,}049$ decisive $8\\times8$ positions that we could solve (not a random sample) the model names the real winner in $92.5\\%$; on six ranks a",1,'6 92.5 conclusion')
rep(D+'14_conclusion.tex',"Against real chess the model is right in $92.5\\%$ of the decisive $8\\times8$ positions we can check; on six ranks a","Against real chess the model is right in $92.5\\%$ of the decisive $8\\times8$ positions we could solve (not a random sample); on six ranks a",1,'6 92.5 conclusion')
# 7 threat
both('05_sums.tex',"\\emph{threat} for a side if a position reachable from it gives that side a passed pawn.","\\emph{threat} for a side if play on its own files can reach a position, with no passed pawn earlier, that gives that side a passed pawn (a race gives both sides one).",'7 threat')
# 8
rep(P+'05_sums.tex',"without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}).","without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}), and in our model \\lab{P} (the position is in the repository).",1,'8 E in our model')
rep(D+'05_sums.tex',"without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}).","without (E) the decomposition already fails in the pure pawn game (Proposition~\\ref{prop:condE}), and in our model \\lab{P} (Section~S12).",1,'8 E in our model')
both('05_sums.tex',"on $\\cyl{8}$ with en passant off, $X=$","on $\\cyl{8}$ with en passant off and the count rule, $X=$",'8 count rule')
both('01_intro.tex',"however draws are treated;","however draws are treated \\lab{C1};",'8 C1 on real bullet')
both('04_kings.tex',"(queen promotions only, at most two). Of these","(queen promotions only, at most two queens at a time). Of these",'8 two queens')
both('02_rules.tex',"with $n$ files and eight ranks.","with $n$ files and, unless we say otherwise, eight ranks.",'8 eight ranks')
both('13_verify.tex',"$15$ reference games $X$: all\n$4{,}967{,}550$ outcomes of $G+X$ match","$15$ reference games $R$: all\n$4{,}967{,}550$ outcomes of $G+R$ match",'8 R')
both('08_star2.tex',"two programs check $n<17$ \\lab{C2}","two programs check $n\\le61$ \\lab{C2}",'8 n<=61')
# 9 J4
both('09_real.tex',"beside T, has $12$, with only file f free of pawns between them. Their oracle","beside T, has $12$; no file between its pawns and T is free of pawns, so Theorem~\\ref{thm:validity} does not apply. Their oracle",'9 five-file')
# 10 bib
rep(P+'../refs.bib',"  organization = {{XBoard} variant rules},\n","  organization = {{XBoard} variant rules},\n  year         = {n.d.},\n",1,'10 Muller')
rep(P+'../refs.bib',"howpublished = {Undergraduate course paper (Math 191)},","howpublished = {Undergraduate course paper (Math 191), Stanford Univ., Stanford, CA, USA},",1,'10 WuYuLandry')
import json
json.dump(log,open(R+'delegate/out/W3_long_port/edits.json','w'),indent=1)
print(len(log),'edits')
