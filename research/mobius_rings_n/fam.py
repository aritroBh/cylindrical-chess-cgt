#!/usr/bin/env python3
"""Family search. usage: fam.py stage ... ; uses bin/mob2_32 (solve) in batch."""
import subprocess, sys, itertools, json
BIN = 'bin/mob2_32'
def solve(rings, binp=BIN, batch=50, tmo=15):
    """batches; a batch/ring exceeding tmo seconds is bisected; a single ring over the limit gives 'TIMEOUT'."""
    out = []
    for i in range(0, len(rings), batch):
        out += _solve(rings[i:i+batch], binp, tmo)
    return out
def _solve(rs, binp, tmo):
    try:
        p = subprocess.run(['nice','-n','15',binp,'solve'], input='\n'.join(rs)+'\n', capture_output=True, text=True, timeout=tmo)
    except subprocess.TimeoutExpired:
        if len(rs) == 1: return ['TIMEOUT']
        h = len(rs)//2
        return _solve(rs[:h], binp, tmo) + _solve(rs[h:], binp, tmo)
    o = p.stdout.split('\n')[:len(rs)]
    assert len(o) == len(rs), (len(o), len(rs), p.stderr[-300:])
    return o
SINGLES = [f'W{r}' for r in range(2,7)] + [f'B{r}' for r in range(3,8)]
def ins(tokens, cut, block, m):
    return tokens[:cut] + block*m + tokens[cut:]
