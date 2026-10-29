#!/usr/bin/env python3
"""K15 r3: add the r3 facts to K15/summary.json (written by fin2/scripts/assemble.py)."""
import json, os, re
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K15 = os.path.dirname(R3)
s = json.load(open(os.path.join(K15, 'summary.json')))
def rd(p):
    try: return open(p).read()
    except Exception: return ''
s['task'] = 'K15'; s['date'] = '2026-10-29 (tags 2026-10-27)'
s['verdicts'] = {
 'Z_B_regression': 'exact classifier grp labels Z_B dud (plain P, flat 7x6, 4 king states); one-ply tests of the brief label it other; brief filter (cylcgt.passed) rejects it',
 'open_question_2': 'yes: G8a Kb2 kc4 Pa3 Pe2 pa4 pe3 and G8b Kb3 kc5 Pa4 Pe3 pa5 pe4 on cyl:8x6 are exactly two-shuttle in P (CHECKED-2) and in chess at cap 2 (COMPUTED-1), no pawn move, no root passer',
 'conjecture_4_7': 'no over or under group in the searched boundary (COMPUTED-1); second half CONJECTURE, no support; near-over survivor Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4 refuted on context file f',
 'chess_D2_D2m': 'not two-shuttle in chess: 52 of 108 P-losing deviations draw (cap 1, exact)'}
s['r3'] = {'binaries_identical_to_fin2': True,
 'ref3_sample': [l for l in rd(os.path.join(R3, 'logs', 'cmp_ref3.txt')).splitlines()],
 'rerun': [l for l in rd(os.path.join(R3, 'logs', 'rerun.log')).splitlines() if 'exit=' in l],
 'notrun_root_check': rd(os.path.join(R3, 'logs', 'notrun_summary.txt')).strip().splitlines(),
 'chess_cyl7_D2_D2m': rd(os.path.join(R3, 'logs', 'chess_cyl7_summary.txt')).strip().splitlines()[0::3],
 'zstar_contexts': [l for l in rd(os.path.join(R3, 'logs', 'ctxexh_surv_chunked.txt')).splitlines()],
 'xcheck2_passes_reading': 'see logs/xcheck2_r3.txt: 20 configurations, 772188 roots, 0 label mismatches'}
json.dump(s, open(os.path.join(K15, 'summary.json'), 'w'), indent=1)
print('summary.json updated')
