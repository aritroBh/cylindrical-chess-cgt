"""K8v: tables for the report, built only from my own outputs (out/*.json, logs/*.log) and, for the comparison columns,
K8's json data files.  usage: v8_tables.py > report_tables.txt"""
import glob, json, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
K8 = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8'
TASK1 = ['cyl:5x4', 'cyl:3x7', 'cyl:5x7', 'cyl:3x8', 'cyl:4x7', 'cyl:4x8', 'flat:4x6', 'flat:3x7', 'cyl:2x6', 'cyl:2x8', 'cyl:6x7']
CHESS = ['flat:3x4', 'flat:4x4', 'cyl:4x4', 'cyl:4x6', 'flat:5x6', 'cyl:3x6', 'cyl:5x6', 'cyl:6x5', 'cyl:7x5', 'cyl:3x7', 'cyl:3x8', 'cyl:2x6', 'cyl:2x8']
tag = lambda b: b.replace(':', '_')
summ = json.load(open(os.path.join(K8, 'summary.json')))
K8T1 = {r['board']: r for r in summ['task1']}
# ---- parse logs
vrun = {}
for l in open(os.path.join(HERE, 'logs/v_run.log')):
    m = re.match(r'(\S+) quiet placements mine/jsonl (\d+) (\d+) mismatches (\{.*\})', l)
    if m:
        vrun[m.group(1)] = (int(m.group(2)), int(m.group(3)), sum(eval(m.group(4)).values()))
chk1 = {}
for l in open(os.path.join(HERE, 'logs/v_check1.log')):
    m = re.match(r'MY check1 (\S+) compared (\d+) \(KPK (\d+), other (\d+)\) differences (\d+) non-exact kp lines (\d+)', l)
    if m:
        chk1[m.group(1)] = tuple(int(x) for x in m.groups()[1:])
det = {}
for l in open(os.path.join(HERE, 'logs/v6_detail.log')):
    if l.startswith('{'):
        d = json.loads(l); det[d['board']] = d
legal = {}
for l in open(os.path.join(HERE, 'logs/v_legal.log')):
    m = re.match(r'(\S+) all candidate lines (\d+) kpsolve non-X (\d+) mine legal KPK (\d+) symmetric difference (\d+)', l)
    if m:
        legal[m.group(1)] = tuple(int(x) for x in m.groups()[1:])
offl = {}
cur = None
for l in open(os.path.join(HERE, 'logs/v_offclass.log')):
    if l.startswith('   off placements'):
        names = re.findall(r"\('([^']+)', \d+, \d+\)", l)
        offl[cur] = names
    else:
        cur = l.split()[0]
print('== TASK 1: normal play (11 boards).  quiet placements compared / per-placement mismatches (signature, class, chess T=0, diff vs K8 jsonl) / tempo-detail diffs')
print('%-9s %7s %7s %5s %5s %4s %-48s %9s %5s %6s %-10s' % ('board', 'quiet', 'K8jsonl', 'mism', 'off', 'sens', 'thresholds', 'kpcmp', 'kpdif', 'detdif', 'prediction'))
tot_cmp = 0
seen = {}
for b in TASK1:
    r = K8T1[b]; d = det[b]
    q, qk8, mis = vrun[b]
    c = chk1[b]
    off = int(re.search(r'off/off\+\* (\d+)', d['classes']).group(1))
    seen[b] = c[0]
    print('%-9s %7d %7d %5d %5d %4d %-48s %9d %5d %6d %-10s' % (b, q, qk8, mis, off, d['tempo_sensitive'], json.dumps(d['thresholds']).replace(' ', ''), c[0], c[3], d['total_diffs'],
          ('OK' if (off > 0) == (d['tempo_sensitive'] > 0) and d['tempo_sensitive'] == r['tempo_sensitive'] and off == r['off_placements'] else 'DIFF')))
print('legal-KPK-set check (all candidate lines, kpsolve non-X, mine, symdiff):', {b: legal[b] for b in TASK1})
ok = 0
for b in TASK1:
    k = json.load(open(os.path.join(K8, 'offclass_%s.json' % tag(b))))
    mine = sorted(offl.get(b, []))
    ok += mine == sorted(k['white_stalemated_placements'])
print('off-class placements (White to move, no legal move) equal K8 offclass lists on %d of %d boards' % (ok, len(TASK1)))
print()
# ---- Task 2
print('== TASK 2: chess stalemate rule (13 boards)')
print('%-9s %6s %8s %5s | %5s %5s %5s %5s | %4s %6s %6s %6s | %5s %5s | %s' % ('board', 'quiet', 'check1', 'diff', 'sens', '+1', '-1', '+-1', 'zug', 'z!pm1', 'pm1!z', 'pm1!z%', 'both', 'norm', 'K8 mismatches (placement fields / aggregates / sensitive list)'))
t2 = {}
for b in CHESS:
    d = json.load(open(os.path.join(HERE, 'out/chess_%s.json' % tag(b))))
    t2[b] = d; r = d['rules']['WdBd']
    print('%-9s %6d %8d %5d | %5d %5d %5d %5d | %4d %6d %6d %6.1f | %5d %5d | %d / %d / %d' % (
        b, d['quiet'], d['check1']['nodes'], d['check1']['differences'], r['tempo_sensitive'], r['sensitive_at_plus1'], r['sensitive_at_minus1'], r['sensitive_at_pm1'],
        d['mutual_zugzwangs'], d['zug_not_sens_pm1'], d['pm1_not_zug'], d['pm1_not_zug_share_percent'] if d['pm1_not_zug'] or d['mutual_zugzwangs'] else 0.0,
        d['sens_both_rules'], d['normal_tempo_sensitive'], d['K8_total_mismatches'], len(d['K8_tempo_detail_aggregate_mismatches']),
        d['sensitive_listing_symmetric_difference_with_K8_tempo_detail']))
print()
print('thresholds (chess rule) and tails n=-20..-2 / n=2..20 (constant, period2, other):')
for b in CHESS:
    r = t2[b]['rules']['WdBd']
    print('%-9s thr %s  tail- %s  tail+ %s' % (b, json.dumps(r['thresholds']).replace(' ', ''), tuple(r['tails_n_minus20_to_minus2'].values()), tuple(r['tails_n_2_to_20'].values())))
print()
print('zugzwang vs spare move details: kp pair of mutual zugzwangs; non-zugzwang sensitive-at-+-1 by kp pair and by direction; chess zugzwangs not all-W under normal play; normal-play strict zugzwang placements')
for b in CHESS:
    d = t2[b]
    print('%-9s zug_by_pair %s | pm1_not_zug_by_pair %s | direction %s | chess-zug-not-allW-in-normal-play %d | normal-play strict zugzwang KPK placements %d %s | zug not sens at both +1 and -1: %d | zug not tempo-sensitive: %d' % (
        b, d['zug_by_pair'], d['pm1_not_zug_by_kp_pair'], d['pm1_not_zug_direction'], d['chess_zug_not_all_W_under_normal_play'],
        d['normal_play_strict_zugzwang_placements'], d['normal_play_strict_zugzwang_pairs'], d['zug_not_sens_at_both_plus1_and_minus1'], d['zug_not_tempo_sensitive']))
print()
# ---- variant check totals
print('== variant check at T = 0 (my chess-rule solver vs kpsolve), compared / differences')
tot = 0; totd = 0
allb = list(dict.fromkeys(TASK1 + CHESS))
rows = []
for b in allb:
    if b in chk1:
        n, kpk, oth, dif, ne = chk1[b]
    else:
        c = t2[b]['check1']; n, kpk, oth, dif, ne = c['nodes'], c['kpk'], c['other'], c['differences'], c['kp_nonexact_lines']
    tot += n; totd += dif
    rows.append('%s %d/%d' % (b, n, dif))
print('; '.join(rows))
print('boards', len(allb), 'positions compared', tot, 'differences', totd)
