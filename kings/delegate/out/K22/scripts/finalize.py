#!/usr/bin/env python3
"""Merge the narrative result into summary.json (after summarize.py)."""
import json, re
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22/'
S = json.load(open(D + 'summary.json'))
comp = open(D + 'logs/compare_log.txt').read()
strat = open(D + 'logs/strategy_check.txt').read()
S['verdict'] = 'Lemma 2.9 without the hypothesis is FALSE (counterexamples with two attacked s-bar pawns). Repaired lemma under (B1) (at most one s-bar pawn attacked by an s pawn): PROVED.'
S['counterexamples'] = [
 dict(id='E1', board='flat:4x5', Fz='a..d', position='Kd4 kb5 Pb2 Pb3 pc3 pc4 b -', local_T=3, queen_clause_T=3, python_T=3, pmodel_real_kings='W W (all 5 Black moves lose)'),
 dict(id='E2', board='cyl:7x6', Fz='a..c', position='Ka5 kc6 Pc3 Pc4 pb4 pb5 b -', local_T=3, queen_clause_T=3, python_T=3, pmodel_real_kings='W W (all 5 Black moves lose)'),
 dict(id='E3', board='flat:5x6', Fz='a..e', position='Ka5 kc6 Pc3 Pc4 pb4 pb5 b -', local_T=3, python_queen_clause_T=3, pmodel_real_kings='W W'),
 dict(id='E4', board='cyl:7x6', Fz='a..c, f=a', position='Kc5 ka6 Pa3 Pa4 pb4 pb5 b -', local_T=3, python_T=3, pmodel_real_kings='W W (all 5 Black moves lose)'),
 dict(id='control', board='flat:4x5', Fz='a..d', position='Ka1 kb5 Pb2 Pb3 pc3 pc4 b -', local='no White win (python agrees)', pmodel_real_kings='L L (Black wins)')]
S['compare_python_vs_cpp'] = dict(runs=len(re.findall(r'compared', comp)), roots=sum(map(int, re.findall(r'compared (\d+) roots', comp))), white_wins=sum(map(int, re.findall(r'compared \d+ roots, (\d+) White wins', comp))), mismatches=sum(map(int, re.findall(r'mismatches (\d+)', comp))), illegal=sum(map(int, re.findall(r'illegal (\d+)', comp))))
S['strategy_check'] = dict(runs=len(re.findall(r'violations=', strat)) , roots=sum(map(int, re.findall(r': (\d+) roots with', strat))), states=sum(map(int, re.findall(r'(\d+) states, violations', strat))), violations=sum(map(int, re.findall(r'violations=(\d+)', strat))))
S['exhaustive_boundary'] = 'roots: s-bar pawns on one file f (1..WMAX), s pawns on F_Z (0..BMAX), s king on f above the front pawn, s-bar king anywhere legal on F_Z, s to move, e.p. root variants for H>=6; see configs; pawn limits 3+3 (4+4 on flat 3x5 3x6 4x5 4x6 5x5); 4-rank boards have no root with two attacked pawns'
json.dump(S, open(D + 'summary.json', 'w'), indent=1)
print(json.dumps({k: S[k] for k in ('compare_python_vs_cpp', 'strategy_check', 'totals')}))
