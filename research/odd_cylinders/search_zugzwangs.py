#!/usr/bin/env python3
"""Search for all mutual zugzwangs of type K+P vs K+P on small cylinders."""

import subprocess
import itertools
import json

ROOT = "."
KPSOLVE = f"{ROOT}/kings/kpsolve"

def name(f, r):
    return f"{chr(ord('a') + f)}{r}"

def is_mutual_zugzwang(W, H, wp_pos, bp_pos, wk_pos, bk_pos, ep="on", promote="Q", cap=1):
    """Test if a K+P vs K+P position is a mutual zugzwang."""
    pos_wtm = f"P{wp_pos} p{bp_pos} K{wk_pos} k{bk_pos} w -"
    pos_btm = f"P{wp_pos} p{bp_pos} K{wk_pos} k{bk_pos} b -"
    
    cmd = [KPSOLVE, "--board", f"cyl:{W}x{H}", "--ep", ep, "--promote", promote, "--cap", str(cap)]
    
    try:
        out_w = subprocess.run(cmd, input=pos_wtm + "\n", capture_output=True, text=True, check=True, timeout=60)
        out_b = subprocess.run(cmd, input=pos_btm + "\n", capture_output=True, text=True, check=True, timeout=60)
        
        line_w = out_w.stdout.strip()
        line_b = out_b.stdout.strip()
        
        if "|" not in line_w or "|" not in line_b:
            return False, None, None
        
        bounds_w = line_w.split("|")[1].strip().split()
        bounds_b = line_b.split("|")[1].strip().split()
        
        # Mutual zugzwang: White to move loses (L L), Black to move loses (W W)
        is_zug = (bounds_w[0] == "L" and bounds_w[1] == "L" and 
                  bounds_b[0] == "W" and bounds_b[1] == "W")
        
        return is_zug, bounds_w, bounds_b
    except Exception as e:
        return False, None, None

def search_zugzwangs(W, H, max_positions=1000):
    """Search for mutual zugzwangs on cyl:WxH."""
    r = H // 2
    results = []
    count = 0
    
    # Pawns on same file (trébuchet-like) or adjacent files
    # White pawn on rank r, Black pawn on rank r+1 (or similar)
    # Kings on surrounding squares
    
    for wp_f in range(W):
        for bp_f in range(W):
            # Pawns should be on same or adjacent files for interaction
            # Try white pawn at rank r, black at r+1
            for wp_r in [r]:
                for bp_r in [r+1]:
                    if bp_r > H: continue
                    wp_pos = name(wp_f, wp_r)
                    bp_pos = name(bp_f, bp_r)
                    
                    # Kings on nearby squares
                    for wk_f in range(W):
                        for wk_r in range(1, H+1):
                            for bk_f in range(W):
                                for bk_r in range(1, H+1):
                                    # Skip if kings adjacent
                                    df = min((wk_f - bk_f) % W, (bk_f - wk_f) % W)
                                    dr = abs(wk_r - bk_r)
                                    if max(df, dr) <= 1:
                                        continue
                                    
                                    # Skip if king on pawn
                                    if (wk_f, wk_r) == (wp_f, wp_r) or (wk_f, wk_r) == (bp_f, bp_r):
                                        continue
                                    if (bk_f, bk_r) == (wp_f, wp_r) or (bk_f, bk_r) == (bp_f, bp_r):
                                        continue
                                    
                                    is_zug, bounds_w, bounds_b = is_mutual_zugzwang(W, H, wp_pos, bp_pos, 
                                                                                   name(wk_f, wk_r), name(bk_f, bk_r))
                                    if is_zug:
                                        results.append({
                                            "board": f"cyl:{W}x{H}",
                                            "wp": wp_pos, "bp": bp_pos,
                                            "wk": name(wk_f, wk_r), "bk": name(bk_f, bk_r),
                                            "wtm_bounds": bounds_w, "btm_bounds": bounds_b
                                        })
                                        print(f"  Found: {results[-1]}")
                                    
                                    count += 1
                                    if count >= max_positions:
                                        return results
    return results

def main():
    all_results = {}
    
    # Test odd cylinders: 3, 5, 7
    for W in [3, 5, 7]:
        for H in [5, 6, 7, 8]:
            if W > 8 or H > 8: continue
            print(f"\nSearching cyl:{W}x{H}...")
            try:
                results = search_zugzwangs(W, H, max_positions=2000)
                all_results[f"cyl:{W}x{H}"] = results
                print(f"  Found {len(results)} mutual zugzwangs")
            except Exception as e:
                print(f"  ERROR: {e}")
                all_results[f"cyl:{W}x{H}"] = {"error": str(e)}
    
    # Save
    with open(f"{ROOT}/research/odd_cylinders/zugzwang_search.json", "w") as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    main()