# Theory predictions (LOOPY.md §6) against kpsolve

Result pairs are (White to move, Black to move), from White's point of view. kpsolve: `--cap 1 --promote QRBN --ep on`, and `--cap 2` for the three P4 rows whose cap-1 bounds differed; "bounds" means the two cap bounds differ.

Two baselines: "Z = 0" reads the king group as 0 and values the rest with cylcgt (the theory's "naive convention"); "literal cylcgt" runs cylcgt.pawns.value on the whole pawn set, kings ignored (kings/results/predictions_literal_cylcgt.json).

| # | Board | Position | Theory | Z = 0 | Literal cylcgt | kpsolve | Theory holds | Literal holds |
|---|---|---|---|---|---|---|---|---|
| P1a | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` | DD | WW | WW | DD | yes | **NO** |
| P1b | cyl:7x6 | `Kc1 Pb2 Pe2 ka2 pb3 pc2 pe3 pe5` | DD | LL | LL | DD | yes | **NO** |
| P2 nothing | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5` | WW | LW | WW | WW | yes | yes |
| P2 Hm1 | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe3 pe5` | WW | LL | WW | WW | yes | yes |
| P2 H* | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe3 pe5` | WW | WL | WW | WW | yes | yes |
| P2 H*2 | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe5` | WW | WL | WW | WW | yes | yes |
| P2 H0 | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe3 pe4` | WW | LW | WW | WW | yes | yes |
| P3 nothing | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2` | LL | LW | LL | LL | yes | yes |
| P3 Hp1 | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe2 Pe4 pe5` | LL | WW | LL | LL | yes | yes |
| P3 H* | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe3 pe5` | LL | WL | LL | LL | yes | yes |
| P3 H*2 | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe2 pe5` | LL | WL | LL | LL | yes | yes |
| P3 H0 | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe3 pe4` | LL | LW | LL | LL | yes | yes |
| P4 nothing | cyl:7x6 | `Ka4 Pb3 kc3 pb4` | LW | LW | LW | LW | yes | yes |
| P4 Hm1 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe2 pe3 pe5` | LL | LL | LL | LL | yes | yes |
| P4 Hp1 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe2 Pe4 pe5` | WW | WW | WW | WW | yes | yes |
| P4 H* | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe3 pe5` | WL | WL | WL | DL | **NO** | **NO** |
| P4 H*2 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe2 pe5` | WL | WL | WL | DL | **NO** | **NO** |
| P4 H0 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe3 pe4` | LW | LW | LW | LD | **NO** | **NO** |
| P5 bare | cyl:7x6 | `Kc4 Pb5 kb6 pc5` | DW | LW | race | DW | yes | no prediction (race) |
| P5 +Hp1 | cyl:7x6 | `Kc4 Pb5 kb6 pc5 Pe2 Pe4 pe5` | WW | WW | race | WW | yes | no prediction (race) |
| P8 6-rank | cyl:7x6 | `Kc6 Pb5 kb4 pc5` | WW | LW | race | WW | yes | no prediction (race) |
| P9 | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 kc6 pb5 pf3` | WL | WW | WW | WL | yes | **NO** |
| P10 k=0 | cyl:8x6 | `Ka5 Pb4 Pc5 kc6 pb5` | WW | LW | WW | WW | yes | yes |
| P10 k=1 | cyl:8x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe3 pe5` | WW | LL | WW | WW | yes | yes |
| P10 k=2 | cyl:8x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe3 pe5 Pg2 pg3 pg5` | WW | LL | WW | WW | yes | yes |

Theory: 22 of 25 exactly determined predictions hold. Literal cylcgt: 16 of 22 (the others it scores as races at move 0).
