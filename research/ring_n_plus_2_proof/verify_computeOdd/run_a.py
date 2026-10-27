"""run_a.py -- (a) outcome of G + *h, h = 0..HMAX, for R_n and Qo_n, odd n = LO..HI, by an independent engine.

  python run_a.py ENGINE LO HI [FAMS] [HMAX]
  ENGINE: mine  = oddeng.py (this directory), flags 'keep' and 'expire' (and 'raw' flags for n <= 15),
          E     = verify_compute/myeng.py (Full solver, 'keep' and 'expire'),
          C     = check3/eng.py (T50 verifier's solver),
          exh   = oddeng.py in the EXHAUSTIVE (no early exit) mode, for small n only.
  Expectation (G = *k means: G + *h has outcome P for h = k and N otherwise):
          R_n  = *2:  NNPNNNN..   Qo_n = *3:  NNNPNNN..   for n >= 11;   n = 9: all L.
Every line: family, n, pawns, signature, number of states, seconds, and whether it equals the expectation.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'verify_compute'))
sys.path.insert(0, os.path.join(HERE, '..', 'check3'))
import oddeng as O          # noqa: E402


def expected(fam, n, hmax):
    k = {'R': 2, 'Qo': 3}[fam]
    return ''.join('P' if h == k else 'N' for h in range(hmax + 1))


def main():
    engine = sys.argv[1]
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    fams = sys.argv[4].split(',') if len(sys.argv) > 4 else ['R', 'Qo']
    hmax = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    hs = range(hmax + 1)
    if engine == 'E':
        import myeng as E
    if engine == 'C':
        import eng as C
    for fam in fams:
        for n in range(lo, hi + 1, 2):
            toks = O.tokens_R(n) if fam == 'R' else O.tokens_Qo(n)
            pos = O.parse(toks)
            assert O.npawns(pos) == n + 2
            runs = []
            if engine == 'mine':
                for label, kw in (('keep', dict(mode='keep')), ('expire', dict(mode='expire')),
                                  ('raw-keep', dict(mode='keep', raw=True))):
                    if label == 'raw-keep' and n > 15:
                        continue
                    t0 = time.time()
                    F = O.Full(**kw)
                    runs.append((label, F.signature(pos, hs), len(F.memo), time.time() - t0))
            elif engine == 'exh':
                for label, kw in (('exhaustive-keep', dict(mode='keep', exhaustive=True)),
                                  ('exhaustive-expire', dict(mode='expire', exhaustive=True))):
                    t0 = time.time()
                    F = O.Full(**kw)
                    runs.append((label, F.signature(pos, hs), len(F.memo), time.time() - t0))
            elif engine == 'E':
                pe = tuple(E.parse_file(t) for t in toks)
                assert pe == O.to_pairs(pos)
                for label in ('keep', 'expire'):
                    t0 = time.time()
                    F = E.Full(label)
                    runs.append((label, F.signature(pe, hs), F.nodes, time.time() - t0))
            elif engine == 'C':
                pc = C.parse(toks)
                assert pc == O.to_pairs(pos)
                t0 = time.time()
                S = C.Solver()
                sig = ''
                for h in hs:
                    a = S.win(pc, None, h, 'W')
                    b = S.win(pc, None, h, 'B')
                    sig += {(True, True): 'N', (True, False): 'L', (False, True): 'R', (False, False): 'P'}[(a, b)]
                runs.append(('T50', sig, S.nodes, time.time() - t0))
            want = expected(fam, n, hmax)
            sigs = {s for _, s, _, _ in runs}
            if n == 9:
                verdict = 'n=9: all L' if sigs == {'L' * (hmax + 1)} else 'n=9: UNEXPECTED ' + str(sigs)
            else:
                verdict = ('== ' + ('*2' if fam == 'R' else '*3') if sigs == {want} else
                           'DIFFERENT from ' + want + ' !!!') + (' (engines/modes agree)' if len(sigs) == 1 else ' (MODES DISAGREE)')
            print(f'{engine} {fam}_{n} pawns={n + 2} ' + ' | '.join(f'{lab}: {s} ({k} states, {t:.1f}s)' for lab, s, k, t in runs)
                  + '  ' + verdict, flush=True)


if __name__ == '__main__':
    main()
