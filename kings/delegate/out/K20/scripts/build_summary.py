#!/usr/bin/env python3
"""Assemble summary.json (K20): definition, tables, verification counts, full-board comparisons, labels, reproduce commands."""
import json, os, re, glob, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(__file__))
from report_text_def import DEFINITION
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = '/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python'


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def ext_totals(path):
    out = collections.OrderedDict(); pairs = [0, 0]
    for l in open(path):
        if 'EXT' in l:
            for part in l.split(':', 1)[1].split(';'):
                m = re.match(r'\s*(\S+) agree=(\d+) disagree=(\d+)', part)
                if m:
                    a = out.setdefault(m.group(1), [0, 0]); a[0] += int(m.group(2)); a[1] += int(m.group(3))
        m = re.search(r'PAIRS checked (\d+) mismatches (\d+)', l)
        if m: pairs[0] += int(m.group(1)); pairs[1] += int(m.group(2))
    return {'ext_agree_disagree': out, 'pairs_checked': pairs[0], 'pairs_mismatches': pairs[1]}


def check_totals(paths):
    roots = 0; bad = 0
    for p in paths:
        for l in open(p):
            m = re.match(r'config .* compared (\d+) running mismatches (\d+)', l)
            if m:
                pass
            m = re.match(r'TOTAL compared (\d+) mismatches (\d+)', l)
            if m: roots += int(m.group(1)); bad += int(m.group(2))
    return {'roots_compared': roots, 'mismatches': bad, 'outcomes_compared': roots * 34 * 2}


classes = json.load(open(D + '/summary_classes.json'))
res = {'definition': DEFINITION}
res['class_tables'] = classes
res['python_independent_check'] = check_totals([D + '/logs/check1.log', D + '/logs/check2.log', D + '/logs/check3.log'])
res['battery4553'] = {}
for n in ('flat_6x6', 'cyl_6x6', 'cyl_8x6'):
    res['battery4553'][n] = ext_totals(D + '/logs/ext_%s.log' % n)
res['battery4553']['extra_configs'] = ext_totals(D + '/logs/ext_extra.log')
res['alone_vs_P_model'] = {}
for n in ('flat_6x6', 'cyl_6x6', 'cyl_7x6', 'cyl_8x6'):
    res['alone_vs_P_model'][n] = sh('%s %s/scripts/cmp_alone.py %s/logs/alone_%s.pred %s/logs/alone_%s.pmodel' % (PY, D, D, n, D, n))
res['alone_vs_chess_cap1'] = {}
for n in ('flat_6x6', 'cyl_6x6'):
    p = D + '/logs/alone_%s.chess' % n
    if os.path.exists(p) and os.path.getsize(p) > 0:
        res['alone_vs_chess_cap1'][n] = sh('%s %s/scripts/cmp_alone.py %s/logs/alone_%s.pred %s' % (PY, D, D, n, p))
res['full_board_contexts'] = {}
for n in ('full_flat8x6', 'full_far_flat8x6', 'full_far2_flat8x6'):
    res['full_board_contexts'][n] = sh('%s %s/scripts/cmp_full.py %s/logs/%s.pred %s/logs/%s.pmodel' % (PY, D, D, n, D, n))

res['narrative'] = {
 'note': 'REPORT.md was not written: the environment forbids report .md files for subagents. This JSON carries the report text; EDITS.md is the proposed LOOPY change.',
 'values_that_occur': 'Battery sense (B34), free boards and boxes: dud (majority: both kings shuffle), on and off (one king frozen), 0 (mutual zugzwang with free kings, e.g. cyl:6x6 Kb3 kf2 Pa2 pa3), * (two pairs on cylinders: faithful cases cyl:7x6 Ke2 kf4 Pa2 pa3 Pc3 pc4 and cyl:8x6 Kc2 kb4 Pa2 pa3 Pd3 pd4; the adjacent-file cases of cyl:6x6 are not faithful; also in one-file boxes, where the kings only move along the pawn file), tis and tisn, {on|off}, the switches {1|0} and {0|-1} (flat boards, pairs a2/a3 + c4/c5 and mirror), and the finite tempi +1 and -1. Never named: +-2, +-3, +-1/2, up, down, up*, down*, *2, over, under, {2|0}, {0|-2}. Decisive (named {+|}, {|-}, {+|-}, {+|0}, {0|-}, {+|on}, {off|-}): a forced decisive event exists in some context. Loopy, not classified: 40 to 54 percent of all roots.',
 'finite_tempo': 'flat:6x6 (also 7x6, 8x6) Kc3 ka4 Pa2 pa3 Pc4 pc5 = +1; Ka3 kc4 Pa4 pa5 Pc2 pc3 = -1; Kd3 ka4 Pa2 pa3 Pc4 pc5 = {1|0}; Ka3 kd4 Pa4 pa5 Pc2 pc3 = {0|-1}. Faithful configuration, F_Z = {a,b,c}, both kings on F_Z for the +-1 roots. cyl:6x6 Kd3 kd1 Pa2 pa3 = +1 (kings on the file antipodal to the pawns). Even-width cylinders (6, 8, 10): every single blocked pair has +1 and -1 roots (7, 11, 13 roots for the three ranks together); odd width (5, 7, 9): none.',
 'region_dependence': 'flat Kc3 ka4 Pa2 pa3 Pc4 pc5: box(0) = files a-c: value 0; box(1) = a-d: tis; box(2) = a-e: +1; free: +1. Kd3 ka4 ...: box(1) unclassified, box(2) and free {1|0}.',
 'short_games': 'Short roots occur only in one-file boxes (box(0)): the zero game (both kings stuck on the pawn file), {+|} and {|-}. No canonical form beyond 0, +B, -B was needed. Free boards: no short root.',
 'bridge_D_to_P': 'The D-model decisive event (a capture that leaves one passer) is not always a P-win. alone_vs_P_model gives the counts: on cyl:6x6 all 256 positions of the +-1 roots agree with kp_p --pmodel; on cyl:8x6 171 of 198 agree (the passer is caught by the other king in the others); the bare switch roots {1|0}, {0|-1} each fail in one of their two sides to move. Chess (kpsolve cap 1): cyl:6x6 254 of 256 +-1 positions agree exactly, 2 have undecided bounds.',
 'full_board_contexts': 'kp_p --pmodel, flat:8x6, group Kc3 ka4 Pa2 pa3 Pc4 pc5 (and 3 relatives) beside H0, Hp1, Hm1, H*, H*2 on file g: 46 of 48 match o(value(G) + value(H)); all 24 positions for +1 and -1 match; the misses are the bare switch roots. Contexts on file e: 39 of 72. Contexts on files f and h: 31 of 56. Misses are draws where the prediction is a win, consistent with the region dependence (context pawns take squares of the buffer and the next file away from the kings).',
 'limits': 'Battery equality is not equality in all sums (open question 4). on and off names are not exact for up to 1 percent of the roots they name on B4553 (40 of 3883 on cyl:6x6). B4553 was run in full on flat:6x6, cyl:6x6, cyl:8x6 and on selected configurations of cyl:7x6, flat:7x6, flat:8x6 only (the full flat:8x6 run was stopped early to free the shared lock; its partial log is kept as ext_flat_8x6.partial.log). The Python re-implementation compared 57,324 roots on 16 configurations, not all. Kings in the local game are free outside F_Z in the free runs; contexts that take away room change the value.',
}
res['reproduce'] = [
 'cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20; c++ -O2 -std=c++17 -o kg scripts/kg.cpp   # needs nothing else',
 './kg --board flat:6x6 --maxpairs 2 --only "a2,c4" --ext --pairs --maxex 2      # +1, {1|0}: classes, B4553 test, pair test',
 './kg --board cyl:8x6 --maxpairs 2 --maxex 3 --roots logs/roots_cyl_8x6.txt > logs/cyl_8x6_free.log   # one board, free; add --margin 0|1|2 for boxes',
 'PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python scripts/check_kg.py flat:6x6 logs/roots_flat_6x6.txt "a2 c4"   # independent re-implementation',
 'cc -O2 -o kp_p /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread; PYTHONPATH=... python scripts/gen_full.py flat:8x6 logs/full_far_flat8x6 far; ./kp_p --board flat:8x6 --pmodel --cap 1 < logs/full_far_flat8x6.pos > logs/full_far_flat8x6.pmodel; python scripts/cmp_full.py logs/full_far_flat8x6.pred logs/full_far_flat8x6.pmodel',
 'python scripts/gen_alone.py cyl:6x6 "+1;-1;0;tis;tisn" logs/alone_cyl_6x6; ./kp_p --board cyl:6x6 --pmodel --cap 1 < logs/alone_cyl_6x6.pos > logs/alone_cyl_6x6.pmodel; python scripts/cmp_alone.py logs/alone_cyl_6x6.pred logs/alone_cyl_6x6.pmodel',
]

json.dump(res, open(D + '/summary.json', 'w'), indent=1)
print('written', D + '/summary.json', os.path.getsize(D + '/summary.json'))
