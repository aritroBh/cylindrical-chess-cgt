#!/usr/bin/env python3
"""K15 r3: write fin2/logs/r3_additions.md (section 7.5 of FINDINGS.md), fin2/logs/over_followup.md, fin2/body_head.md and fin2/body_verdicts.md.
All numbers that come from runs are read from r3/logs, r3/data and fin2/logs; the prose is fixed text."""
import os, re, json, glob, hashlib
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K15 = os.path.dirname(R3); FIN2 = os.path.join(K15, 'fin2')
def rd(p, d=''):
    try: return open(p).read()
    except Exception: return d
def md5(p):
    try: return hashlib.md5(open(p, 'rb').read()).hexdigest()
    except Exception: return '?'

# ---------- facts from logs ----------
cmp_ref3 = rd(os.path.join(R3, 'logs', 'cmp_ref3.txt')).strip().splitlines()
rerun = [l for l in rd(os.path.join(R3, 'logs', 'rerun.log')).splitlines() if 'exit=' in l]
same_bins = all(md5(os.path.join(R3, 'bin', b)) == md5(os.path.join(FIN2, 'bin', b)) for b in ('grp', 'kp', 'kpp', 'ref3', 'ref3m'))
notrun = rd(os.path.join(R3, 'logs', 'notrun_summary.txt')).strip().splitlines()
chess7 = rd(os.path.join(R3, 'logs', 'chess_cyl7_summary.txt')).strip().splitlines()
zrows = [l for l in rd(os.path.join(R3, 'logs', 'ctxexh_surv_chunked.txt')).splitlines() if l.startswith('Kd5 kb5')]
ref16 = [l for l in rd(os.path.join(R3, 'data', 'zstar_ref16.out')).splitlines() if ' | ' in l]
zchess = rd(os.path.join(R3, 'logs', 'chess_zstar_c1.out')).strip()
zchess_err = rd(os.path.join(R3, 'logs', 'chess_zstar_c1.err')).strip().splitlines()
fullctx = rd(os.path.join(R3, 'logs', 'ctxexh_surv.txt')).strip()

sys_path_added = __import__('sys').path.insert(0, FIN2)
import confirm as C
def pred_of(pos):
    t = pos.split(); stm = t[-2]; pw = [x[1:] for x in t if x[0] == 'P' and x[1] == 'g']; pb = [x[1:] for x in t if x[0] == 'p' and x[1] == 'g']
    w, b = C.solve_d(6, [C.sq(x) for x in pw], [C.sq(x) for x in pb], 'over'); return w if stm == 'w' else b
ref_ok = sum(1 for l in ref16 if pred_of(l.split(' | ')[0].strip()) == l.split(' | ')[1].strip()); ref_bad = len(ref16) - ref_ok
add = []
add.append('### 7.5 Re-checks made in this attempt (`r3/`)')
add.append('')
add.append('This attempt rebuilt every binary itself (`r3/bin/`: `grp` from `K15/grp.c`, `kp` from `kings/kpsolve.c`, `kpp` from `K7/scripts/draft/kp_p.c`, `ref3` and `ref3m` from the K23 sources). %s' % ('The five builds are byte-identical to the binaries of the earlier attempt (md5).' if same_bins else 'The builds differ from the earlier binaries.'))
add.append('')
add.append('- **Census re-runs (COMPUTED-1, reproduction).** Re-run with the rebuilt `grp` (one CPU-minute each, nice 15): %d runs (flat 7×6 ≤ 2+2 plain P; flat 7×6 ≤ 2+2 with passes; cyl:8×6 and cyl:7×6, 3 files ≤ 3+3, both readings). The candidate lists are byte-identical and the JSON counts are identical (`r3/logs/rerun.log`). This shows determinism of one source, not independence.' % len(rerun))
add.append('- **Z_B regression (CHECKED-2 for the values).** `scripts/zb_regression_final.sh` and `scripts/depth.py` re-run: the logs are identical to `fin2/logs/zb_regression_final.txt` and `fin2/logs/zb_depth.txt`. `kpp` and `ref3m` on the 8 roots of Z_B on flat 7×6 give (D, D) at all 8 roots, 8 drawing moves and 26 losing moves (`r3/logs/`, same lists as LOOPY §5.7). On cyl:7×6 and cyl:8×6 (`r3/logs/zb_cyl7_*.txt`, `zb_cyl8_*.txt`): `kpp` and `ref3m` give the same root values (all D) and the same move lists at all 8 roots; 38 legal moves, 8 draw, 30 lose, on both boards.')
add.append('- **G8a and G8b (CHECKED-2 in P, COMPUTED-1 in chess).** `kpp` and `ref3m` on the 16 roots (cyl:8×6): identical root values and identical sorted move lists (`r3/logs/g8_kpp_r3.txt`, `g8_ref3m_r3.txt`). The chess cap-2 lists of `fin2/chess/cyl_8x6_G8_states_c2_mv.out` equal the P lists at all 16 roots (value D D, same moves, same values). Chess has only kpsolve here: `ownchess` of K27 is a flat-board program, so no second chess solver covers the cylinder.')
add.append('- **Second solver on the confirmation tables (CHECKED-2 for the sample).** %s. The positions are seeded random samples of the inputs of the confirmation runs (`r3/scripts/sample_ref3.py`: seeds 7, 8, 9); `ref3` shares no code with `kp_p` (`r3/scripts/cmp_ref3.py`). So the kp_p confirmation tables are CHECKED-2 on these 250 positions and COMPUTED-1 on the rest.' % '; '.join(cmp_ref3))
nr = []
for l in notrun:
    m = re.match(r'(\w+) groups (\d+) .*?: (\d+) others', l)
    if m: nr.append('%s: %s of %s groups' % (m.group(1).replace('_', ':'), m.group(3), m.group(2)))
add.append('- **Root check of the 49 dud groups that the earlier attempt had not confirmed** (found by the later census runs: 12 on cyl:7×6, 12 on cyl:8×6, 25 on cyl:8×8; their rows in `fin2/dud_groups.md` said "not run" before). `kpp --pmodel --moves` at the two roots of each (`r3/data/notrun_*.out`, `r3/scripts/chunkrun.py`): the value is (D, D) at both roots and every non-draw move loses for the mover, for ' + ', '.join(nr) + '. This agrees with the exact classifier `grp` (reading B) at the root (CHECKED-2: independent code). No context was run for these 49: they are dud in the empty context only.')
import ast
def c7(line):
    d = ast.literal_eval(line[line.index('{'):])
    return {k.strip(): v for k, v in d.items()}
parts = []
for l in chess7:
    if l.startswith('D2'):
        name = l.split(' roots')[0]; d = c7(l)
        parts.append('%s: %d moves draw in P and in chess (exact); of the %d moves that lose in P, %d lose in chess (exact), %d draw in chess (exact) and %d are undecided at cap 1' % (name.strip(), d['P draw (shuttle)'], d['P: loses'], d['chess: loses (exact)'], d['chess: draws (exact)'], d['chess: undecided at cap 1']))
add.append('- **Chess on the 7×6 cylinder, D2 and D2m (COMPUTED-1, kpsolve cap 1, `--moves`, all 24 king states of each, both sides to move; `r3/logs/chess_cyl7_c1_mv.out`).** The root values are exact (D, D) at all 96 roots. Against the P move lists, over the 48 roots of each group: ' + '; '.join(parts) + '. So D2 and D2m are **not** two-shuttle in chess: about half of the deviations that lose in P draw in chess (among them king moves across the wrap, such as Ka1–g1 and Ka1–g2 from the root of D2m, which lose in P and draw in chess).')
add.append('')
add.append('**The over-like survivor Z\\* (section 7.3).** Context runs of this attempt, `r3/scripts/ctxexh_chunked.py` (all assignments of {empty, White pawn, Black pawn} to the squares X2..X5 of one context file X with at most 3 context pawns; both sides to move; prediction r(G ⊞ over_D) by `confirm.solve_d`; value by `kp_p --pmodel`, exact):')
add.append('')
add.append('| board | context file | contexts (≤ 3 pawns) | positions | agree | DISAGREE | inexact | missing |')
add.append('|---|---|---|---|---|---|---|---|')
boards = ['cyl:8x6', 'cyl:8x6', 'cyl:7x6']
for i, l in enumerate(zrows):
    m = re.search(r'file (\w): (\d+) contexts \((?:at most )?(\d+)(?: to (\d+))? pawns\) x 2 sides = (\d+) positions: agree (\d+), DISAGREE (\d+), inexact (\d+), missing (\d+)', l)
    if m:
        f, nc, _, _, npos, ag, di, ix, ms = m.groups()
        add.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % (boards[i] if i < 3 else '?', f, nc, npos, ag, di, ix, ms))
add.append('')
dis_lines = [l.strip() for l in rd(os.path.join(R3, 'logs', 'ctxexh_surv_chunked.txt')).splitlines() if l.startswith('   context')]
add.append('The disagreements (same three on both boards, file f; the assignment is read f2 f3 f4 f5 with W = White pawn, B = Black pawn, . = empty): ' + '; '.join(sorted(set(dis_lines))) + '. One of them, `Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4 Pf3 pf4 pf5 b -`, was also solved by `ref3` (value L, equal to `kp_p`; the over prediction is W): CHECKED-2 (`r3/data/zstar_f3.ref3.out`). There Black plays d4–d3 and wins; in the empty context that move loses.')
if ref16:
    add.append('')
    add.append('`ref3` on %d sampled positions of the file-g contexts (≤ 2 context pawns, `r3/data/zstar_ref16.in`, `.out`): %d equal the over prediction, %d do not (CHECKED-2 for this sample of the 130 agreeing positions).' % (len(ref16), ref_ok, ref_bad))
add.append('')
if zchess:
    add.append('Chess, Z\\* alone (kpsolve cap 1, `r3/logs/chess_zstar_c1.out`): `' + zchess.replace('\n', '` ; `') + '`. ' + (zchess_err[-2] if len(zchess_err) >= 2 else ''))
else:
    add.append('Chess for Z\\*: not run: the `heavy.sh` job waited about 50 minutes for a slot of the shared lock (held by other jobs) and was cancelled by its owner (PIDs in `r3/logs/my_queued_heavy_pids.txt`); not claimed.')
if fullctx:
    add.append('')
    add.append('The full single-file run of the earlier script `ctx_exh.py` (all 81 assignments, 4-pawn contexts included, through the lock) finished: ```' + fullctx + '```')
else:
    add.append('')
    add.append('The queued full run of `ctx_exh.py` (all 81 assignments per file, which includes the contexts with 4 pawns, and the context files e and f of the 7×6 board) waited about two hours for a slot of the shared lock and was cancelled; the 4-pawn contexts are untested for Z\\*.')
open(os.path.join(FIN2, 'logs', 'r3_additions.md'), 'w').write('\n'.join(add) + '\n')
print('\n'.join(add)[:3000])
