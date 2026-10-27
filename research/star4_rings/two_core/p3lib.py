# Phase 3 helpers: primitive-core search (width <= 6), single-core rings = block + alternating W2/B4 wall.
import itertools, random, json, sys, os
from collections import Counter
from lib import *

WR = [2, 3, 4, 5, 6]; BR = [3, 4, 5, 6, 7]
def single_tokens():
    out = []
    for w in [0] + WR:
        for b in [0] + BR:
            if w == 0 and b == 0: continue
            out.append(make_token({w} if w else set(), {b} if b else set()))
    return out
V35 = single_tokens()
def dbl_tokens():
    out = set()
    for ws in itertools.chain.from_iterable(itertools.combinations(WR, k) for k in (0, 1, 2)):
        for bs in itertools.chain.from_iterable(itertools.combinations(BR, k) for k in (0, 1, 2)):
            if not ws and not bs: continue
            if len(ws) < 2 and len(bs) < 2: continue
            out.add(make_token(set(ws), set(bs)))
    return sorted(out)
VDBL = dbl_tokens()

TYPES = (('W', 4), ('B', 4), ('W', 5), ('B', 5))   # first-pass wall types: (first token, length)
CONFIRM = {('W', 4): ('W', 6), ('B', 4): ('B', 6), ('W', 5): ('W', 7), ('B', 5): ('B', 7)}

class Log:
    """append-only log of evaluated single-core rings that are 'interesting'"""
    def __init__(self, name):
        self.f = open(name, "a"); self.hist = Counter(); self.seen = set(); self.n = 0
    def rec(self, tag, blk, f, L, sig):
        self.n += 1
        v = nimber(sig)
        key = v if isinstance(v, int) else ("N+" if v == 'N+' else "other")
        self.hist[key] += 1
        interesting = (isinstance(v, int) and v >= 2) or (sig[:4] == 'NNNN' and sig != 'NNNNNNNN') or sig.startswith('NNNP')
        if interesting:
            k = (tag, S(blk), f, L)
            self.f.write(f"{tag}\t{S(blk)}\t{f}\t{L}\t{sig}\n"); self.f.flush()

def probe(ev, lg, tag, blk, types=TYPES):
    """evaluate blk closed with each wall type; returns {(f,L): sig}"""
    res = {}
    for (f, L) in types:
        full = blk + wall(L, f)
        if not legal_start(full): continue
        sig = ev.sig(full)
        res[(f, L)] = sig
        lg.rec(tag, blk, f, L, sig)
    return res

def is_star4_pattern(sig):
    return sig[:5] == 'NNNNP'
