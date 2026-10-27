# T60: 4-man piece endgames on the Möbius strip, Klein bottle and projective plane

**Status: computed once (COMPUTED-1), with Bellman self-checks passing (0 errors) on every table.** Two of the
twisted boards are new; validation of the plane/cylinder/torus modes against `tablebase/replica/REPORT.md`
matches exactly (see §Validation).

## 5-line summary

- Extended `replica.c` (copied, not edited) with three twisted topologies; mobius/klein/rp2 all solve and pass
  Bellman checks.
- On all three twisted boards, almost every material is a forced win for White (KNNK is the only common draw;
  klein KRK is also a draw).
- Max mates are short: longest is mobius KBNK 20 moves; most are ≤12.
- Square colours are not well defined on any twisted board (bishops change colour across the glued edges), so the
  KBBK "opposite/same colour" split is only a coordinate-colour convenience.
- Validation: plane/cyl/torus modes reproduce every number in `tablebase/replica/REPORT.md`.

## Results (white to move)

"Won %" = share of legal white-to-move positions won. "Max DTM" in moves. "Forced win" = won from every legal
position (no draws).

### Möbius strip (file edge glues with rank flip; rank edges walls)

| Material | Legal | Won | Won % | Max DTM | Forced win? |
|---|---:|---:|---:|---:|---|
| KQK | 98,956 | 98,956 | 100.0000 | 5 | yes |
| KRK | 147,776 | 147,776 | 100.0000 | 12 | yes |
| KBBK (all) | 7,005,328 | 7,005,328 | 100.0000 | 7 | yes |
| KBBK (coord. opp. colours) | 3,566,776 | 3,566,776 | 100.0000 | 6 | yes |
| KBBK (coord. same colour) | 3,438,552 | 3,438,552 | 100.0000 | 7 | yes |
| KBNK | 8,883,740 | 8,883,740 | 100.0000 | 20 | yes |
| KNNK | 10,861,312 | 832 | 0.0077 | 1 | no (draw) |
| KRBK | 6,694,356 | 6,694,356 | 100.0000 | 7 | yes |
| KRRK | 5,974,912 | 5,974,912 | 100.0000 | 4 | yes |
| KQRK | 4,103,984 | 4,103,984 | 100.0000 | 3 | yes |
| KQQK | 2,683,320 | 2,683,320 | 100.0000 | 2 | yes |
| KRNK | 8,172,816 | 8,172,816 | 100.0000 | 11 | yes |

### Klein bottle (file edge glues with rank flip; rank edge wraps with no flip)

| Material | Legal | Won | Won % | Max DTM | Forced win? |
|---|---:|---:|---:|---:|---|
| KQK | 54,424 | 54,424 | 100.0000 | 2 | yes |
| KRK | 145,344 | 960 | 0.6605 | 1 | no (draw) |
| KBBK (all) | 2,538,784 | 2,538,784 | 100.0000 | 2 | yes |
| KBBK (coord. opp. colours) | 1,192,736 | 1,192,736 | 100.0000 | 2 | yes |
| KBBK (coord. same colour) | 1,346,048 | 1,346,048 | 100.0000 | 2 | yes |
| KBNK | 5,459,136 | 5,459,136 | 100.0000 | 6 | yes |
| KNNK | 10,129,536 | 0 | 0.0000 | 0 | no (draw) |
| KRBK | 4,228,024 | 4,228,024 | 100.0000 | 4 | yes |
| KRRK | 5,856,768 | 5,856,768 | 100.0000 | 4 | yes |
| KQRK | 2,407,440 | 2,407,440 | 100.0000 | 2 | yes |
| KQQK | 800,960 | 800,960 | 100.0000 | 1 | yes |
| KRNK | 7,786,624 | 7,786,624 | 100.0000 | 13 | yes |

### Projective plane RP² (file edge glues with rank flip; rank edge wraps with file flip)

| Material | Legal | Won | Won % | Max DTM | Forced win? |
|---|---:|---:|---:|---:|---|
| KQK | 52,512 | 52,512 | 100.0000 | 3 | yes |
| KRK | 124,848 | 124,848 | 100.0000 | 12 | yes |
| KBBK (all) | 3,286,760 | 3,286,760 | 100.0000 | 3 | yes |
| KBBK (coord. opp. colours) | 1,670,128 | 1,670,128 | 100.0000 | 3 | yes |
| KBBK (coord. same colour) | 1,616,632 | 1,616,632 | 100.0000 | 3 | yes |
| KBNK | 5,936,292 | 5,936,292 | 100.0000 | 6 | yes |
| KNNK | 10,245,072 | 936 | 0.0091 | 1 | no (draw) |
| KRBK | 3,901,992 | 3,901,992 | 100.0000 | 4 | yes |
| KRRK | 4,294,080 | 4,294,080 | 100.0000 | 3 | yes |
| KQRK | 2,028,860 | 2,028,860 | 100.0000 | 2 | yes |
| KQQK | 897,928 | 897,928 | 100.0000 | 1 | yes |
| KRNK | 6,745,660 | 6,745,660 | 100.0000 | 9 | yes |

### Square colours

On all three twisted boards the standard (f+r) mod 2 colouring is not invariant under the glued edges:
a bishop changes colour when it crosses a file-edge gluing (mobius/klein/rp2) and, for rp2, also when it
crosses a rank-edge gluing. So "bishop colour" is not well defined; the KBBK opposite/same-colour lines above
are coordinate-colour conveniences only. On the Möbius strip, both coordinate-colour cases are still forced
wins (unlike the cylinder, where same-colour bishops draw).

### Non-forced cases

- mobius KNNK: 10,860,480 draws; 51,040 of them force an immediate capture/stalemate, the rest do not.
- klein KRK: 144,384 draws; none are "only immediate capture/stalemate" (white has a move avoiding both in
  every drawn position), yet still no win.
- klein KNNK: 10,129,536 draws; 57,600 force an immediate capture/stalemate.
- rp2 KNNK: 10,244,136 draws; 49,120 force an immediate capture/stalemate.

## Validation

Plane/cylinder/torus modes reproduce `tablebase/replica/REPORT.md` exactly. Sample (white to move):

| Board | Material | Legal | Won | Won % | Max DTM |
|---|---|---:|---:|---:|---:|
| plane | KQK | 144,508 | 144,508 | 100.0000 | 10 |
| plane | KRK | 175,168 | 175,168 | 100.0000 | 16 |
| plane | KBBK opp-col | 5,008,256 | 5,007,216 | 99.9792 | 19 |
| cyl | KRK | 172,480 | 4,832 | 2.8015 | 3 |
| cyl | KBBK opp-col | 4,026,816 | 4,026,816 | 100.0000 | 14 |
| cyl | KBNK | 9,733,264 | 2,384 | 0.0245 | 2 |
| torus | KRBK | 8,222,336 | 1,792 | 0.0218 | 1 |
| torus | KRRK | 8,002,560 | 8,002,560 | 100.0000 | 7 |

All 24 tables (8 materials × 3 boards) have 0 Bellman errors and pass the applicable symmetry checks; the
position-by-position comparison with the prototype was not re-run here, but the summary numbers match.

## Implementation notes

- Source: `replica.c` (copied from `tablebase/replica/replica.c`, not edited). Twisted modes added:
  `mobius`, `klein`, `rp2`, selected by argv[1].
- Geometry: `step()` wraps with optional rank/file flips; ray generation uses a visited set so a ray stops
  when it revisits a square (required for mobius/klein/rp2 where rays are longer than 8).
- Ray arrays enlarged from 8 to 64 per ray (twisted rays can be up to 16 squares).
- No symmetries assumed for twisted boards (symmetry check skipped); Bellman check runs on every position.
- A latent buffer bug (`Child ch[64]`) was enlarged to 256; mobius queens can generate >64 moves per position.

## Reproduce

From `research/twisted_tablebases/A/`:

Build:
```bash
cc -O2 -pthread replica.c -o replica
```

Validate plane/cyl/torus (should print "passed (0 errors)" for each):
```bash
./replica plane Q check
./replica cyl R check
./replica torus RB check
```

Solve a twisted table (example):
```bash
./replica mobius BN check
./replica klein RN check   # KRNK
./replica rp2 BB check
```

Full run of all twisted tables:
```bash
for topo in mobius klein rp2; do
  for men in Q R BB BN NN RB RR QR QQ RN; do
    ./replica "$topo" "$men" check
  done
done
```

Single position probe:
```bash
./replica mobius KBNK probe "Kd3 Bh7 Na4 kh6"
```
