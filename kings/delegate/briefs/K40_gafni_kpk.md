# K40: Gafni's K+P vs K values without edges (LOOPY §8 item 5, plan item A8)

Output: `kings/delegate/out/K40/` (write only there; no git; do not edit LOOPY.md, REPORT.md or anything under atlas/).

LOOPY §8 item 5 asks for Gafni's K+P vs K values without edges, starting from the cylinder KPK table in `atlas/cylinder/kpk`
(read only). Find what Gafni's values are in the literature the repository cites (search the repo for "Gafni"; no network).

1. State precisely what is to be computed: the CGT value (in the D-model / P model of LOOPY) of a lone K+P vs K component
   on a cylinder, as a function of the geometry, and how it relates to the KPK win/draw table.
2. Compute it on cyl:W×H for the boards the atlas covers (at least 6×6, 7×6, 8×6, 8×8), with kp_p `--pmodel` and ref3m,
   and compare with the atlas table (every disagreement listed).
3. Find the rule (a closed form or a short case list) and prove what you can by hand; label everything.
4. `EDITS.md` for LOOPY §8 item 5, OLD once.
