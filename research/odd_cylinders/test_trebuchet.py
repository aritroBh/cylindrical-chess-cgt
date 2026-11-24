#!/usr/bin/env python3
"""Test the 5.1 trébuchet pattern on cylinders of various sizes."""

import subprocess
import json

ROOT = "."
KPSOLVE = f"{ROOT}/kings/kpsolve"

def name(f, r):
    return f"{chr(ord('a') + f)}{r}"

def test_trebuchet(W, H, ep="on", promote="Q", cap=1):
    """Test the 5.1 trébuchet pattern on cyl:WxH."""
    r = H // 2
    # Pattern: WP at (0, r), BP at (0, r+1), WK at (W-1, r+1), BK at (1, r)
    wp = name(0, r)
    bp = name(0, r + 1)
    wk = name(W - 1, r + 1)
    bk = name(1, r)
    
    results = {}
    for stm in ["w", "b"]:
        pos = f"P{wp} p{bp} K{wk} k{bk} {stm} -"
        cmd = [KPSOLVE, "--board", f"cyl:{W}x{H}", "--ep", ep, "--promote", promote, "--cap", str(cap)]
        try:
            out = subprocess.run(cmd, input=pos + "\n", capture_output=True, text=True, check=True, timeout=120)
            line = out.stdout.strip()
            if "|" in line:
                bounds = line.split("|")[1].strip().split()
                results[stm] = (bounds[0], bounds[1])
            else:
                results[stm] = ("ERROR", "ERROR")
        except subprocess.TimeoutExpired:
            results[stm] = ("TIMEOUT", "TIMEOUT")
        except Exception as e:
            results[stm] = (f"ERROR: {e}", f"ERROR: {e}")
    
    # Check if mutual zugzwang: White to move -> Black wins (L), Black to move -> White wins (W)
    wtm = results.get("w", ("", ""))
    btm = results.get("b", ("", ""))
    is_zugzwang = (wtm[0] == "L" and wtm[1] == "L" and btm[0] == "W" and btm[1] == "W")
    
    return {
        "board": f"cyl:{W}x{H}",
        "pattern": f"P{wp} p{bp} K{wk} k{bk}",
        "r": r,
        "results": results,
        "is_mutual_zugzwang": is_zugzwang,
        "wtm_exact": wtm[0] == wtm[1],
        "btm_exact": btm[0] == btm[1],
    }

def main():
    results = []
    
    # Test cylinders with n=3..9 files, R=5..8 ranks
    for W in range(3, 10):
        for H in range(5, 9):
            print(f"Testing cyl:{W}x{H}...")
            try:
                res = test_trebuchet(W, H)
                results.append(res)
                print(f"  {res['pattern']}: wtm={res['results']['w']}, btm={res['results']['b']}, zugzwang={res['is_mutual_zugzwang']}")
            except Exception as e:
                print(f"  ERROR: {e}")
                results.append({"board": f"cyl:{W}x{H}", "error": str(e)})
    
    # Save results
    with open(f"{ROOT}/research/odd_cylinders/trebuchet_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary table
    print("\n=== SUMMARY ===")
    print("Board | Pattern | WTM | BTM | Zugzwang | Parity")
    print("------|---------|-----|-----|----------|-------")
    for r in results:
        if "error" in r:
            print(f"{r['board']} | ERROR: {r['error']}")
            continue
        parity = "odd" if int(r['board'].split(":")[1].split("x")[0]) % 2 == 1 else "even"
        wtm_str = f"{r['results']['w'][0]}{r['results']['w'][1]}"
        btm_str = f"{r['results']['b'][0]}{r['results']['b'][1]}"
        print(f"{r['board']} | {r['pattern']} | {wtm_str} | {btm_str} | {r['is_mutual_zugzwang']} | {parity}")

if __name__ == "__main__":
    main()