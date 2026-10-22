"""K6 verifier (B pipeline): per board, with my own graph (v_gen), test games (v_games) and C solver (v_prod):
  1. every quiet placement: class counts by my own signatures (compared with the reported class string);
  2. tempo sensitivity of EVERY placement: the 11 finite test games (0,1,2,-1,-2,*,up,down,1/2,-1/2,+-1) and the
     integer scan x + n, n = -10..10 (pair of results, White-starts / Black-starts);
  3. comparison with the builder's tempo_detail_<tag>.json (sensitive list, finite results, full n profile,
     jump positions) and with the aggregate numbers in structured_boards.json.
usage: v6_detail.py flat:3x4 ...     (writes verify/out/<tag>_mine.json, prints one summary line per board)"""
import json, os, sys, collections, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); K6 = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8'
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run

OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
RANGE = list(range(-10, 11))
FIN = vg.TESTS[:11]
assert FIN == ['0', '1', '2', '-1', '-2', '*', 'up', 'down', '1/2', '-1/2', '+-1']
REPORTED = {r['board']: r for r in json.load(open(os.path.join(K6, 'summary.json')))['task1']}
CSIG = {nm: vg.signature(V) for nm, V in vg.candidates()}
BY = {}
for nm, s in CSIG.items():
    BY.setdefault(s, []).append(nm)


def classify(sig):
    dec = 'W' if set(sig) == {'W'} else 'L' if set(sig) == {'L'} else None
    m = BY.get(sig, [])
    if dec == 'W':
        return 'WHITE-WINS-ALL'
    if dec == 'L':
        return 'BLACK-WINS-ALL'
    if m:
        return '/'.join(m)
    pairs = {sig[i:i + 2] for i in range(0, 32, 2)}
    return 'unmatched T-independent' if len(pairs) == 1 else 'unmatched T-dependent'


def fmt_classes(c):
    keys = [('WHITE-WINS-ALL', 'WHITE-WINS-ALL'), ('on/on+*', 'on/on+*'), ('off/off+*', 'off/off+*'), ('dud', 'dud'),
            ('unmatched T-dependent', 'unmatched T-dependent'), ('unmatched T-independent', 'unmatched T-independent')]
    s = '; '.join('%s %d' % (lab, c.get(k, 0)) for k, lab in keys)
    other = {k: v for k, v in c.items() if k not in dict(keys)}
    return s, other


def main(board):
    t0 = time.time()
    M = v_gen.build(board); G = M['G']; n = len(M['nodes'])
    tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.graph')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]),
                                           ' '.join(map(str, M['succ'][i]))))
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes'])
             if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    tpath = os.path.join(v_run.WORK, tag + '.games6')
    v_run.write_games(tpath, [('T%d' % k, vg.GAMES[t]) for k, t in enumerate(vg.TESTS)])
    R = v_run.run_c(gpath, tpath, 0)
    v_run.write_games(tpath, [('N%d' % (k + 20), vg.integer(k)) for k in RANGE])
    NR = v_run.run_c(gpath, tpath, 0)
    os.remove(gpath); os.remove(tpath)
    classes = collections.Counter()
    mine = {}
    for (cw, cb) in quiet:
        p = M['nodes'][cw]
        pl = 'K%s P%s k%s' % (v_gen.name(G, p[1]), v_gen.name(G, p[3]), v_gen.name(G, p[2]))
        sig = ''.join(R['T%d' % k][cw] + R['T%d' % k][cb] for k in range(len(vg.TESTS)))
        fin = {t: R['T%d' % k][cw] + R['T%d' % k][cb] for k, t in enumerate(vg.TESTS) if t in FIN}
        prof = [NR['N%d' % (k + 20)][cw] + NR['N%d' % (k + 20)][cb] for k in RANGE]
        jumps = [k for k, a, b in zip(RANGE, prof, prof[1:]) if a != b]
        fsens = len(set(fin.values())) > 1
        nsens = bool(jumps)
        c = classify(sig)
        classes[c] += 1
        mine[pl] = dict(cls=c, fin=fin, prof=prof, jumps=jumps, fsens=fsens, nsens=nsens, sens=fsens or nsens)
    cls_str, other = fmt_classes(classes)
    rep = REPORTED.get(board)
    # ---- compare with the builder's detail file
    det = json.load(open(os.path.join(K6, 'tempo_detail_%s.json' % tag)))
    b_sens = {e['placement']: e for e in det['sensitive']}
    m_sens = {pl: m for pl, m in mine.items() if m['sens']}
    bad = collections.Counter()
    bad['sensitive_set_only_mine'] = len(set(m_sens) - set(b_sens))
    bad['sensitive_set_only_builder'] = len(set(b_sens) - set(m_sens))
    for pl in set(m_sens) & set(b_sens):
        e, m = b_sens[pl], m_sens[pl]
        bad['finite_results'] += e['finite_tests'] != m['fin']
        bad['n_profile_full'] += {str(k): v for k, v in zip(RANGE, m['prof'])} != e['n_profile_full']
        bad['jumps_at'] += e['jumps_at'] != m['jumps']
    nj = collections.Counter(len(m['jumps']) for m in mine.values())
    jat = collections.Counter(j for m in mine.values() for j in m['jumps'])
    far = sum(any(j >= 2 or j <= -3 for j in m['jumps']) for m in mine.values())
    agg = dict(quiet=len(mine), tempo_sensitive=len(m_sens), sensitive_to_finite_tests=sum(m['fsens'] for m in mine.values()),
               sensitive_to_n_scan=sum(m['nsens'] for m in mine.values()),
               thresholds={str(k): v for k, v in sorted(jat.items())}, max_jump_beyond_pm2=far)
    for k in ('quiet', 'tempo_sensitive', 'sensitive_to_finite_tests', 'sensitive_to_n_scan', 'max_jump_beyond_pm2'):
        bad['agg_' + k] += agg[k] != det[k]
    bad['agg_thresholds'] += agg['thresholds'] != det['thresholds']
    # ---- compare with tempo_scan.jsonl line
    ts = [json.loads(l) for l in open(os.path.join(K6, 'tempo_scan.jsonl'))]
    ts = [t for t in ts if t['board'] == board]
    assert len(ts) == 1, 'tempo_scan lines for %s: %d' % (board, len(ts))
    t = ts[0]
    bad['scan_placements'] += t['placements'] != len(mine)
    bad['scan_number_of_jumps'] += t['number_of_jumps'] != {str(k): v for k, v in sorted(nj.items())}
    bad['scan_jump_positions'] += t['jump_between_n_and_n_plus_1'] != {str(k): v for k, v in sorted(jat.items())}
    bad['scan_far'] += t['placements_with_a_jump_beyond_pm2'] != far
    # ---- compare with the reported class string and tempo summary
    if rep:
        coll = collections.Counter()
        for k, v in classes.items():
            coll['unmatched' if k.startswith('unmatched') else k] += v
        bad['reported_quiet'] += rep['quiet'] != len(mine)
        bad['reported_classes'] += dict(coll) != rep['classes']
        bad['reported_tempo_sensitive'] += rep['tempo_sensitive'] != len(m_sens)
        bad['reported_thresholds'] += rep['thresholds'] != agg['thresholds']
        bad['reported_off_placements'] += rep['off_placements'] != classes.get('off/off+*', 0)
        bad['reported_finite'] += rep['sensitive_to_finite_tests'] != agg['sensitive_to_finite_tests']
        bad['reported_nscan'] += rep['sensitive_to_n_scan'] != agg['sensitive_to_n_scan']
        bad['reported_far'] += rep['max_jump_beyond_pm2'] != agg['max_jump_beyond_pm2']
    else:
        bad['reported_missing'] += 1
    # ---- class of the sensitive placements, and whether pairs for n=0 equal test '0'
    sens_cls = collections.Counter(m['cls'] for m in m_sens.values())
    n0 = sum(m['prof'][RANGE.index(0)] != m['fin']['0'] for m in mine.values())
    n1 = sum(m['prof'][RANGE.index(1)] != m['fin']['1'] or m['prof'][RANGE.index(-2)] != m['fin']['-2'] or
             m['prof'][RANGE.index(2)] != m['fin']['2'] or m['prof'][RANGE.index(-1)] != m['fin']['-1'] for m in mine.values())
    summary = dict(board=board, quiet=len(mine), classes=cls_str, other_classes=other, **{k: agg[k] for k in agg if k != 'quiet'},
                   sensitive_by_class=dict(sens_cls), n_profile_vs_finite_test_inconsistencies=n0 + n1,
                   builder_tempo_detail_sensitive=len(b_sens), diffs=dict(bad), total_diffs=sum(bad.values()),
                   seconds=round(time.time() - t0, 1))
    json.dump(dict(summary=summary, sensitive={pl: dict(fin=m['fin'], prof=m['prof'], jumps=m['jumps'], cls=m['cls'])
                                                for pl, m in m_sens.items()}),
              open(os.path.join(OUT, tag + '_mine.json'), 'w'))
    print(json.dumps(summary), flush=True)
    return summary['total_diffs']


if __name__ == '__main__':
    sys.exit(1 if sum(main(b) for b in sys.argv[1:]) else 0)
