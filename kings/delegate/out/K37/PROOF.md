# Blind proof of Lemma 2.9

## Conventions and strategy

The blind argument uses the local game of Definition 2.6. Call the side to move `s`, and its opponent `s̄`. The `s̄` pawns all start on file `f`; `s`'s king is on `f` and ahead of every one of them. An `s̄` pawn is *attacked* when an `s` pawn occupies one of its two diagonally forward squares, as in (B1). Pawns attack each other symmetrically here.

Strategy for `s`: if an `s̄` pawn is attacked, capture one such pawn with an attacking `s` pawn; otherwise pass. Keep `s`'s king fixed. An en-passant right carried at the root was created by `s̄`; a pass clears it. `s` never double-steps, so `s̄` can never acquire a new en-passant right from `s`.

## Invariant and induction

At every turn of `s̄`, maintain:

1. Every `s̄` pawn remains on `f` and below `s`'s king.
2. No `s̄` pawn is attacked by an `s` pawn.

At the root, condition 1 holds by hypothesis. Before `s`'s first move, at most one `s̄` pawn is attacked by (B1). If one is attacked, `s` captures it; otherwise `s` passes. Thus both conditions hold before `s̄`'s first move.

Suppose they hold before a later `s̄` move. A king move changes no pawn position. It may capture an `s` pawn, which can only remove attacks. A pawn push stays on `f`: the front pawn cannot push through the king's occupied square, and the other pawns cannot pass the pawn in front of them. It therefore stays below the king and cannot promote. A pawn capture off `f` would have to capture an `s` pawn on a diagonally forward square; that square is precisely an attack on the moving `s̄` pawn, contrary to condition 2. En passant is also impossible: `s` has never double-stepped, and any root right is cleared by the first pass or expired by an intervening move. So all `s̄` pawns stay on `f` and below the king.

Only a pawn that moved can acquire a new attack after `s̄`'s move. By (B1), at most one `s̄` pawn is then attacked. On `s`'s turn, if there is one, capture it with an attacking pawn. This capture is legal: the fixed king on `f` cannot be checked by an `s̄` pawn still on `f` (those pawns attack the adjacent files), and the confined `s̄` king cannot attack it without being adjacent, which is illegal. There are no other pieces that can check or pin. The capturing pawn lands on `f`; it attacks only squares on the two adjacent files, so it attacks no remaining `s̄` pawn on `f`. No other attack relation changes. The removed pawn was the only potentially attacked one, so condition 2 is restored. Condition 1 is preserved because the king did not move and only a pawn below it was removed. If no `s̄` pawn is attacked, passing preserves both conditions and clears any root en-passant right.

The board starts in the required game class and the argument never relies on a move of `s̄`'s king leaving `F_Z`; that king may approach, retreat, or capture an `s` pawn, but cannot check the fixed king from a legal position. Thus `s` is never in check on its turn and never mated. Every `s̄` pawn remains below the fixed king and on `f`, with its forward path blocked; none can promote. A win in `L_T` for any finite `T` would require a promotion by `s̄` or mate of `s`, both excluded. The queen-capture clause is immaterial, so the conclusion holds for both (L1) and (L1_P).

## Why (B1) applies in the stated cases

If `s` has no pawn on `f ± 1`, no `s̄` pawn on `f` is attacked. If `s̄` has exactly one pawn, there can be at most one attacked `s̄` pawn. On a four-rank board, count ranks from `s̄`'s side. Its pawns stand on rank 2 or higher. For two of them on `f` to be attacked by one `s` pawn, that pawn would have to stand on rank 4, the last rank for `s`, which pawns cannot occupy. Hence (B1) is automatic when `H=4`. For `H≥5` that geometry no longer excludes two attacked pawns, so the proof uses (B1) as a genuine hypothesis. The condition is sufficient, not necessary: it may fail in positions where the kings still let `s` hold the blockade, but this proof makes no such broader claim.

## Validation status

The requested independent local-game solver and exhaustive small-board sweep were not completed in this run. No brute-force counts or counterexamples are claimed. The proof above is a manual derivation; it does not rely on a computation. The proof's two key dependencies are the symmetric pawn-attack convention in Definition 2.9 and the absence of pieces other than kings and pawns in `Q_Z`.
