#!/usr/bin/env python3
"""A deliberately weak UCI 'engine' used only to self-test engine/run_suite.py.

It plays a uniformly random legal move (seeded by the FEN, so runs are
reproducible), using realchess/movegen.py for legality. It is NOT a chess
engine and its scores mean nothing.
"""
import hashlib
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from realchess import movegen as MG  # noqa: E402


def main():
    fen = None
    for line in sys.stdin:
        cmd = line.strip()
        if cmd == "uci":
            print("id name mock-random-mover\nid author engine/mock_uci.py\nuciok", flush=True)
        elif cmd == "isready":
            print("readyok", flush=True)
        elif cmd.startswith("position fen "):
            fen = cmd[len("position fen "):]
        elif cmd.startswith("go"):
            moves = sorted(MG.legal_uci(fen)) if fen else []
            rnd = random.Random(hashlib.sha256((fen or "").encode()).hexdigest())
            mv = rnd.choice(moves) if moves else "0000"
            print(f"info depth 1 nodes {len(moves)} score cp 0 pv {mv}", flush=True)
            print(f"bestmove {mv}", flush=True)
        elif cmd == "quit":
            return


if __name__ == "__main__":
    main()
