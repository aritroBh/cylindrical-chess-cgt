#!/usr/bin/env python3
"""K15 r3: king states of the shuttle closure of a group (BFS over king moves that kp_p --pmodel values D in the empty context), both sides to move.
usage: mkstates.py BOARD 'root' ... > states.in   (uses fin2/conf2.states_of with the r3 build of kpp)"""
import sys, os
FIN2 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'fin2')
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FIN2)
import conf2 as C
C.KPP = os.path.join(R3, 'bin', 'kpp')
board = sys.argv[1]; W = int(board.split(':')[1].split('x')[0])
for root in sys.argv[2:]:
    toks = tuple(sorted([t for t in root.split() if t not in ('w', 'b', '-')], key=lambda t: ('KkPp'.index(t[0]), t)))
    for st in C.states_of(board, W, toks):
        pass
    sts = C.states_of(board, W, toks)
    pawns = [t for t in toks if t[0] in 'Pp']
    for (K, k) in sts:
        for stm in 'wb':
            print(' '.join([K, k] + pawns + [stm, '-']))
