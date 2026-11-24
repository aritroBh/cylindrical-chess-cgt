# The even Q family is `*3`

## Model and statement

Use the whole-board pawn game on the eight-rank cylinder `C_n`, with White = Left, Black = Right, normal play, race rule `count`, en passant on, and an en-passant-capturable pawn not passed. A first passer ends the game; if a move gives both sides passed pawns, the smaller promotion distance wins and ties go to the side that did not just move. A decisive terminal position is represented by `+BIG` or `-BIG`, with `BIG = 256`.

Write a file by its pawns, for example `W3B6`. For every even `n >= 8`, define

```text
Q_n = W4 B7 (B4 W2)^((n-8)/2) W3B6 W3 W2B5 B5 W2 B4.
```

This has `n+2` pawns. Files `2..n-7` are the wall: a single `B4` on each even file and a single `W2` on each odd file. A *pattern file* below means a file holding exactly its starting wall pawn and no other pawn.

For even `n>=22`, the start has no passer: `W4` on file 0 and `B7` on file 1 block each other; each wall pawn is blocked by the opposite-color pawn on the neighboring wall file; the core `W3B6, W3, W2B5, B5, W2, B4` is blocked in order by its same-file or adjacent core pawn, with the last `B4` blocked by `W2` on file `n-2`. The start has no e.p. flag. The smaller starts are handled as separate finite bases.

Let `R_n` be the reduced game from the T50 proof: keep moves to a terminal win for the mover as terminal options, keep the nonterminal K-moves, and delete terminal losses and poisoned moves. The reduction lemma in [`ring_n_plus_2_proof/PROOF.md`](../ring_n_plus_2_proof/PROOF.md) says that adding any nim heap of size below 256 gives the same outcome in the full game and in `R_n`.

**Theorem — PROVED, conditional on the finite checks below.** For every even `n >= 8`, `Q_n` is `*3` in the proof's nim-heap sense: for every `h < 256`, `Q_n + *h` has the same outcome as `*3 + *h`. This is a whole-board result under the stated rules; it does not concern the component-sum model.

## Wall and insertion facts

**Wall lemma — PROVED.** The wall in `Q_n` is the E-type alternating wall with its phase shifted: adjacent wall pawns have opposite colors and are two ranks apart. A wall pawn cannot capture; its only moves are `W2->3`, `W2->4` (double step), and `B4->3`. With the five-file pattern window required by the T50 wall lemma, after such a move the mover has no passer. If the opponent already has a passer, the move is a terminal loss; otherwise the neighboring wall pawn can capture the mover's pawn (en passant after `W2->4`), giving the opponent a passed pawn while the changed neighboring pawn remains blocked by the next pattern pawn. Thus every such wall move is L or P. This argument is local and does not depend on which parity starts the wall.

**Insertion lemma — PROVED.** Suppose a nonterminal, e.p.-free node `p` has exact pattern files `c-4..c+5`. Insert copies of files `c+1` and `c`, in that order, immediately after file `c`. Old pawns keep their three-file views; the new pawns have alternating-wall views and are blocked.

In `p`, a pawn on `c-3..c+4` has its three-file and five-file windows inside `c-4..c+5`. By the wall lemma all its moves are L or P, so none is a retained K- or T-move. The same is true in the inserted position for pawns on `c-3..c+6`, using its pattern arc `c-4..c+7`.

Every other old pawn is on `f<=c-4` or `f>=c+5`; its image is on `f<=c-4` or `f>=c+7`. A move of one of these pawns changes files only at most `c-3` or at least `c+4`. It leaves files `c-2..c+3` unchanged, so the child and its inserted image have the same passed pawns, ranks, e.p. protection, and terminal race result. Thus the corresponding move is T, L, or nonterminal on both boards.

For a nonterminal child, classify the opponent's replies as near or far. Near pawns are on `c-1..c+2` in the old child and `c-1..c+4` after insertion; their three-file wall windows remain pattern files. By the wall lemma, a near reply cannot give the replying side a passer. Far replies are on `f<=c-2` or `f>=c+3` in the old child, and `f<=c-2` or `f>=c+5` after insertion. They correspond under insertion and leave files `c,c+1` as pattern files, so their terminal status and winner agree. An en-passant reply to the earlier far double-step is also far because its victim lies on the far file. Therefore an opponent has a winning terminal reply on one board iff it has one on the other: the corresponding move is P on both or neither. These cases establish exact correspondence of T-options and K-children, hence insertion preserves the reduced game.

The L/P deletion argument is the same as T50's: a terminal loss or an immediate winning poison reply cannot be a winning move, while T-options, K-options, and heap moves are retained. Hence the reduced game determines all the required full-board nim-heap outcomes.

## Finite base checks

**COMPUTED-1 — cylcgt reduced-game canonical forms.** `reduced_value.py` evaluated each listed reduced graph with cylcgt's canonical-form arithmetic:

| `n` | Reduced nodes | `R_n` canonical value |
|---:|---:|---:|
| 8 | 1,894 | `*3` |
| 10 | 7,141 | `*3` |
| 12 | 8,556 | `*3` |
| 14 | 8,756 | `*3` |
| 16 | 8,112 | `*3` |
| 18 | 7,968 | `*3` |
| 20 | 7,968 | `*3` |
| 22 | 7,968 | `*3` |

The individual run outputs are in `logs/reduced_value_Q_<n>.txt`.

**CHECKED-2 — outcome signature and graph.** The independent C solver gives `NNNPNNNN` for every `Q_n` in this table, for heap sizes `h=0..7`; the `cylcgt` reduced-graph canonical value predicts the same signature. The cylcgt-based graph builder and the C builder also agree node-for-node and edge-for-edge for every even `n=8..24` (outputs in `logs/reduced_cyl_Q.txt`).

For the induction base `n=22`, the C graph has 7,968 nodes, 21,063 kept K-edges, 17,784 T-options, no e.p. flags, and deviation zone `{0,1,2,3,15,16,17,18,19,21}`. These are **CHECKED-2** by the two graph builders; its reduced-game canonical value `*3` is **COMPUTED-1** by cylcgt arithmetic. The base zone leaves files `5..14` as exact pattern files in every node.

## Induction from `n=22`

Use the fixed cut `c=9`. In `Q_22`, files `5..14` are pattern files. At the cut, file 9 is `W2` and file 10 is `B4`; inserting `B4,W2` after file 9 extends the wall and gives exactly `Q_24`. The same insertion takes each `Q_n` to `Q_{n+2}` for every even `n >= 22`.

Assume the reduced graph `R_n` has no e.p. flags and that each of its nodes agrees with the start outside the zone `{0,1,2,3,n-7,...,n-3,n-1}`. The ten files `5..14` are then exact pattern files. The insertion lemma maps every K-child and every T-option of each node onto the corresponding child or option in `R_{n+2}`. The base zone maps to `{0,1,2,3,n-5,...,n-1,n+1}`, exactly the corresponding zone for `Q_{n+2}`; the inserted nodes therefore remain e.p.-free and the root maps to the new root. Induction on paths from the root gives an isomorphism of reduced games `R_{n+2} = ins_9(R_n)`. Since `R_22` has canonical value `*3`, every `R_n` for even `n >= 22` has canonical value `*3`.

The finite values for `n=8,10,...,20` are listed above, so they complete the smaller cases. By the reduction lemma, the corresponding full-board games have the `*3` nim-heap signature. For `h>7`, the first player can reduce the heap to size 3 and leave the P-position `Q_n+*3`; thus the signature extends through the model's full `h<256` range.

## Direct whole-board checks

**CHECKED-2.** In addition to the reduced-game proof, direct calls to cylcgt's whole-board pawn solver (components disabled, e.p.-aware passed test) returned `*3` for `Q_8` and `Q_10`. The C whole-board solver returned `NNNPNNNN` for each. These direct checks are recorded in `logs/whole_cyl_Q_8.txt` and `logs/whole_cyl_Q_10.txt`; larger base cases use the proved reduction plus the reduced-game canonical forms above.
