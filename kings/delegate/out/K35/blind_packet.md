# K35 blind packet: definitions and statements only (extracted from kings/theory/LOOPY.md at commit 3fbe9f54)

Proofs and verification notes are omitted on purpose. Do not read LOOPY.md itself until Phase 2.

## Proposition 2.11: setting, notation, hypotheses and statement (frozen model F)

*Setting.* F is the frozen promotion model, `kpsolve --frozen`: a promotion wins at once for the promoter; a legal
king move ends the play at once in favour of the opponent of its maker; a side with no legal move at all (king
moves count as moves) that is not in check draws, and one in check loses; infinite play is a draw. The board is
a cylinder with W files and H ≥ 5 ranks (files mod W). On a flat board the same proof works with the neighbouring
files that exist (not separately written out); a second-round reviewer ran flat 5×6, 6×6, 7×6 and 6×7 (434,429 certified positions with side to move, 0 violations; see the checks).

*Notation.* Fix a legal position y (kings not adjacent, the side not to move not in check) before any promotion, the side s to move, a side β (the beneficiary) and ω, the
other side. For a pawn q of either colour let ρ(q) be its rank counted from β's side: ρ(q) = rank(q) if β is
White, and ρ(q) = H + 1 − rank(q) if β is Black, whatever the colour of q (revised after the K10 second round). β's pawns advance towards larger ρ, ω's towards smaller ρ; "ahead of p" means larger ρ.
β's start rank is ρ = 2 and ω's is ρ = H − 1. For a pawn p of β put d = H − ρ(p) − [ρ(p) = 2] (the number of β
moves p needs to promote; this is cylcgt's `promote_distance`), and
- e = d if s = ω (ω makes e moves before β's promoting push),
- e = d − 1 if s = β.

*The ω-only game G_ω(y; p).* Delete p. Only ω moves, one move after another. β's other pawns stay where they are
and can be captured. Both kings stay and block squares; nobody captures a king. ω's pawns move as in chess:
push, double step from the start rank over an empty square, capture, and the e.p. capture that y offers (only
as the first move, and only if s = ω). μ_ω(y; p) is the least number of moves after which some ω pawn stands on
its last rank (the promoting move included), or ∞. It is a minimum over **all** ω pawns, passers or not,
with captures allowed. An ω king move ends F at once, so it never occurs in G_ω.

*Hypotheses.*
- **(H1) clear path.** p is a pawn of β that is passed at y in cylcgt's e.p.-aware sense (`passed` with
  `PASSED_RESPECTS_EP = True`: no ω pawn on files f − 1, f, f + 1 with ρ > ρ(p), and p cannot be taken en passant at
  y), and every square of p's file ahead of p, the promotion square included, is empty. So p is the front pawn
  of its file, and **no pawn and no king of either colour** stands on the path.
- **(H2) no check.** No pawn of either colour stands on a file adjacent to the file of β's king.
- **(H3) no stalemate.** ω's king has a neighbouring square t that is not adjacent to β's king, such that no
  pawn of either colour stands on the file of t or on a file adjacent to it. "Not adjacent" means king distance ≥ 2.
- **(H4) no interference.** Every pawn of β other than p that stands on a file adjacent to p's file has
  ρ ≤ ρ(p) + 1.
- **(H5) timing.** μ_ω(y; p) ≥ e + 1.

**Statement.** Under (H1)–(H5), β wins F from (y, s) by pushing p at every turn (the double step first if
ρ(p) = 2).

## The P model with real kings

P is chess before the first promotion with real kings: the first promotion wins at once for the promoter; mate wins; stalemate and infinite play are draws (Theorem 1.14, sharp form, setting). A private build: `cc -O2 -o <dir>/kpp kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread`, run with `--pmodel` (input lines like `Ka1 ka6 Pc2 w -`, output `<pos> | A B` from White's view).

## Notation for Theorem 2.11K

q₀, …, q_d are the squares p occupies before its first push and after each push of Π, and n_j = j if s = ω, j − 1 if s = β (the number of ω moves made when p reaches q_j). d(·, ·) between squares is the king distance on the board (cylinder: files wrap). k_ω and k_β are the squares of ω's and β's kings at y.

## Theorem 2.11K (statement only)

  - ***Theorem 2.11K.*** Notation of Proposition 2.11; Π is "β pushes p at every
    turn (the double step first if ρ(p) = 2)". Assume (H1) (path free of pawns and kings), (H4), (H2) (no pawn of either colour on a file adjacent to β's king's file),
    (H5K) μ^K_ω(y; p) ≥ e + 1, where μ^K_ω is μ_ω in G^K_ω, which is G_ω with ω's king allowed one step per move onto a square that is not an ω pawn, not β's king and not adjacent to it,
    capturing β's other pawns (the variant that also forbids squares attacked by a remaining β pawn is covered too), (SQ) d(k_ω, q_j) ≥ n_j + 2 for j = 0, …, d (j = 0 only if s = ω), and
    (NS) in no play of Π is ω stalemated at one of its turns (a search of depth ≤ e over ω's replies); (NS) follows from (H3K): every square x with d(x, k_ω) ≤ e − 1 has a king-neighbour t with
    d(t, k_β) ≥ 2 and no pawn of either colour on the files of t, t − 1, t + 1. Then β wins P from (y, s) by Π.


