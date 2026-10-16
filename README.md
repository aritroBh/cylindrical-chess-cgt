# Cylindrical chess endgames: exact CGT, tablebases, learning

Start with **[RESEARCH_PLAN.md](RESEARCH_PLAN.md)**.

| Path | Contents |
|---|---|
| `prior_work/` | The June 2025 paper (`main.tex` + diagrams), unzipped from `Pionner_Research.zip` |
| `notes/audit.md` | Machine-checked audit of every pawn-only claim in the paper |
| `notes/lit_*.md`, `notes/codex_referee.md` | Literature surveys and an independent referee report |
| `cylcgt/` | Exact CGT engine plus a cylinder/flat pawn solver |
| `crosscheck/` | Independent whole-board minimax used to validate `cylcgt` |
| `tablebase/egt_prototype.c` | 4-man DTM retrograde solver for plane, cylinder and torus |

## Reproduce

Run these from this folder, one command per block.

Run the tests:

```bash
.venv/bin/python -m pytest -q tests
```

Recompute the paper's claims:

```bash
.venv/bin/python -m cylcgt.verify_paper
```

Compare the value spectra of the cylinder and the flat board:

```bash
.venv/bin/python -m cylcgt.explore --files 4 --white 2 --black 2
```

Run the independent cross-check (a few minutes):

```bash
.venv/bin/python -m crosscheck.compare
```

Build the tablebase prototype:

```bash
cc -O2 -o egt tablebase/egt_prototype.c
```

Then run it for one endgame, giving the board type and the white pieces besides the king:

```bash
./egt cyl BN
```

## Environments

- `.venv`: the solver, tests and workflows. Only the stdlib and pytest.
- `.venv-ml`: the ML track (PyTorch with the MPS backend, MLX on Metal), kept separate so that the solver
  environment stays minimal. Pinned versions are in `ml/requirements-lock.txt`.

Recreate the ML environment:

```bash
uv venv .venv-ml --python 3.12
```

Then install the pinned packages into it:

```bash
uv pip install --python .venv-ml/bin/python -r ml/requirements-lock.txt
```
