"""n-gram overlap of K13/REPORT.md with LOOPY's sharp-form section (before the K13 edits).
Run from the repo root: python3 kings/delegate/out/K13/overlap.py
Section: lines 549-640 of kings/theory/LOOPY.md at commit 774036f~1 (from the setting of the sharp form to the
end of its 'Reading' paragraphs). Tokens: lower-case runs of letters (incl. σ, ̄, ′); n-grams of the report that also
occur in the section, as a share of all n-grams of the report."""
import re, subprocess
src = subprocess.run(['git', 'show', '774036f~1:kings/theory/LOOPY.md'], capture_output=True, text=True).stdout.split('\n')
sec = ' '.join(src[548:640]).lower()
rep = open('kings/delegate/out/K13/REPORT.md').read().lower()
tok = lambda s: re.findall(r"[a-zσ̄′]+", s)
a, b = tok(sec), tok(rep)
for n in (5, 8):
    A = set(tuple(a[i:i + n]) for i in range(len(a) - n + 1))
    B = [tuple(b[i:i + n]) for i in range(len(b) - n + 1)]
    print(f'{n}-grams: {sum(g in A for g in B)} of {len(B)} report n-grams occur in the section ({sum(g in A for g in B) / len(B):.3%})')
