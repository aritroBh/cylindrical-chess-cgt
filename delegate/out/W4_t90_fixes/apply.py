import sys
log=[]
def rep(path, old, new, n=1):
    s=open(path,encoding='utf-8').read()
    c=s.count(old)
    assert c==n, (path, old[:60], c)
    s=s.replace(old,new)
    open(path,'w',encoding='utf-8').write(s)
    log.append((path,old,new))
P='research/ring_family_proof/proof.tex'
# finding 3
rep(P,"On a pattern file, each neighbouring pattern file holds a single enemy pawn two ranks\nfurther on in the direction of the file's own pawn.",
"An interval of pattern files of one wall means a consecutive subarc of that wall, with the prescribed alternation along every edge of the interval. Each neighbouring pawn within the subarc is an enemy two ranks ahead in the direction of the first pawn.")
rep(P,"such that files $c,c+1$ are pattern files of one wall and the flagged pawn","such that files $c,c+1$ are a consecutive pair of pattern files of one wall (in the above sense) and the flagged pawn")
# finding 5
rep(P,"so the reply does not win for $Y$;","so the reply does not reach a terminal position won by $Y$;")
rep(P,"By (V),\n$\\nu$ wins for $Y$ iff $\\hat\\nu$ does.","By (V),\n$\\nu$ reaches a terminal position won by $Y$ if and only if $\\hat\\nu$ does.")
# finding 7
rep(P,"For every $n\\ge5$ and every heap $0\\le h<256$, the whole-board position $G_n+\\nim h$ is a P-position if $h=2$ and an N-position\notherwise. So $G_n$ and $\\nim2$ have the same outcome in every sum with a nim-heap; in this sense $G_n=\\nim2$.",
"For every $n\\ge5$ and every integer $h\\ge0$, the whole-board position $G_n+\\nim h$ is a P-position if $h=2$ and an N-position\notherwise. In particular the outcomes agree with those of $\\nim2+\\nim h$ throughout $0\\le h<256$.")
rep(P,"The theorem gives the outcome of $G_n+\\nim h$ for every heap; the proof uses no bound on $h$. Moreover, replace the child","For the corresponding equality in ordinary normal-play CGT, use the following representation. Replace the child")
# finding 8
i=open(P,encoding='utf-8').read()
a=i.index("Its reduced games have 662 nodes"); b=i.index("This transfer has not been written out in full.")+len("This transfer has not been written out in full.")
old=i[a:b]
new=("At the flag-free even base $F_{18}$ the reduced graph has 662 nodes and zone $\\{n-7,\\dots,n-3\\}$; at the flag-free odd base $F_{19}$ it has 3568 nodes and zone $\\{0,1,n-6,\\dots,n-2\\}$. Both give P at heap 2. The cuts 4 and 6 use the respective unchanged prefix intervals $[0,9]$ and $[2,11]$. Insertion extends that prefix by one period and carries each zone to the next. The preceding induction therefore gives these node counts from the respective bases onward. The two unreduced searches also give NNPN at 5 and at every width from 7 through 61, covering all defined smaller cases.")
rep(P,old,new)
# finding 9
rep(P,"The P-outcome at heap 2 was\nobtained by solving this graph (\\texttt{rg.c}, \\texttt{eng.py}), by the canonical value $\\nim2$ of the \\texttt{cylcgt}-built reduced game\nin \\texttt{cylcgt}'s CGT arithmetic, and, without reduction, by C2 at $n_0$.",
"At both bases, \\texttt{graph.py} solves the graph emitted by \\texttt{rg.c reduce}, and \\texttt{verify/red.py} independently builds and solves the graph using \\texttt{verify/eng.py} for the pawn rules. Each gives P at heap 2. The canonical computation in \\texttt{reduced\\_value.py} gives $\\nim2$ for the \\texttt{cylcgt}-built reduced game, and the unreduced searches of C2 also give P at both bases.")
# finding 10
rep(P,"$h=0,1,2,3$, for each side moving first.","$h=0,1,2,3$, where N means either starter wins and P means either starter loses.")
rep(P,"The proof uses only the widths $n<n_0$.","The theorem uses C2 to cover the widths below the respective bases; C1 supplies both induction bases.")
# finding 13
rep(P,"and a tie goes to the side that did not make the last move.","and a tie goes to the opponent of the player who made the terminal pawn move. Here $[A]$ is 1 if $A$ holds and 0 otherwise.")
rep(P,"In the \\emph{whole-board game} $G+\\nim h$","Write $\\nim h$ for the nim-heap of integer size $h\\ge0$; a heap move replaces $h$ by any smaller nonnegative integer.\nIn the \\emph{whole-board game} $G+\\nim h$")
rep(P,"\\begin{theorem}\n","In a P-position either starter loses; in an N-position either starter wins.\n\n\\begin{theorem}\n")
rep(P,"protecting a pawn of the player not to move","marking an e.p.-capturable pawn of the player not to move")
rep(P,"the old flag,\nif any, protected an enemy pawn","the old flag,\nif any, marked an e.p.-capturable enemy pawn")
rep(P,"or a flag protecting it lapsed","or a flag marking it lapsed")
rep(P,"protected $q$, which is gone","marked $q$, which is gone")
rep(P,"protects the pawn of $X$ that just moved","marks the e.p.-capturable pawn of $X$ that just moved")
rep(P,"(b) Choose $s\\in","(b) Write $X=Z$ and let $Y$ be the other side. Choose $s\\in")
rep(P,"So every old pawn has the same three files and\nthe same flag status: the same moves and the same status.","So every old pawn has the same three-file contents and\ne.p. eligibility, hence the same legal move directions and passed status.")
rep(P,"flag status; for the same last mover $q$ and $\\ins_c(q)$ are both non-terminal, or both terminal with the same winner.\n(C)","flag status; for the same last mover $q$ and $\\ins_c(q)$ are both non-terminal, or both terminal with the same winner.\nWrite $q\\nu$ for the child of $q$ after $\\nu$ and $\\hat\\nu$ for the corresponding move by the image pawn.\n(C)")
rep(P,"A far reply $\\nu$ starts on a file $\\le c-2$","A far reply $\\nu$ starts on a file, in old-board coordinates, $\\le c-2$")
rep(P,"in $G_n+\\nim2$ every option loses,","in $G_n+\\nim2$ every move by either starter hands the opponent a win,")
rep(P,"\\paragraph{What is and is not proved.}","\\paragraph{Scope and ordinary game value.}")
rep(P,"one of the zone states listed in the code\nrepository.","one of the base zone states listed in \\texttt{zone\\_states\\_odd.txt} and \\texttt{zone\\_states\\_even.txt}, in the displayed cyclic order.")
rep(P,"$Z_n$ holds files $0,1,2$ and the wall pawns","At the root the zone $Z_n$ contains files $0,1,2$ and the wall pawns")
rep(P,"and\non 3). In every node","and\non 3). Pawns in the zone may move on a K-path. In every node")
rep(P,"the move is L). It shows","the move is L). An advance classified L is resolved before a poisoning reply. It shows")
rep(P,"Example for the side: on eleven","Why the side of capture matters: on eleven")
rep(P,"a decisive passer in one\ncomponent can be cancelled by a $-256$ option in another.","a resolved White win contributes $+256$ in a disjunctive sum; a resolved Black win in a second component contributes $-256$. Their sum is zero.")

N='dist/tog/supp_src/'
# Note 1
f=N+'s15_note1.md'
rep(f,"**V (view lemma).** Let $q$ be any position on $C_n$.","**V (view lemma).** For the S13 insertion suppose that $0\\le c\\le n-2$, that $c,c+1$ form a consecutive pattern pair of one wall and that neither carries the flagged pawn. The occupancy assertion (V1) also holds for the unrestricted file-copy operation.")
rep(f,"nothing else changes). (V2)","nothing else changes). Since the victim is off the cut pair, the image of each prospective e.p. capturer remains beside its victim. (V2)")
rep(f,"(resp. $j-3..j+3$)","(resp. one of $j-1..j+3$ and $j-3..j+1$)")
rep(f,"(and under any rule that is a function of the passed pawns and of who moved)","(and under any race rule invariant under this file embedding and determined by preserved data, including the front-pawn information and last mover needed for count)")
# S14
f=N+'s14_ringn.md'
s=open(f,encoding='utf-8').read()
old=[l for l in s.split('\n') if l.startswith("Lemma 1: a side wins $G+\\star h$ moving first iff it wins the reduced game moving first. Lemma 2: let $p$ have no passer")]
assert len(old)==1
rep(f,old[0],"Use Lemmas 1–3 as stated in Section S13. Lemma 1 starts at a non-terminal board. The triple and the alternative five-file window of Lemma 2 must be consecutive in one wall, with the flag conditions of parts (a) and (b). In Lemma 3 the parent is non-terminal and flag-free, $4\\le c\\le n-6$, and $c-4,\\dots,c+5$ is a consecutive pattern interval of one wall. For each side the K-child sets correspond and the T-existence indicators agree.")
# Note 2
f=N+'s15_note2.md'
rep(f,"Hence T-flags and K-children correspond under insertion. No second or \"symmetric\" arc is used.","Hence T-flags and K-children correspond under insertion. No second or \"symmetric\" arc is used. Here $4\\le 9\\le n-6$ for $n\\ge22$ and the interval lies in the single periodic Q wall.")
rep(f,"compare their shortest promotion distances,","compare their shortest promotion distances (of the front passed pawns eligible under the count rule of Section S13),")
rep(f,"the adjacent opposite-colour wall pawn captures","the adjacent enemy on the side extending two further pattern files captures")
# Note 3
f=N+'s15_note3.md'
s=open(f,encoding='utf-8').read()
old=[l for l in s.split('\n') if l.startswith("Lemma 1: a side wins $G+\\star h$ moving first iff it wins the reduced game moving first. Lemma 2: for a wall pawn")]
assert len(old)==1
rep(f,old[0],"Use Lemmas 1–3 in the form stated in section 2 of Note 1 of Section S15. In Lemma 2 let $p$ be non-terminal and let any e.p. flag mark an opponent's pawn; part (b) further requires $p$ to be flag-free. Each stated window is a consecutive pattern interval of one wall. The Lemma 3 cut is $c=6$, with $4\\le c\\le n-6$ throughout the induction.")
rep(f,"neither end enters the lemmas","no central origin is a wall endpoint; a window may use the first wall file as a neighbour")
rep(f,"Zone and pattern files. By C1, in every node","Zone and pattern files. At the base by C1, and at the induction step by the assumed invariant, in every node")
rep(f,"so any rule that depends on the passed pawns and on who moved gives the same class","so any race rule invariant under this file embedding and determined by preserved data, including the front-pawn information and last mover needed for count, gives the same class")
rep(f,"(Lemma 3 fails only at $c=11$)","(the tested correspondence fails at this control cut only at $c=11$)")
# Note 4
f=N+'s15_note4.md'
rep(f,"For $j\\le c+2$ the window $j-1..j+3$, and for $j\\ge c-1$ the window $j-3..j+1$, lies in the arc, which consists of pattern files in every node ($I_n$, H6).","On the source central range use the right window for $j\\le c+2$ and the left window otherwise. On the image central range the right window fits through $j=c+4$, and the left window fits thereafter. Each chosen window lies in the same alternating wall.")
rep(f,"their hand proofs are those of Section S13 and 2b,","their hand proofs are those of Section S13 (in particular step (iii) of Lemma 3 in Section S13) and 2b,")
print(len(log),"edits ok")
