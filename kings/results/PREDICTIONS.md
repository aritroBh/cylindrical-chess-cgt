# Theory predictions (LOOPY.md §6) against kpsolve

Result pairs are (White to move, Black to move), from White's point of view. kpsolve: `--cap 1 --promote QRBN --ep on`, and `--cap 2` for the three P4 rows whose cap-1 bounds differed; "bounds" means the two cap bounds differ.

| # | Board | Position | Predicted | Naive convention | kpsolve | Prediction holds |
|---|---|---|---|---|---|---|
| P1a | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` | DD | WW | DD | yes |
| P1b | cyl:7x6 | `Kc1 Pb2 Pe2 ka2 pb3 pc2 pe3 pe5` | DD | LL | DD | yes |
| P2 nothing | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5` | WW | LW | WW | yes |
| P2 Hm1 | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe3 pe5` | WW | LL | WW | yes |
| P2 H* | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe3 pe5` | WW | WL | WW | yes |
| P2 H*2 | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe5` | WW | WL | WW | yes |
| P2 H0 | cyl:7x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe3 pe4` | WW | LW | WW | yes |
| P3 nothing | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2` | LL | LW | LL | yes |
| P3 Hp1 | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe2 Pe4 pe5` | LL | WW | LL | yes |
| P3 H* | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe3 pe5` | LL | WL | LL | yes |
| P3 H*2 | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe2 pe5` | LL | WL | LL | yes |
| P3 H0 | cyl:7x6 | `Kc1 Pb2 ka2 pb3 pc2 Pe3 pe4` | LL | LW | LL | yes |
| P4 nothing | cyl:7x6 | `Ka4 Pb3 kc3 pb4` | LW | LW | LW | yes |
| P4 Hm1 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe2 pe3 pe5` | LL | LL | LL | yes |
| P4 Hp1 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe2 Pe4 pe5` | WW | WW | WW | yes |
| P4 H* | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe3 pe5` | WL | WL | DL | **NO** |
| P4 H*2 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe2 pe5` | WL | WL | DL | **NO** |
| P4 H0 | cyl:7x6 | `Ka4 Pb3 kc3 pb4 Pe3 pe4` | LW | LW | LD | **NO** |
| P5 bare | cyl:7x6 | `Kc4 Pb5 kb6 pc5` | DW | LW | DW | yes |
| P5 +Hp1 | cyl:7x6 | `Kc4 Pb5 kb6 pc5 Pe2 Pe4 pe5` | WW | WW | WW | yes |
| P8 6-rank | cyl:7x6 | `Kc6 Pb5 kb4 pc5` | WW | LW | WW | yes |
| P9 | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 kc6 pb5 pf3` | WL | WW | WL | yes |
| P10 k=0 | cyl:8x6 | `Ka5 Pb4 Pc5 kc6 pb5` | WW | LW | not run | — |
| P10 k=1 | cyl:8x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe3 pe5` | WW | LL | not run | — |
| P10 k=2 | cyl:8x6 | `Ka5 Pb4 Pc5 kc6 pb5 Pe2 pe3 pe5 Pg2 pg3 pg5` | WW | LL | not run | — |

19 of 22 exactly determined predictions hold.
