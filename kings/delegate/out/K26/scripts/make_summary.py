#!/usr/bin/env python3
"""K26 final: write summary.json from the logs (counts only; the prose is in the final report of the task).  Usage: make_summary.py"""
import glob, json, os, re, collections, hashlib, subprocess
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
R = '/Users/aritro/Downloads/Research/Chessendgames'


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


S = {'task': 'K26', 'item': 'LOOPY section 8 item 2 and Conjecture 4.7 (dud groups without a pawn break on the cylinder; over groups), P model',
     'sources_md5': {k: md5(os.path.join(R, v)) for k, v in {
         'kpsolve.c': 'kings/kpsolve.c', 'kp_p.c': 'kings/delegate/out/K7/scripts/draft/kp_p.c',
         'ref3.cpp': 'kings/delegate/out/K23/verify/ref3.cpp', 'ref3m.cpp': 'kings/delegate/out/K23/verify/ref3m.cpp'}.items()}}
# t2 / t1 merged (per-piece convention)
m = json.load(open(os.path.join(LOG, 'merged.json'))) if os.path.exists(os.path.join(LOG, 'merged.json')) else {}
S['merged_runs'] = {k: {kk: vv for kk, vv in v.items() if kk in ('board', 'limits', 'type', 'complete', 'candidates', 'exact_dud', 'min_total_leaks_8roots', 'classes', 'over_pre')} for k, v in m.items()}
a = json.load(open(os.path.join(LOG, 'audit_merged.json')))
S['audit_second_enumerator_second_solver'] = {k: {kk: v[kk] for kk in ('placements', 'hist8_kpp', 'hist8_ref3m', 'roots_compared_full_lists', 'value_mismatches', 'move_list_mismatches', 'complete')} for k, v in a.items()}
ca = json.load(open(os.path.join(LOG, 'confirm_all.json')))
S['confirm_all_ref3m'] = {'groups': ca['groups'], 'roots': ca['roots'], 'failures': len(ca['failures']), 'per_class_board': ca['per_class_board']}
nc = json.load(open(os.path.join(LOG, 'negcontrol', 'confirm_all_negcontrol.json')))
S['negative_control_failures'] = len(nc['failures'])
cf = json.load(open(os.path.join(LOG, 'confirm_final.json')))
S['confirm_final_ref3m_movelists'] = {'groups': len(cf['groups']), 'roots': cf['total_roots'], 'agree': cf['roots_fully_agreeing']}
# over2/over3
o = {}
for f in sorted(glob.glob(os.path.join(LOG, 'over2_*_22.json')) + glob.glob(os.path.join(LOG, 'over3_*.json'))):
    d = json.load(open(f))
    o[os.path.basename(f)] = {k: d.get(k) for k in ('board', 'limits', 'nf', 'shard', 'candidates', 'stageA_survivors', 'stageA_dropped_by_king_freeze_filter', 'stageB_survivors', 'classes', 'seconds')}
    o[os.path.basename(f)]['mutual_groups'] = len(d.get('groups', []))
S['under_over_mutual_searches'] = o
fc = json.load(open(os.path.join(LOG, 'final_ctx.json')))
S['contexts'] = {'sampled_rows': len(fc['sampled']), 'exhaustive': fc['exhaustive']}
S['verdicts'] = {
    'open_question_2_dud_without_pawn_break_on_cylinder': 'YES in P (COMPUTED-1 search, CHECKED-2 roots): Z_B (Pa3 Pb4 pb3 pc4; Kb2/Kc3, ka4/kb5) on cyl:7x6, cyl:8x6 and every 6-rank board tried; Z_C (Pa2 Pc4 pa3 pc5; Kc2/Kc3, ka4/ka5; all pawns blocked, passer-free) on cyl:8x6 and cyl:9x6. Not PROVED by hand on the cylinder. Z_B equals dud_D in all exhaustive contexts of <= 3 pawns tried (2049 + 577 + 2049); Z_C fails in 131 of 2049.',
    'flat_7x7': 'no exact dud in <= 2+2; minimum total leak count 1',
    'exact_over_under_mutual_zugzwang': 'none found: cyl:8x6 3 files 2+2, 3+2, 2+3; cyl:8x6 four files 2+2; cyl:7x6, flat 7x6, flat 8x6 2+2 (COMPUTED-1). Lemma (PROVED): no freeze is a non-capturing king move.',
    'conjecture_4_7': 'first half supported in P within the searched range (no exact over/under with <= 2+2 pawns on 3 files of cyl:8x6, also 3+2, 2+3 and four files); second half (wider groups) not supported and not refuted; loose (one-sided zugzwang) under/over groups exist in numbers (120 on cyl:8x6 3 files 2+2) but are not over_D (Prop 4.6 fails in 6 of 768 premise roots).',
    'exact_on_off': 'exist on every board (4 to 34 per board and range, many passer-free); beside contexts they match Theorem 3.4(b) except 12 roots in 5 of the sampled contexts on the two cylinders.'}
S['housekeeping'] = 'bin/ and bin_r/ deleted at the end; the optional Z_C detail run logs/exh/detail_zc_fg (left over from the previous attempt queue, which I could not stop) finished by itself; its numbers (61 contexts, 40 roots differ) repeat the earlier Z_C sample'
json.dump(S, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
print('summary.json written', os.path.getsize(os.path.join(OUT, 'summary.json')), 'bytes')
