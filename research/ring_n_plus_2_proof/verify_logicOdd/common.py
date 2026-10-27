"""Shared helpers for the odd-family logic audit (verify_logicOdd).  Engine D = copy of verify_logic/engine.py (written from the rules)."""
import sys, os
sys.setrecursionlimit(1000000)
import engineD
from engineD import *      # noqa

def R_toks(n):
    assert n % 2 == 1 and n >= 9
    return ['W5', 'B7'] + ['W2', 'B4'] * ((n - 9) // 2) + ['W2', 'W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']

def Qo_toks(n):
    assert n % 2 == 1 and n >= 9
    return ['W4', 'B7'] + ['W2', 'B4'] * ((n - 9) // 2) + ['W2', 'W3B6', 'W3', 'W2B5', 'B5', 'W2', 'B4']

TOKS = {'R': R_toks, 'Qo': Qo_toks}

def pat(j):
    """wall pattern of the odd families: W2 on even files, B4 on odd files (files 2..n-7)"""
    return parse_file('W2') if j % 2 == 0 else parse_file('B4')

def cls(pos, ep=None):
    """per side: (has a T-move, frozenset of K-children (pos, ep))"""
    out = {}
    for side in 'WB':
        cl = classify(pos, ep, side)
        out[side] = (any(c == 'T' for c, *_ in cl), frozenset((npos, nep) for c, npos, nep, *_ in cl if c == 'K'))
    return out
