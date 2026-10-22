#!/usr/bin/env python3
"""T44: statistics for KPKP on the 8x8 flat board and the 8x8 cylinder (corrected input).

Streams the four chunk files kpkp_<board>_<i>.out.zst (kpsolve output, `<position> | A B`, values in White's view,
A >= true >= B) and never holds more than two 19 MB byte tables in memory.

Pass 1 loads the flat board, pass 2 the cylinder, comparing each cylinder position with the flat position on the
same squares and the same side to move.  Writes (all small) into this directory:
    stats.json                numbers for the report
    mz_cyl_only.tsv.zst       every cylinder-only mutual zugzwang pair (certain on the cylinder, not possible on flat)
    sample_<board>.txt        a uniform reservoir sample of legal positions with their (A, B), for the 2nd-program check
    diffs_sample.txt          a random sample of positions whose result differs between the boards
Usage (project root):  .venv/bin/python -I research/kpkp/t44/analyze_t44.py
"""
import json
import os
import random
import subprocess
import sys

HERE = os.environ.get('T44_DIR') or os.path.dirname(os.path.abspath(__file__))
NCHUNK = 4
RES = {'L': 0, 'D': 1, 'W': 2}
NAME = 'LDW'
SQ = {'abcdefgh'[f] + str(r + 1): r * 8 + f for r in range(8) for f in range(8)}
NKEY = 64 * 64 * 48 * 48          # (wk, bk, wp, bp)  ->  index
RESERVOIR = 1500


def sqname(s):
    return 'abcdefgh'[s % 8] + str(s // 8 + 1)


def fen(wk, wp, bk, bp, stm):
    rows = []
    for r in range(7, -1, -1):
        row, empty = '', 0
        for f in range(8):
            s = r * 8 + f
            ch = {wk: 'K', wp: 'P', bk: 'k', bp: 'p'}.get(s)
            if ch is None:
                empty += 1
            else:
                if empty:
                    row += str(empty)
                    empty = 0
                row += ch
        if empty:
            row += str(empty)
        rows.append(row)
    return '/'.join(rows) + ' ' + stm + ' - - 0 1'


def stream(board):
    for i in range(NCHUNK):
        p = subprocess.Popen(['zstdcat', os.path.join(HERE, 'kpkp_%s_%d.out.zst' % (board, i))],
                             stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
        for line in p.stdout:
            yield line
        p.stdout.close()
        if p.wait() != 0:
            raise SystemExit('zstdcat failed on %s chunk %d' % (board, i))


def pair_status(cw, cb):
    """cw, cb: codes (hi*3+lo+1) of the White-to-move and Black-to-move positions on the same squares.
    The side to move does worse than the other side iff v_w < v_b.  Returns
    0 none (one side illegal) / 1 certainly not / 2 possible but not certain /
    3 certain, exact (L,D) / 4 certain, exact (L,W) / 5 certain, exact (D,W) / 6 certain, bounds not exact."""
    if cw == 0 or cb == 0 or cw == 10 or cb == 10:
        return 0
    hw, lw = divmod(cw - 1, 3)
    hb, lb = divmod(cb - 1, 3)
    if hw < lb:                                   # upper bound of v_w below lower bound of v_b
        if hw == lw and hb == lb:
            return {(0, 1): 3, (0, 2): 4, (1, 2): 5}[(hw, hb)]
        return 6
    if lw < hb:
        return 2
    return 1


def load(board, flat_tabs=None, rng=None):
    """One pass over a board. Returns (stats, code table, pair-status table, reservoir, extras)."""
    code = bytearray(NKEY * 2)
    mz = bytearray(NKEY)
    cnt = {}                                       # (stm, A, B) -> n
    res_sample = []
    seen = 0
    nleg = 0
    extra = {'cyl_only_mz': 0, 'mz_flat_not_cyl': 0, 'both_mz': 0, 'cyl_mz_flat_maybe': 0,
             'flat_only_positions': 0, 'both_positions': 0, 'cyl_only_positions': 0}
    chg = {}                                       # (stm, flat_res, cyl_res) exact-exact differing
    chg_inexact = {}                               # (stm, 'flat A B', 'cyl A B') where intervals disjoint
    same_exact = {}                                # stm -> n of exact-exact equal
    unresolved_compat = {}                         # stm -> n pairs with an inexact side and overlapping intervals
    diff_sample = []
    ndiff = 0
    mz_types = {}
    seam_mz = 0
    out_mz = None
    if flat_tabs is not None:
        out_mz = subprocess.Popen(['zstd', '-q', '-3', '-f', '-o', os.path.join(HERE, 'mz_cyl_only.tsv.zst')],
                                  stdin=subprocess.PIPE, text=True)
        out_mz.stdin.write('wk\twp\tbk\tbp\tcyl_w\tcyl_b\tflat_w\tflat_b\tcyl_type\tseam\tfen_w\n')
    for line in stream(board):
        t = line.split()
        wk, wp, bk, bp = SQ[t[0][1:]], SQ[t[1][1:]], SQ[t[2][1:]], SQ[t[3][1:]]
        stm = t[4]
        a, b = t[7], t[8]
        cnt[(stm, a, b)] = cnt.get((stm, a, b), 0) + 1
        seen += 1
        if a == 'X' or b == 'X':
            continue
        key = ((wk * 64 + bk) * 48 + (wp - 8)) * 48 + (bp - 8)
        si = 0 if stm == 'w' else 1
        c = 1 + RES[a] * 3 + RES[b]
        code[key * 2 + si] = c
        # reservoir sample of legal positions
        nleg += 1
        if rng is not None:
            if len(res_sample) < RESERVOIR:
                res_sample.append((line.rstrip('\n')))
            else:
                j = rng.randrange(nleg)
                if j < RESERVOIR:
                    res_sample[j] = line.rstrip('\n')
        if si == 1:                                # Black-to-move line: pair with the White-to-move twin
            st = pair_status(code[key * 2], c)
            mz[key] = st
            if st >= 3:
                mz_types[st] = mz_types.get(st, 0) + 1
        # cross-board comparison (second pass only)
        if flat_tabs is not None:
            fcode, fmz = flat_tabs
            fc = fcode[key * 2 + si]
            if fc == 0:
                extra['cyl_only_positions'] += 1
            else:
                extra['both_positions'] += 1
                fh, fl = divmod(fc - 1, 3)
                ch, cl = RES[a], RES[b]
                if fh == fl and ch == cl:
                    if fh == ch:
                        same_exact[stm] = same_exact.get(stm, 0) + 1
                    else:
                        k = (stm, NAME[fh], NAME[ch])
                        chg[k] = chg.get(k, 0) + 1
                        ndiff += 1
                        if len(diff_sample) < 4000:
                            diff_sample.append(line.rstrip('\n') + '  flat=' + NAME[fh])
                        else:
                            j = rng.randrange(ndiff)
                            if j < 4000:
                                diff_sample[j] = line.rstrip('\n') + '  flat=' + NAME[fh]
                else:
                    if ch < fl or fh < cl:         # bounds intervals [lo, hi] disjoint: certainly different
                        k = (stm, 'flat %s%s' % (NAME[fh], NAME[fl]), 'cyl %s%s' % (a, b))
                        chg_inexact[k] = chg_inexact.get(k, 0) + 1
                    else:
                        unresolved_compat[stm] = unresolved_compat.get(stm, 0) + 1
            if si == 1:
                fst = fmz[key]
                if st >= 3:
                    if fst >= 3:
                        extra['both_mz'] += 1
                    elif fst == 1:                 # flat: certainly NOT a mutual zugzwang
                        extra['cyl_only_mz'] += 1
                        wf, rf = wp % 8, bp % 8
                        seam = int({wf, rf} == {0, 7})
                        seam_mz += seam
                        fw = code2s(fcode[key * 2])
                        fb = code2s(fcode[key * 2 + 1])
                        out_mz.stdin.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s\n' % (
                            sqname(wk), sqname(wp), sqname(bk), sqname(bp),
                            code2s(code[key * 2]), code2s(c), fw, fb, st, seam, fen(wk, wp, bk, bp, 'w')))
                    elif fst != 0:
                        extra['cyl_mz_flat_maybe'] += 1
                elif fst >= 3:
                    extra['mz_flat_not_cyl'] += 1
    if out_mz:
        out_mz.stdin.close()
        out_mz.wait()
    extra.update({'chg': {'%s:%s>%s' % k: v for k, v in sorted(chg.items())},
                  'chg_inexact_certain': {'%s:%s>%s' % k: v for k, v in sorted(chg_inexact.items())},
                  'same_exact': same_exact, 'unresolved_compatible': unresolved_compat,
                  'ndiff_exact': ndiff, 'seam_cyl_only_mz': seam_mz})
    return cnt, code, mz, res_sample, diff_sample, mz_types, extra


def code2s(c):
    if c == 0:
        return '--'
    if c == 10:
        return 'XX'
    h, l = divmod(c - 1, 3)
    return NAME[h] + NAME[l]


def summarise(cnt):
    out = {}
    for stm in 'wb':
        row = {'total': 0}
        for (s, a, b), n in cnt.items():
            if s != stm:
                continue
            row['total'] += n
            row[a + b] = row.get(a + b, 0) + n
        out[stm] = row
    return out


def main():
    rng = random.Random(20261022)
    res = {}
    cnt_f, code_f, mz_f, samp_f, _, mzt_f, _ = load('flat', None, rng)
    res['flat'] = {'counts': summarise(cnt_f), 'mz_types(3=LD,4=LW,5=DW,6=inexact)': mzt_f,
                   'mz_pairs_certain': sum(mzt_f.values()),
                   'mz_pairs_possible_only': mz_f.count(2)}
    cnt_c, code_c, mz_c, samp_c, diff_s, mzt_c, extra = load('cyl', (code_f, mz_f), rng)
    res['cyl'] = {'counts': summarise(cnt_c), 'mz_types(3=LD,4=LW,5=DW,6=inexact)': mzt_c,
                  'mz_pairs_certain': sum(mzt_c.values()), 'mz_pairs_possible_only': mz_c.count(2)}
    # positions legal on flat but not enumerated for the cylinder
    nflat_only = 0
    for i in range(NKEY * 2):
        if code_f[i] and not code_c[i]:
            nflat_only += 1
    extra['flat_only_positions'] = nflat_only
    res['cross'] = extra
    with open(os.path.join(HERE, 'stats.json'), 'w') as f:
        json.dump(res, f, indent=1, sort_keys=True)
    for board, samp in (('flat', samp_f), ('cyl', samp_c)):
        with open(os.path.join(HERE, 'sample_%s.txt' % board), 'w') as f:
            f.write('\n'.join(samp) + '\n')
    with open(os.path.join(HERE, 'diffs_sample.txt'), 'w') as f:
        f.write('\n'.join(diff_s) + '\n')
    print(json.dumps(res, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
