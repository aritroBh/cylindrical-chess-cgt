"""Run one kpsolve (niced) with an RSS watchdog that kills only its own child. usage: guard.py DIR BOARD PROMOTE CAP TAG [--frozen]"""
import subprocess, sys, time, resource
d, b, p, c, t, *extra = sys.argv[1:]
K = "/Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve"
cmd = ["nice", "-n", "15", K, "--board", b, "--ep", "on", "--promote", p, "--cap", c, "--threads", "2"] + extra
t0 = time.time(); peak = 0; killed = False
with open(f"{d}/positions.txt") as fi, open(f"{d}/out_{t}.txt", "w") as fo, open(f"{d}/err_{t}.txt", "w") as fe:
    pr = subprocess.Popen(cmd, stdin=fi, stdout=fo, stderr=fe)
    open(f"{d}/kpsolve_{t}.pid", "w").write(str(pr.pid))
    while pr.poll() is None:
        try: rss = int(subprocess.run(["ps", "-o", "rss=", "-p", str(pr.pid)], capture_output=True, text=True).stdout.strip() or 0)
        except ValueError: rss = 0
        peak = max(peak, rss)
        if rss > 3900000: pr.kill(); killed = True; break
        time.sleep(2)
    pr.wait()
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
open(f"{d}/status_{t}.txt", "w").write(f"exit {pr.returncode} killed_for_rss {killed} peak_rss_kb_sampled {peak} maxrss_children_bytes {ru.ru_maxrss} wall_s {time.time()-t0:.1f} cpu_user_s {ru.ru_utime:.1f}\n")
