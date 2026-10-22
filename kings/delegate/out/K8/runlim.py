"""Run a command with time and RSS limits, polling only its own macOS process tree via libproc."""
import ctypes
import json
import os
import signal
import subprocess
import sys
import time


class ProcRSS:
    """macOS libproc reader for our own process tree; the sandbox denies `ps`."""
    def __init__(self):
        if sys.platform != 'darwin':
            raise RuntimeError('this runlim copy needs macOS libproc when ps is sandboxed')
        self.lib = ctypes.CDLL('/usr/lib/system/libsystem_kernel.dylib')
        self.lib.proc_listchildpids.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        self.lib.proc_pidinfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint64,
                                          ctypes.c_void_p, ctypes.c_int]
        self.lib.proc_listchildpids.restype = ctypes.c_int
        self.lib.proc_pidinfo.restype = ctypes.c_int

    def children(self, pid):
        buf = (ctypes.c_int * 4096)()
        copied = self.lib.proc_listchildpids(pid, buf, ctypes.sizeof(buf))
        if copied < 0:
            return []
        return list(buf[:min(copied // ctypes.sizeof(ctypes.c_int), len(buf))])

    def tree(self, root):
        out, todo = {root}, [root]
        while todo:
            pid = todo.pop()
            for child in self.children(pid):
                if child > 0 and child not in out:
                    out.add(child)
                    todo.append(child)
        return out

    def resident_mb(self, pid):
        buf = ctypes.create_string_buffer(96)  # proc_taskinfo begins with virtual and resident uint64s
        if self.lib.proc_pidinfo(pid, 4, 0, buf, ctypes.sizeof(buf)) < 16:
            return None
        return ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint64))[1] / (1024 * 1024)


def main():
    label, max_s, max_mb, outfile = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    cmd = sys.argv[sys.argv.index('--') + 1:]
    t0 = time.time()
    rss_reader = ProcRSS()
    p = subprocess.Popen(cmd, start_new_session=True)
    peak_single = peak_total = 0.0
    killed = None
    while p.poll() is None:
        live = [rss_reader.resident_mb(pid) for pid in rss_reader.tree(p.pid)]
        live = [v for v in live if v is not None]
        if live:
            peak_single = max(peak_single, max(live))
            peak_total = max(peak_total, sum(live))
        if peak_single > max_mb:
            killed = 'rss'
        elif time.time() - t0 > max_s:
            killed = 'time'
        if killed:
            try:
                os.killpg(p.pid, signal.SIGTERM)  # only the session started above
            except ProcessLookupError:
                pass
            try:
                p.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            break
        time.sleep(0.2)
    rc = p.wait()
    rec = dict(label=label, rc=rc, seconds=round(time.time() - t0, 1),
               peak_single_rss_mb=round(peak_single, 1), peak_total_rss_mb=round(peak_total, 1),
               killed=killed)
    with open(outfile, 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(json.dumps(rec), flush=True)
    sys.exit(99 if killed else rc)


main()
