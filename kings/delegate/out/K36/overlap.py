"""n-gram overlap of a blind PROOF.md with the LOOPY section it re-derives (LOOPY at commit 774036f).
Run from the repo root: python3 kings/delegate/out/K33/overlap.py <PROOF.md> <start marker> <end marker>
Tokens: lower-case runs of letters; share of the proof's n-grams that also occur in the section."""
import re, subprocess, sys
src = subprocess.run(['git', 'show', '774036f:kings/theory/LOOPY.md'], capture_output=True, text=True).stdout
a0 = src.index(sys.argv[2]); a1 = src.index(sys.argv[3], a0)
sec, rep = src[a0:a1].lower(), open(sys.argv[1]).read().lower()
tok = lambda s: re.findall(r"[a-zσ̄′]+", s)
a, b = tok(sec), tok(rep)
for n in (5, 8):
    A = set(tuple(a[i:i + n]) for i in range(len(a) - n + 1))
    B = [tuple(b[i:i + n]) for i in range(len(b) - n + 1)]
    k = sum(g in A for g in B)
    print(f'{n}-grams: {k} of {len(B)} ({k / len(B):.2%})')
