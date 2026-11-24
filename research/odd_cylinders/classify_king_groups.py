#!/usr/bin/env python3
"""Classify king groups as on, off, dud, or 0 (frozen) on various cylinders."""

import subprocess
import json

ROOT = "."
KPSOLVE = f"{ROOT}/kings/kpsolve"

def name(f, r):
    return f"{chr(ord('a') + f)}{r}"

def test_king_group(W, H, pieces, ep="on", promote="Q", cap=1):
    """Test a king group position (no context pawns)."""
    # pieces: list of (piece, file, rank) e.g., [('P', 0, 4), ('p', 0, 5), ('K', 7, 5), ('k', 1, 4)]
    pos_parts = []
    for piece, f, r in pieces:
        pos_parts.append(f"{piece}{name(f, r)}")
    
    results = {}
    for stm in ["w", "b"]:
        pos = " ".join(pos_parts) + f" {stm} -"
        cmd = [KPSOLVE, "--board", f"cyl:{W}x{H}", "--ep", ep, "--promote", promote, "--cap", str(cap)]
        try:
            out = subprocess.run(cmd, input=pos + "\n", capture_output=True, text=True, check=True, timeout=60)
            line = out.stdout.strip()
            if "|" in line:
                bounds = line.split("|")[1].strip().split()
                results[stm] = (bounds[0], bounds[1])
            else:
                results[stm] = ("ERROR", "ERROR")
        except Exception as e:
            results[stm] = (f"ERROR: {e}", f"ERROR: {e}")
    
    wtm = results.get("w", ("", ""))
    btm = results.get("b", ("", ""))
    
    wtm_exact = wtm[0] == wtm[1]
    btm_exact = btm[0] == btm[1]
    wtm_result = wtm[0] if wtm_exact else "?"
    btm_result = btm[0] if btm_exact else "?"
    
    # Classify according to LOOPY.md Theorem 3.4:
    # - 0 (frozen): (L, W) mutual zugzwang
    # - on: White can shuttle -> (W, W) White wins either way
    # - off: Black can shuttle -> (L, L) Black wins either way
    # - dud: Both can shuttle -> (D, D) draw either way
    # Note: Need to also check for illegal (X) or other patterns
    
    if wtm_result == "X" or btm_result == "X":
        classification = "illegal"
    elif wtm_result == "L" and btm_result == "W":
        classification = "0 (frozen)"
    elif wtm_result == "W" and btm_result == "W":
        classification = "on (White shuttle)"
    elif wtm_result == "L" and btm_result == "L":
        classification = "off (Black shuttle)"
    elif wtm_result == "D" and btm_result == "D":
        classification = "dud (both shuttle)"
    elif wtm_result == "W" and btm_result == "L":
        classification = "N (first player wins)"
    elif wtm_result == "L" and btm_result == "L":
        classification = "P (second player wins) - wait, this is off"
    else:
        classification = f"unknown ({wtm_result}, {btm_result})"
    
    return {
        "board": f"cyl:{W}x{H}",
        "pieces": pieces,
        "wtm": wtm_result, "btm": btm_result,
        "wtm_exact": wtm_exact, "btm_exact": btm_exact,
        "classification": classification,
        "wtm_bounds": wtm, "btm_bounds": btm
    }

def test_known_groups(W, H):
    """Test known king group patterns from LOOPY.md."""
    r = H // 2
    results = []
    
    # 1. 5.1 A-trébuchet (should be 0/frozen)
    if W >= 4:
        pieces = [('P', 0, r), ('p', 0, r+1), ('K', W-1, r+1), ('k', 1, r)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "5.1_trébuchet"
        results.append(res)
    
    # 2. 7.2 Crossed blockade (should be off? - frozen for Black only)
    # WK (X+1, H-2), WP (X, H-1), BK (X, H), BP (X+1, H-1)
    if W >= 3 and H >= 5:
        X = 0
        pieces = [('P', X, H-1), ('p', (X+1)%W, H-1), 
                  ('K', (X+1)%W, H-2), ('k', X, H)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "7.2_crossed"
        results.append(res)
    
    # 3. 7.3 Pattern (should be on/White win)
    # WK (X+1, H), WP (X, H-1), BK (X, H-2), BP (X+1, H-1)
    if W >= 3 and H >= 5:
        X = 0
        pieces = [('P', X, H-1), ('p', (X+1)%W, H-1),
                  ('K', (X+1)%W, H), ('k', X, H-2)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "7.3_pattern"
        results.append(res)
    
    # 4. Z_onT1 (White shuttle = on)
    # Ka5 Pb4 Pc5 / kc6 pb5 on 7x6
    # White: Ka5 (file 0, rank 5), Pb4 (file 1, rank 4), Pc5 (file 2, rank 5)
    # Black: kc6 (file 2, rank 6), pb5 (file 1, rank 5)
    if W >= 3 and H >= 6:
        pieces = [('P', 1, 4), ('P', 2, 5), ('p', 1, 5),
                  ('K', 0, 5), ('k', 2, 6)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "Z_onT1"
        results.append(res)
    
    # 5. Z_offT1 (Black shuttle = off) - mirror of Z_onT1
    if W >= 3 and H >= 6:
        pieces = [('P', 1, H-3), ('p', 1, H-4), ('p', 2, H-3),
                  ('k', 0, H-4), ('K', 2, H-5)]
        # Adjust ranks for board size
        # Original: Kc1 Pb2 / ka2 pb3 pc2 on 7x6
        # c=2, a=0, b=1
        # White: Pb2 (1,2), Black: ka2 (0,2), pb3 (1,3), pc2 (2,2), Kc1 (2,1)
        pieces = [('P', 1, 2), ('p', 0, 2), ('p', 1, 3), ('p', 2, 2),
                  ('K', 2, 1), ('k', 0, 2)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "Z_offT1"
        results.append(res)
    
    # 6. Bare kings (no pawns) - should be draw (dud-like)
    if W >= 3:
        pieces = [('K', 0, r), ('k', W//2, r)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "bare_kings"
        results.append(res)
    
    # 7. Single pawn + kings - various configurations
    # White pawn, both kings far
    if W >= 4:
        pieces = [('P', 0, 2), ('K', W-1, 2), ('k', W//2, H-1)]
        res = test_king_group(W, H, pieces)
        res["pattern"] = "single_pawn_far_kings"
        results.append(res)
    
    return results

def main():
    all_results = {}
    
    for W in range(3, 9):
        for H in range(5, 9):
            if W > 8 or H > 8: continue
            print(f"\nClassifying king groups on cyl:{W}x{H}...")
            try:
                results = test_known_groups(W, H)
                all_results[f"cyl:{W}x{H}"] = results
                for r in results:
                    print(f"  {r['pattern']}: {r['classification']} (WTM={r['wtm']}, BTM={r['btm']})")
            except Exception as e:
                print(f"  ERROR: {e}")
                all_results[f"cyl:{W}x{H}"] = {"error": str(e)}
    
    with open(f"{ROOT}/research/odd_cylinders/king_group_classification.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    # Summary by pattern
    print("\n=== CLASSIFICATION SUMMARY BY PATTERN ===")
    patterns = ["5.1_trébuchet", "7.2_crossed", "7.3_pattern", "Z_onT1", "Z_offT1", "bare_kings", "single_pawn_far_kings"]
    for pattern in patterns:
        print(f"\n{pattern}:")
        for board, data in all_results.items():
            if "error" in data: continue
            for r in data:
                if r["pattern"] == pattern:
                    parity = "odd" if int(board.split(":")[1].split("x")[0]) % 2 == 1 else "even"
                    print(f"  {board} ({parity}): {r['classification']}")

if __name__ == "__main__":
    main()