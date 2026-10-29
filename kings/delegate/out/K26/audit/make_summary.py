#!/usr/bin/env python3
"""K26 attempt 5: write summary.json from the FRESH logs (logs/k26f_*, k26c_*, k26f_over3_*, logs/f/*).  Counts only; the prose is FINDINGS.md."""
import glob, json, os, re, collections, hashlib
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(OUT, 'logs')
R = '/Users/aritro/Downloads/Research/Chessendgames'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
S = {'task': 'K26', 'attempt': 5, 'item': 'LOOPY section 8 item 2 and Conjecture 4.7: dud groups without a pawn break on the cylinder; over groups (P model)',
     'sources_md5': {k: md5(os.path.join(R, v)) for k, v in {'kpsolve.c': 'kings/kpsolve.c', 'kp_p.c': 'kings/delegate/out/K7/scripts/draft/kp_p.c',
                     'ref3.cpp': 'kings/delegate/out/K23/verify/ref3.cpp', 'ref3m.cpp': 'kings/delegate/out/K23/verify/ref3m.cpp'}.items()}}
def runs(prefix, typ):
    d = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(LOG, prefix + '_*_summary.json'))):
        nm = os.path.basename(f)[:-len('_summary.json')]
        m = re.match(r'^%s_(flat|cyl)_(\d+x\d+)_(\d)(\d)_(t1|t2)(?:_s(\d+)of(\d+))?$' % prefix, nm)
        if m and m.group(5) == typ:
            d[(m.group(1) + ':' + m.group(2), int(m.group(3)), int(m.group(4)))].append((int(m.group(7) or 1), int(m.group(6) or 0), json.load(open(f)), nm))
    return d
for prefix, tag in (('k26f', 'two_shuttle_per_piece_convention'), ('k26c', 'two_shuttle_promotions_counted_once')):
    out = {}
    for k, lst in sorted(runs(prefix, 't2').items()):
        n = lst[0][0]
        h = collections.Counter()
        for s in lst:
            for a, b in s[2]['stage2_hist_total_leaks_8roots'].items(): h[int(a)] += b
        duds = []
        for s in lst:
            for line in open(os.path.join(LOG, s[3] + '_groups.jsonl')):
                r = json.loads(line)
                if r['total'] == 0: duds.append({'W': r['W'], 'B': r['B'], 'wp': r['wp'], 'bp': r['bp'], 'textbook_passer': bool(r['passW'] or r['passB'])})
        out['%s:%d+%d' % k] = {'placements': sum(s[2]['candidates'] for s in lst), 'shards_done': len(lst), 'shards_total': n, 'complete': sorted(s[1] for s in lst) == list(range(n)),
                               'min_total_leaks': min(s[2]['min_total_leaks_8roots'] for s in lst), 'count_total0': h[0], 'count_total1': h[1], 'count_total2': h[2], 'exact_duds': duds}
    S[tag] = out
out = {}
for k, lst in sorted(runs('k26f', 't1').items()):
    n = lst[0][0]; cl = collections.Counter()
    for s in lst:
        for a, b in s[2]['classes'].items(): cl[a] += b
    out['%s:%d+%d' % k] = {'placements': sum(s[2]['candidates'] for s in lst), 'shards_done': len(lst), 'shards_total': n, 'complete': sorted(s[1] for s in lst) == list(range(n)), 'classes': dict(cl)}
S['one_shuttle_on_off_and_loose_under_over'] = out
o3 = collections.OrderedDict()
for f in sorted(glob.glob(os.path.join(LOG, 'k26f_over3_*.json'))):
    d = json.load(open(f)); k = '%s:%d+%d:files=%d' % (d['board'], d['limits'][0], d['limits'][1], d['nf'])
    a = o3.setdefault(k, collections.Counter()); a['files'] += 1
    for kk in ('candidates', 'stageA_survivors', 'stageB_survivors'): a[kk] += d[kk]
    a['exact_under_over_groups'] += len(d['groups'])
    for kk, vv in d['classes'].items():
        if 'dropped' in kk: a[kk.split(':')[-1] + '_drops'] += vv
S['exact_under_over_mutual_zugzwang_fresh_runs'] = {k: dict(v) for k, v in o3.items()}
S['exact_under_over_mutual_zugzwang_reused'] = 'earlier attempt: logs/over3_cyl_8x6_32.json, over3_cyl_8x6_23.json, over3_cyl_8x6_22_nf4_*.json, over2_{cyl_7x6,cyl_8x6,flat_7x6,flat_8x6}_22.json: 0 exact groups in every file; see FINDINGS.md section 3'
def jl(p):
    return json.load(open(os.path.join(LOG, p))) if os.path.exists(os.path.join(LOG, p)) else None
c = jl('f/confirm/confirm_all.json')
if c: S['confirm_all_ref3m'] = {'groups': c['groups'], 'roots': c['roots'], 'failures': len(c['failures']), 'per_class_board': c['per_class_board']}
c = jl('f/confirm/negcontrol.json')
if c: S['negative_control_failures'] = len(c['failures'])
c = jl('f/confirm/confirm_final.json')
if c: S['confirm_final_20_groups_full_move_lists'] = {'groups': len(c['groups']), 'roots': c['total_roots'], 'roots_kpp_and_ref3m_agree': c['roots_fully_agreeing']}
c = jl('f/final_ctx_fresh.json')
if c:
    S['contexts_fresh'] = {'sampled_rows': len(c['sampled']), 'exhaustive': c['exhaustive']}
# audits
aud = collections.defaultdict(lambda: collections.Counter())
for f in sorted(glob.glob(os.path.join(LOG, 'f', 'audit', 'audit*_s*of8.json'))):
    d = json.load(open(f)); nm = os.path.basename(f)
    key = ('t1' if nm.startswith('audit1_') else 't2') + ':' + d['board']
    a = aud[key]; a['shards'] += 1; a['placements'] += d['placements']
    mm = d.get('full_list_mismatches') or d.get('mismatches') or {}
    a['roots_compared'] += mm.get('roots', 0); a['value_mismatches'] += mm.get('value', 0); a['move_list_mismatches'] += mm.get('moves', 0)
    if key.startswith('t2'):
        for sv in ('kpp', 'ref3m'):
            for t, v in d['stage2_hist_' + sv].items():
                if int(t) <= 2: a['%s_total%s' % (sv, t)] += v
    else:
        for t, v in d['classes'].items(): a[t] += v
S['second_enumerator_second_solver_audit_fresh'] = {k: dict(v) for k, v in aud.items()}
S['named_groups_boards'] = 'audit/named_groups.txt (kpp and ref3m, 8 roots, 32 boards)'
S['not_rerun_fresh'] = ['t2 cyl:7x6 2+3 and flat:7x6 3+2 (colour mirrors)', 't1 3+2 and 2+3 on cyl:8x6 and flat 7x6', 'over3/over2 searches', 'collapsed-promotion searches', 'exhaustive <=3-pawn contexts (reused: ZB 2049+577+2049 contexts 0 differ; ZC 131 of 2049 differ)', 'third enumerator on flat 7x7']
S['verdicts'] = {
 'open_question_2': 'YES in P: exact duds without any pawn break exist on the cylinder: Z_B (and mirror) on cyl:7x6 and cyl:8x6, Z_C (Pa2 Pc4 / pa3 pc5, kings c2/c3 and a4/a5, all pawns blocked, no textbook passer) and its mirror on cyl:8x6 only. Exhaustive (F_Z = a-c, <= 2+2, 3+2, 2+3, no cut-off) finds exactly these; flat 7x7: none (min leak 1). Roots and move lists CHECKED-2; search CHECKED-2 for 2+2 on four boards, COMPUTED-1 otherwise; no hand proof on the cylinder.',
 'conjecture_4_7': 'first half supported in P (no exact under/over group in <= 2+2, 3+2, 2+3 on 3 files of cyl:8x6, nor <= 2+2 on cyl:7x6, flat 7x6, flat 8x6, nor <= 2+2 on 4 files of cyl:8x6; all reused from the earlier attempt, the fresh over3 runs did not get a lock slot; 3+2/2+3 on cyl:7x6/flat 7x6 and flat 7x7 not searched); second half (wider groups) neither supported nor refuted. COMPUTED-1.',
 'exact_on_off': 'exist on every board; match Theorem 3.4(b) beside contexts except where the frozen king can reach a context pawn through the wrap or the shuttler has a helpful other move: (Pun) fails beside that context.',
 'z_b_contexts': 'Z_B equals dud_D in every exhaustive context of <= 3 pawns tried (see contexts_fresh); Z_C does not.'}
json.dump(S, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1)
print('summary.json', os.path.getsize(os.path.join(OUT, 'summary.json')), 'bytes')
