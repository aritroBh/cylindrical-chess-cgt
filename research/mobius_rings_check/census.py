"""Run the requested T77 rows in order, with one solver process at a time."""
import os
import subprocess
from pathlib import Path

directory = Path(__file__).resolve().parent
rows = [(3, 3), (3, 4), (3, 5), (3, 6), (5, 5), (5, 6),
        (4, 4), (4, 5), (4, 6), (4, 7), (7, 7), (8, 8),
        (4, 8), (6, 6), (6, 7)]

if os.getpriority(os.PRIO_PROCESS, 0) < 10:
    raise SystemExit("T77 census requires nice >= 10; worker not started")
print("files pawns roots mirror star2 star2_mirror star3 star3_mirror", flush=True)
for files, pawns in rows:
    subprocess.run([directory / "check", "mobius", str(files), "enum", str(pawns)],
                   check=True, timeout=44*60+1)
