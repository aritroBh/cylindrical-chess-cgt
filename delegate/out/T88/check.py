"""Check the far-reply witness and the proposed interior TT base."""
from delegate.out.T87 import check


def main():
    rules = check.rules
    n, root = check.start("TT", 5)
    # Square 8*f+r-1 encodes chart file f, chess rank r.
    child, = (p for a, b, _, p in rules.moves(n, root, rules.WHITE)
              if (a, b) == (8*1+1, 8*1+2))
    assert rules.terminal(n, child) == rules.LIVE
    reply, = (p for a, b, _, p in rules.moves(n, child, rules.BLACK)
              if (a, b) == (8*12+3, 8*12+2))
    before, after = (rules.tokens(n, p).split() for p in (child, reply))
    assert [f for f in range(n) if before[f] != after[f]] == [12]
    assert before[14:16] == after[14:16] == ["B4", "W2"]
    print("TT(5) far reply changes file 12 alone and preserves the cut pair.")
    check.traverse("TT", 6, audit=True)
    check.whole_board("TT", 5)


if __name__ == "__main__":
    main()
