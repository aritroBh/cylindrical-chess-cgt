import random
def nf(board, W, f): return f % W if board == 'cyl' else (f if 0 <= f < W else None)
def attacked_count(board, W, wp, bp):
    n = 0
    for (f, x) in wp:
        for df in (-1, 1):
            h = nf(board, W, f + df)
            if h is not None and (h, x + 1) in bp: n += 1; break
    return n
