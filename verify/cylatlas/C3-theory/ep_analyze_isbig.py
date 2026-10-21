import re
def isbig(k):
    for t in re.findall(r"(\*?)(-?\d+)(?:/(\d+))?", k):
        if t[0] == "*": continue
        if abs(int(t[1])) >= 128 * (int(t[2]) if t[2] else 1): return True
    return False
