# Applies referee fixes F1-F5 (VERIFY.md) to EDITS.md. Each OLD string must occur exactly once.
import sys
p = sys.argv[1]
s = open(p).read()
R = []
R.append(("| P3.12 | For S ∈ {on, off, dud} the BIG/CGT translation of K ⊞ S is right exactly in the tempo regime (neither side forces an event against passes), and wrong on the forced positions of the side the reservoir favours. In general it can fail even in the tempo regime (3-node stopper, 2-node K) | PROVED; the last claim COMPUTED |",
 "| P3.12 | For S ∈ {on, off, dud} the BIG/CGT translation of K ⊞ S is right exactly outside P_R (on), outside P_L (off), outside P_L ∪ P_R (dud): it is wrong exactly on the forced positions of the side the reservoir does not favour (of both sides for dud, where \"right\" is exactly the tempo regime). In general it can fail even in the tempo regime (3-node stopper, 2-node K) | PROVED; the last claim COMPUTED (and hand-checked) |"))
R.append(("So for these three the translation is right in the tempo regime, and wrong on the forced positions of the side that the reservoir favours; Theorem 3.4, not Theorem 1.11, is the\nsum theorem for them.",
 "So the translation is right exactly outside P_R for `on`, outside P_L for `off` and in the tempo regime T for `dud` (wrong on the forced positions of the side that the reservoir does not favour); Theorem 3.4, not Theorem 1.11, is the\nsum theorem for them."))
R.append(("- (c) *Necessity for one rest component.* If the rest of an event is a single component G with a reserve ∞ (e.g. `off` beside a ⊕ event),\n  dominance fails for every B: it needs Left to win B + G^B second, i.e. λ_B(G) ≤ B.",
 "- (c) *Necessity of the reserve condition for dominance (not for D = CGT), for one rest component.* If the rest of an event is a single component G with a reserve ∞ (e.g. `off` beside a ⊕ event),\n  dominance fails for every B: it needs Left to win B + G^B second, i.e. λ_B(G) ≤ B. Dominance is not the same as D = CGT: `{⊖∣} ⊞ on` is not dominant (λ(on) = 0 but the ⊖ event needs ρ(on) = ∞) yet D = CGT = (W, W), because Right cannot force the ⊖ (Proposition 3.12)."))
R.append(("For a component with an infinite\nreserve opposite a threat no such value exists (Proposition 3.12).",
 "For a component with an infinite\nreserve opposite a threat that the threatening side can force, no such value exists (Proposition 3.12); an unforceable threat (a suicide) leaves the translation right although dominance fails (`{⊖∣} ⊞ on`, `{∣⊕} ⊞ off`, `{⊖∣} ⊞ dud`, `{∣⊕} ⊞ dud`: D = CGT, COMPUTED, B = 2, 5, 9)."))
R.append(("*Reading (the \"value\" of a loopy component).", "*Reading (the \"value\" of a loopy component)."))  # sanity: must occur once
R.append(("For K short and S a stopper (no draws, Proposition 3.10), S matters only\nin the *tempo regime* T = ¬(P_L ∪ P_R), where W(K ⊞ S) ⊆ ¬P_R and L(K ⊞ S) ⊆ ¬P_L.",
 "For K short and S a stopper (no draws, Proposition 3.10), S matters only\nin the *tempo regime* T = ¬(P_L ∪ P_R): outside T nothing depends on S (the inclusions of Theorem 3.11 hold everywhere; they are the whole content)."))
R.append(("- *An infinite reserve on the opposite side kills every B.* `{⊕∣} ⊞ off`",
 "- *An infinite reserve opposite a forcible threat kills every B.* `{⊕∣} ⊞ off`"))
R.append(("(CONJECTURE C1 refuted).", "(the guess is refuted)."))
R.append(("  although the criterion fails: λ_5 of the second component is exactly B = 5",
 "  although the criterion fails: λ_5 of the second component is exactly B = 5"))  # sanity
R.append(("- What fails: an infinite reserve opposite a threat (on or off against the wrong sign, dud against both) has no integer translation (Proposition 3.12);",
 "- What fails: an infinite reserve opposite a threat that the threatening side can force (on or off against the wrong sign, dud against both) makes the integer translation wrong, for every B, on the forced positions (Proposition 3.12); an unforceable threat (a suicide) does not, although dominance still fails;"))
for old, new in R:
    n = s.count(old)
    if n != 1:
        print("FAIL count", n, "for", old[:70]); sys.exit(1)
    s = s.replace(old, new)
open(p, "w").write(s)
print("ok", len(R))
