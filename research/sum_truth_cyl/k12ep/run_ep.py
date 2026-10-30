"""Regenerate K12 roots (copied gen.py), keep only roots carrying an e.p. right, certify them with the copied checker.py
(e.p. mode: ep tuple passed to check_certified), write kpsolve --frozen inputs. Usage: run_ep.py W H K"""
import sys, json, os
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen as G, checker as C, process as PR
from cylcgt import pawns as P
W, H, K = map(int, sys.argv[1:4])
OUT = os.path.dirname(os.path.abspath(__file__))
uniq, board = G.process_board(W, H, K)
tot = len(uniq)
ep = [r for r in uniq if r[4] is not None]
print(W, H, 'roots', tot, 'with ep', len(ep), 'noep', tot - len(ep), flush=True)
rows = []
for (W_, H_, Wp, Bp, e, stm) in ep:
    root = {'W': W, 'H': H, 'Wp': Wp, 'Bp': Bp, 'ep': (list(e[0]), list(e[1]), e[2]), 'stm': stm}
    pos = C.make_pos(Wp, Bp, root['ep'], W, H)
    oW = len(C.passed_pawns_list(board, pos, 'W', W, H)) > 0
    oB = len(C.passed_pawns_list(board, pos, 'B', W, H)) > 0
    cW, cB = P.passed(board, pos, 'W'), P.passed(board, pos, 'B')
    beta = PR.beta_for_root(root)
    cert = C.check_certified(W, H, Wp, Bp, root['ep'], stm, beta)
    rows.append({'line': PR.kpsolve_line(root), 'beta': beta, 'certified': cert, 'single': oW ^ oB, 'race': oW and oB,
                 'selftest_ok': (cW == oW and cB == oB)})
json.dump(rows, open(f'{OUT}/ep_{W}x{H}.json', 'w'))
open(f'{OUT}/ep_{W}x{H}_in.txt', 'w').write('\n'.join(r['line'] for r in rows) + '\n')
print('done', len(rows), 'cert', sum(r['certified'] for r in rows), flush=True)
