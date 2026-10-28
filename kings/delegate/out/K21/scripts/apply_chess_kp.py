import json, sys
D = "/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K21/"
s = open(D + "EDITS.md").read()
i = s.index("- **kpsolve (C, cap 1): not obtained.**")
j = s.index("**What loopy kings do to the convention.**\n>>>>>>> NEW")
new = ("- **kpsolve (C, cap 1, real chess with promotion to Q, R, B, N): 4 contexts, 8 positions, all agree (CHECKED-2: kpsolve and the P-model solver are independent codes, and both agree with the D-model prediction).** "
"`Ka5 Pb4 Pc5 kc6 pb5` plus `Pe2 pf3`: White to move W, Black to move L, i.e. (W, L), as predicted and as in P9; plus `Pe3 pf4`: (W, L); plus `Pe2 pe3 pf3`: (L, L); plus `Pe2 pe3`: (W, W). "
"In every line the lower and upper bounds of kpsolve coincide, so the value is certified at cap 1 (13,125 layers, 1.41e9 states, 407 s on a machine at load 150, about 1.5 GB RSS; `chess/results_C.txt`). "
"Caveat: the four contexts are the ones for which the P-model and the D-model prediction already agreed; the three P-model disagreements (above) were not re-run in kpsolve (each needs another batch of the same size). "
"Reproduce: `cc -O2 -o bin/kp kings/kpsolve.c -lpthread; kings/delegate/heavy.sh bin/kp --board cyl:7x6 --ep on --promote QRBN --cap 1 --threads 2 < chess/positions_C.txt` (`scripts/run_kp_cap1.sh`).\n\n")
s = s[:i] + new + s[j:]
open(D + "EDITS.md", "w").write(s)
# summary.json
m = json.load(open(D + "summary.json"))
m["chess_kpsolve_cap1"] = {"positions": 8, "contexts": 4, "agree_with_D_prediction_and_P_model": 8,
  "results": "chess/results_C.txt", "cmd": "scripts/run_kp_cap1.sh", "states": 1413517896, "seconds": 407.1}
m["referee"] = {"file": "VERIFY.md", "verdict": "ACCEPT WITH FIXES", "fixes_applied_in_EDITS": ["F1", "F2", "F3", "F4", "F5", "sec8 bullet"], "script": "scripts/apply_referee_fixes.py"}
m["report_md"] = "not written: the Write tool refused; the proofs are the Section-3 block of EDITS.md"
json.dump(m, open(D + "summary.json", "w"), indent=1)
print("ok")
