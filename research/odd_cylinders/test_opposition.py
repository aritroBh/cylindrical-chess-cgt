#!/usr/bin/env python3
"""Test king opposition: K+P vs K on cylinders of various sizes."""

import subprocess
import json

ROOT = "."
KPSOLVE = f"{ROOT}/kings/kpsolve"

def name(f, r):
    return f"{chr(ord('a') + f)}{r}"

def test_kpk(W, H, wp_file, wp_rank, wk_file, wk_rank, bk_file, bk_rank, ep="on", promote="Q", cap=1):
    """Test a K+P vs K position."""
    wp = name(wp_file, wp_rank)
    wk = name(wk_file, wk_rank)
    bk = name(bk_file, bk_rank)
    
    results = {}
    for stm in ["w", "b"]:
        pos = f"P{wp} K{wk} k{bk} {stm} -"
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
    
    # Determine outcome
    wtm_exact = wtm[0] == wtm[1]
    btm_exact = btm[0] == btm[1]
    
    wtm_result = wtm[0] if wtm_exact else "?"
    btm_result = btm[0] if btm_exact else "?"
    
    return {
        "board": f"cyl:{W}x{H}",
        "wp": wp, "wk": wk, "bk": bk,
        "wtm": wtm_result, "btm": btm_result,
        "wtm_exact": wtm_exact, "btm_exact": btm_exact,
        "wtm_bounds": wtm, "btm_bounds": btm
    }

def test_opposition_positions(W, H):
    """Test key opposition positions on cyl:WxH."""
    results = []
    
    # Standard opposition test: pawn in center, kings in opposition
    # On a cylinder, "opposition" means kings on same file with one rank between,
    # or on adjacent files with same rank (diagonal opposition)
    
    center_f = W // 2
    mid_r = H // 2
    
    # Test 1: Direct opposition (same file, one rank gap)
    if mid_r + 1 <= H and mid_r - 1 >= 1:
        # White pawn at (center_f, mid_r), WK at (center_f, mid_r-1), BK at (center_f, mid_r+1)
        # But pawn and WK can't be on same square
        # Let's put pawn at mid_r, WK at mid_r-1 (behind), BK at mid_r+1 (in front)
        if mid_r - 1 >= 1 and mid_r + 1 <= H:
            res = test_kpk(W, H, center_f, mid_r, center_f, mid_r-1, center_f, mid_r+1)
            res["type"] = "direct_opposition"
            results.append(res)
    
    # Test 2: Diagonal opposition (adjacent files, same rank)
    # White pawn at (center_f, mid_r), WK at (center_f-1, mid_r), BK at (center_f+1, mid_r)
    res = test_kpk(W, H, center_f, mid_r, (center_f-1)%W, mid_r, (center_f+1)%W, mid_r)
    res["type"] = "diagonal_opposition"
    results.append(res)
    
    # Test 3: Pawn on 2nd rank, kings far away (should be win for White usually)
    res = test_kpk(W, H, center_f, 2, (center_f+2)%W, 2, (center_f-2)%W, H-1)
    res["type"] = "pawn_2nd_rank"
    results.append(res)
    
    # Test 4: Rook pawn (file 0), kings on adjacent files
    if W >= 4:
        res = test_kpk(W, H, 0, 2, 1, 2, W-1, H-1)
        res["type"] = "rook_pawn"
        results.append(res)
    
    # Test 5: Pawn near promotion, kings in opposition
    if H >= 5:
        res = test_kpk(W, H, center_f, H-1, center_f, H-2, center_f, H)
        res["type"] = "near_promotion"
        results.append(res)
    
    return results

def main():
    all_results = {}
    
    for W in range(3, 9):
        for H in range(5, 9):
            if W > 8 or H > 8: continue
            print(f"\nTesting opposition on cyl:{W}x{H}...")
            try:
                results = test_opposition_positions(W, H)
                all_results[f"cyl:{W}x{H}"] = results
                for r in results:
                    print(f"  {r['type']}: wp={r['wp']}, wk={r['wk']}, bk={r['bk']} -> WTM={r['wtm']}, BTM={r['btm']}")
            except Exception as e:
                print(f"  ERROR: {e}")
                all_results[f"cyl:{W}x{H}"] = {"error": str(e)}
    
    with open(f"{ROOT}/research/odd_cylinders/opposition_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    print("\n=== OPPOSITION SUMMARY ===")
    for board, data in all_results.items():
        if "error" in data:
            print(f"{board}: ERROR")
            continue
        parity = "odd" if int(board.split(":")[1].split("x")[0]) % 2 == 1 else "even"
        print(f"\n{board} ({parity}):")
        for r in data:
            print(f"  {r['type']}: WTM={r['wtm']}, BTM={r['btm']} (exact: {r['wtm_exact']}, {r['btm_exact']})")

if __name__ == "__main__":
    main()