"""run_lemma2.py -- Lemma 2 (wall pawns) of T50, checked exhaustively on the actual nodes of the reduced game R_n of P_n.

For every node c of R_n (no flag, no passed pawn), every colour Z, every wall pawn q of colour Z on a file j >= 7 (wall = files
6..n-1 of P_n, pattern file = file whose content is exactly its start content, W2 on even and B4 on odd files) whose files
j-1, j, j+1 are pattern files (no wrap-around):
  (a) after every move of q, Z has no passed pawn;
  (b) if moreover files j-1..j+3 (or j-3..j+1) are pattern files, every move of q is classified L or P (never T or K).
Also reported: whether q has any capture / e.p. capture (the note's H3 says: none).
The check uses only myeng.py.   Usage: python -B run_lemma2.py N [N ...]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import myeng as M


def wall(j):
    return M.parse_file('W2') if j % 2 == 0 else M.parse_file('B4')


def run(n):
    G = M.Graph(M.P_start(n))
    pat = lambda pos, j: 0 <= j < n and j >= 6 and pos[j] == wall(j)
    cnt = dict(nodes=len(G.order), pawn_cases_a=0, moves_a=0, bad_a=0, pawn_cases_b=0, moves_b=0, bad_b=0, captures=0, flagged_children=0)
    kinds = {}
    for pos, ep in G.order:
        assert ep is None
        for Z in (0, 1):
            for j in range(7, n):
                if not (pat(pos, j - 1) and pat(pos, j) and pat(pos, j + 1)):
                    continue
                w, b = pos[j]
                mask = (w, b)[Z]
                if mask == 0 or bin(mask).count('1') != 1:
                    continue
                r = mask.bit_length()
                q = (j, r)
                mv = M.gen_moves(pos, None, Z, only=q)
                cnt['pawn_cases_a'] += 1
                for npos, ne in mv:
                    cnt['moves_a'] += 1
                    if M.passed_pawns(npos, ne, Z):
                        cnt['bad_a'] += 1
                    if sum(M.npawns(npos) for _ in (0,)) < M.npawns(pos):
                        cnt['captures'] += 1
                    if ne is not None:
                        cnt['flagged_children'] += 1
                hyp_b = all(pat(pos, x) for x in range(j - 1, j + 4)) or all(pat(pos, x) for x in range(j - 3, j + 2))
                if hyp_b:
                    cnt['pawn_cases_b'] += 1
                    cl = [x for x in M.classify(pos, None, Z) if x[1:] in set(mv)]
                    assert len(cl) == len(mv)
                    for k, npos, ne in cl:
                        cnt['moves_b'] += 1
                        kinds[(Z, r, k)] = kinds.get((Z, r, k), 0) + 1
                        if k not in 'LP':
                            cnt['bad_b'] += 1
    return cnt, kinds


for n in map(int, sys.argv[1:]):
    cnt, kinds = run(n)
    print('n=%d' % n, cnt, 'classes of the moves in (b) as (colour, rank of q, class): count', sorted(kinds.items()), flush=True)
