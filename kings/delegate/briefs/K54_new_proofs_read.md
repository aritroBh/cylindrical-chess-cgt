# K54: referee read of two proof texts written on 2026-11-23

**Output directory:** `kings/delegate/out/K54/` (exists). Write only there. Do **not** edit any existing file. Do not
run git.

Two proofs in `kings/theory/LOOPY.md` were rewritten on 2026-11-23 after reports from outside the Claude family (your
K52 and the re-read T83). The new texts were written and refereed by models of one vendor. Read them as printed now.

1. **Theorem 1.11(c), the frontier step ("quiet-move" argument).** Find it with
   `grep -n "quiet" kings/theory/LOOPY.md`. Read Definition 1.10 with the new passer-colour threat set τ_P, the
   statement of Theorem 1.11(c) with (HSS), (B), (E) and the passer-free root, and the whole proof. `kings/delegate/out/K52/`
   holds your earlier report and `kings/delegate/out/K52/integrate/` what was done with it. Mark every step of the
   printed proof SOUND, GAP or FALSE. Attack: repeated splits of a component; which (E) covers a right that the sum
   model keeps and the whole board has dropped; why a later freeze by the opponent is credited +B and not −B under each
   of the three race rules; the token count; whether (B) as stated is the bound actually used; whether τ_P and the
   scored τ are used consistently; the alternative under B > N(X). Check the two no-(E) witnesses and the necessity
   paragraph as printed.
2. **Theorem 2.7 (a), Steps 5 and 6, and the "Example (the reply itself can mate)".** Find it with
   `grep -n "plays r and wins, by a" kings/theory/LOOPY.md`. Mark every step SOUND, GAP or FALSE. Is the corrected
   timing ("no later than its T-th move after r; r itself may mate") exactly what the proof gives? Is the claim that
   the stalemate side has no gap right, given that (L3) is stated over real plays? Verify the example and its variant
   (`Ka6 Pb6 Pb7 Pd6 / Kb8 Pa7 Pa3`, Black to move) with your own short script.
3. **Tests.** For 1.11(c): your own script importing `cylcgt` read-only; for passer-free roots with 3 + 3 pawns on
   boards where (E) can fail (5 files, 6–7 ranks; sample if the full set is too large), compare o(S) with the
   whole-board result on roots that satisfy (HSS), (B) and (E), and separately on roots that fail (E) only later (no
   right at the root). The second set decides a question LOOPY leaves OPEN: say what you find.

Write `FINDINGS.md`: a 5-line summary; per step the verdict; each problem with the LOOPY line number, a
counterexample or the missing step, and replacement text; the test counts; your recommended label for each.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Light computation only (minutes, under 1 GB). No file over 50 MB; no installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Delete binaries at the end. The repository is
public: no personal data, relative paths only.
