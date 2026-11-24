#!/usr/bin/env python3
"""Efficient batch search for mutual zugzwangs using kpsolve's batch mode."""

import subprocess
import json
import os

ROOT = "."
KPSOLVE = f"{ROOT}/kings/kpsolve"

def name(f, r):
    return f"{chr(ord('a') + f)}{r}"

def generate_candidate_positions(W, H):
    """Generate candidate K+P vs K+P positions that could be mutual zugzwangs."""
    r = H // 2
    positions = []
    
    # Pattern 1: 5.1 trébuchet (A-trébuchet)
    # WP at (0, r), BP at (0, r+1), WK at (W-1, r+1), BK at (1, r)
    if W >= 4:  # Need at least 4 files for non-adjacent kings
        wp = name(0, r)
        bp = name(0, r+1)
        wk = name(W-1, r+1)
        bk = name(1, r)
        positions.append((f"P{wp} p{bp} K{wk} k{bk} w -", "5.1_trébuchet"))
        positions.append((f"P{wp} p{bp} K{wk} k{bk} b -", "5.1_trébuchet"))
    
    # Pattern 2: Crossed blockade (7.2 pattern)
    # WK at (1, r+1), WP at (0, r), BK at (0, r+2), BP at (1, r+1)
    # Adjusted for cylinder
    if W >= 3 and H >= 6:
        wp = name(0, r)
        bp = name(1, r+1)
        wk = name(1, r+1)
        bk = name(0, r+2) if r+2 <= H else name(0, H)
        if r+2 <= H:
            positions.append((f"P{wp} p{bp} K{wk} k{bk} w -", "7.2_crossed"))
            positions.append((f"P{wp} p{bp} K{wk} k{bk} b -", "7.2_crossed"))
    
    # Pattern 3: 7.3 pattern
    # WK at (1, H), WP at (0, H-1), BK at (0, H-2), BP at (1, H-1)
    if W >= 3 and H >= 5:
        wp = name(0, H-1)
        bp = name(1, H-1)
        wk = name(1, H)
        bk = name(0, H-2)
        positions.append((f"P{wp} p{bp} K{wk} k{bk} w -", "7.3_pattern"))
        positions.append((f"P{wp} p{bp} K{wk} k{bk} b -", "7.3_pattern"))
    
    # Pattern 4: Mirror of 5.1 (rotated)
    # Try different file offsets
    for offset in range(W):
        wp = name(offset, r)
        bp = name(offset, r+1)
        wk = name((offset - 1) % W, r+1)
        bk = name((offset + 1) % W, r)
        # Check kings not adjacent
        df = min((((offset - 1) % W) - ((offset + 1) % W)) % W, 
                 (((offset + 1) % W) - ((offset - 1) % W)) % W)
        dr = 1
        if max(df, dr) > 1:
            positions.append((f"P{wp} p{bp} K{wk} k{bk} w -", f"5.1_rot{offset}"))
            positions.append((f"P{wp} p{bp} K{wk} k{bk} b -", f"5.1_rot{offset}"))
    
    # Pattern 5: Kings on same file, pawns on adjacent files
    for wp_f in range(W):
        for bp_f in [(wp_f + 1) % W, (wp_f - 1) % W]:
            wp = name(wp_f, r)
            bp = name(bp_f, r+1)
            # White king behind white pawn, black king behind black pawn
            wk = name(wp_f, r-1) if r-1 >= 1 else name(wp_f, 1)
            bk = name(bp_f, r+2) if r+2 <= H else name(bp_f, H)
            # Check kings not adjacent
            df = min((wk[0] - bk[0]) % W, (bk[0] - wk[0]) % W) if isinstance(wk, tuple) else min((wp_f - bp_f) % W, (bp_f - wp_f) % W)
            dr = abs((r-1 if r-1 >= 1 else 1) - (r+2 if r+2 <= H else H))
            if max(df, dr) > 1:
                positions.append((f"P{wp} p{bp} K{wk} k{bk} w -", f"adj_pawns_{wp_f}_{bp_f}"))
                positions.append((f"P{wp} p{bp} K{wk} k{bk} b -", f"adj_pawns_{wp_f}_{bp_f}"))
    
    return positions

def run_batch(board, positions, ep="on", promote="Q", cap=1):
    """Run kpsolve on a batch of positions."""
    input_text = "\n".join(positions) + "\n"
    cmd = [KPSOLVE, "--board", board, "--ep", ep, "--promote", promote, "--cap", str(cap)]
    try:
        out = subprocess.run(cmd, input=input_text, capture_output=True, text=True, check=True, timeout=300)
        results = []
        for i, line in enumerate(out.stdout.strip().split("\n")):
            if "|" in line:
                bounds = line.split("|")[1].strip().split()
                results.append((bounds[0], bounds[1]))
            else:
                results.append(("ERROR", "ERROR"))
        return results
    except subprocess.TimeoutExpired:
        return [("TIMEOUT", "TIMEOUT")] * len(positions)
    except Exception as e:
        return [(f"ERROR: {e}", f"ERROR: {e}")] * len(positions)

def main():
    all_results = {}
    
    for W in [3, 4, 5, 6, 7, 8]:
        for H in [5, 6, 7, 8]:
            if W > 8 or H > 8: continue
            board = f"cyl:{W}x{H}"
            print(f"\nTesting {board}...")
            
            positions_with_labels = generate_candidate_positions(W, H)
            positions = [p for p, _ in positions_with_labels]
            labels = [l for _, l in positions_with_labels]
            
            # Debug
            print(f"  Generated {len(positions_with_labels)} entries")
            for item in positions_with_labels[:3]:
                print(f"    {item}")
            
            if not positions:
                print(f"  No candidates")
                continue
            
            print(f"  Testing {len(positions)//2} position pairs...")
            results = run_batch(board, positions)
            
            zugzwangs = []
            for i in range(0, len(results), 2):
                if i+1 < len(results):
                    wtm = results[i]
                    btm = results[i+1]
                    label = labels[i] if i < len(labels) else "unknown"
                    
                    is_zug = (wtm[0] == "L" and wtm[1] == "L" and 
                              btm[0] == "W" and btm[1] == "W")
                    
                    if is_zug:
                        zugzwangs.append({
                            "label": label,
                            "position": positions[i],
                            "wtm": wtm,
                            "btm": btm
                        })
                        print(f"  ZUGZWANG: {label} - {positions[i]}")
            
            all_results[board] = {
                "total_tested": len(positions)//2,
                "zugzwangs_found": len(zugzwangs),
                "zugzwangs": zugzwangs
            }
            print(f"  Found {len(zugzwangs)} mutual zugzwangs")
    
    with open(f"{ROOT}/research/odd_cylinders/zugzwang_batch.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("\n=== SUMMARY ===")
    for board, data in all_results.items():
        if "error" in data:
            print(f"{board}: ERROR")
        else:
            parity = "odd" if int(board.split(":")[1].split("x")[0]) % 2 == 1 else "even"
            print(f"{board} ({parity}): {data['zugzwangs_found']}/{data['total_tested']} zugzwangs")

if __name__ == "__main__":
    main()