"""T33 items 3-5: value of each root under every setting (cylcgt), with the C-solver nimber for comparison."""
import time
from cylcgt import pawns, cgt

ROOTS = [
    ("C3 W a2 a3 b2 / B b7 c6 c7", 3, "W: a2 a3 b2 / B: b7 c6 c7"),
    ("C4 W a4 b2 c2 / B b6 c5 d6 d7", 4, "W: a4 b2 c2 / B: b6 c5 d6 d7"),
]
SETTINGS = [
    ("count, e.p. on, aware test (default)", "count", True, True),
    ("count, e.p. on, textbook test", "count", True, False),
    ("count, e.p. off", "count", False, False),
    ("mover, e.p. on, aware test", "mover", True, True),
    ("mover, e.p. on, textbook test", "mover", True, False),
    ("mover, e.p. off", "mover", False, False),
    ("opponent, e.p. on, aware test", "opponent", True, True),
    ("opponent, e.p. on, textbook test", "opponent", True, False),
    ("opponent, e.p. off", "opponent", False, False),
]

def main():
    for label, files, text in ROOTS:
        pos = pawns.Pos.parse(text)
        print(f"== {label}")
        for name, race, ep_on, aware in SETTINGS:
            pawns.RACE_RULE = race
            pawns.PASSED_RESPECTS_EP = aware
            pawns._value.cache_clear()
            board = pawns.Board(files, 8, True, ep_on)
            t0 = time.time()
            g = pawns.value(board, pos)
            nim = next((q for q in range(16) if cgt.nimber(q) is g), None)
            print(f"  {name:38s} value {cgt.show(g):>12s}  outcome {cgt.outcome(g)}  nimber {('*'+str(nim)) if nim is not None else '-'}  ({time.time()-t0:.1f}s)", flush=True)
        print()

if __name__ == "__main__":
    main()
