# T72: draw-aware model with loopy values

## 5-line summary
- Collected 13 real-draw nodes, 3 draw terminals, 6 proven drawing king moves and 17 suite draw roots (39 draws total).
- Scoring draws as 0 reproduces 0/39; as dud reproduces 21/39 (53.8%); as {on|off} reproduces 0/39.
- The dud treatment is the only one that turns the zero-valued pawn components into draws, including all 6 king-move draws.
- The {on|off} treatment is a first-player win, not a draw, so it never reproduces a draw at component level.
- Under (iii) the A2 oracle value is not pinned (bounds do not collapse); (iii) is ill-defined there because the trébuchet king group is context-dependent, not a shuttle.

## Method
Draws were collected from `realchess/results/comp_Wa2c2_Bb7d7_nodes_pure_offline.json` (13 nodes whose
`real_class` contains "draw"), the 3 draw terminals of `realchess/REPORT.md` §5, the 6 king moves with
verdict "draws" in `comp_Wa2c2_Bb7d7_kings_pure_offline.json`, and the 17 roots with `tb_root == "draw"`
in `engine/suite/results.json`. For each, the pawn component value was computed with `cylcgt` under the count
rule (`PASSED_RESPECTS_EP = True`). Reproduction was scored at component level: a treatment reproduces a real
draw iff the resulting game is a draw (dud). Treatment (i) replaces a draw by 0 (a P-game, second-player win);
(ii) by dud (both sides may pass forever); (iii) by {on|off} (a first-player win).

Reproduce: `PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python score.py`
(run from `research/draw_model/`).

## Results

| Draw set | n | (i) as 0 | (ii) as dud | (iii) as {on|off} |
|---|---:|---:|---:|---:|
| real-draw nodes | 13 | 0 | 4 | 0 |
| draw terminals | 3 | 0 | 3 | 0 |
| proven king-move draws | 6 | 0 | 6 | 0 |
| suite draw roots | 17 | 0 | 8 | 0 |
| **total** | **39** | **0** | **21** | **0** |

Reproduction rate: (i) 0%, (ii) 53.8%, (iii) 0%.

## Labels
- Draw counts and component outcomes: COMPUTED-1 (single implementation, `score.py`).
- "dud reproduces draws whose pawn value is 0": COMPUTED-1.
- "A2 oracle value not pinned under (iii)": CONJECTURE (bounds not recomputed here; inferred from the
  ill-defined shuttle assignment of the trébuchet king group).
- No claim is made that (ii) is the physically correct treatment of chess draws; only that it has the
  highest reproduction rate among the three tested.
PY