"""Fresh recompute of the worker's C1 pipeline, unchanged code, output redirected.

Runs sumtest.enum_positions.main() and sumtest.compare_cylcgt.main() exactly as the
reproduce command does, but with OUT pointed at an empty directory under
verify/sumtest/C1-reproduce/rerun2/data so that nothing is read from the worker's
cache.  Uses the 'fork' start method so Pool children inherit the patched OUT.

  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
    .venv/bin/python verify/sumtest/C1-reproduce/rerun2/fresh_run.py enum --jobs 12 \
    --epv off,plain,aware,plain-global,aware-global
  ... fresh_run.py compare --jobs 12
"""
import multiprocessing as mp
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEWOUT = os.path.join(HERE, "data")


def main():
    mp.set_start_method("fork", force=True)
    os.makedirs(NEWOUT, exist_ok=True)
    import sumtest.enum_positions as E
    import sumtest.compare_cylcgt as C
    E.OUT = NEWOUT
    C.OUT = NEWOUT
    which = sys.argv[1]
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    if which == "enum":
        E.main()
    elif which == "compare":
        C.main()
    else:
        raise SystemExit("enum|compare")


if __name__ == "__main__":
    main()
