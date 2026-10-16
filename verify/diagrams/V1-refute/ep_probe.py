"""Which claimed positions reach a double step that the model scores as an
immediate passed pawn although the opponent could capture it en passant?
Also: re-evaluate with a 'faithful e.p.' variant in which such a pawn is not
counted as passed while the e.p. right stands (it becomes passed as soon as the
right lapses, i.e. on the next move in the component that is not the capture).
Imports only indep.py (this directory).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     .venv/bin/python -I verify/diagrams/V1-refute/ep_probe.py
"""
import sys, threading
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import indep as I

EXAMPLES = []
orig_after = I.after_move


def faithful_after(W, B, ep, mover, was_double):
    if was_double and ep is not None:
        (tf, tr), (cf, cr), cap = ep
        pieces = B if cap == "B" else W
        if any((g, cr) in pieces for g in I.adj(cf)):
            pawn = (cf, cr)
            Wm = W - {pawn} if mover == "W" else W
            Bm = B - {pawn} if mover == "B" else B
            wp = I.is_passed(Wm, B, "W") if mover == "W" else I.is_passed(W, B, "W")
            bp = I.is_passed(W, Bm, "B") if mover == "B" else I.is_passed(W, B, "B")
            full_mover = I.is_passed(W, B, mover)
            if full_mover and not (wp if mover == "W" else bp):
                if len(EXAMPLES) < 6:
                    EXAMPLES.append((sorted(I.FILES[f]+str(r) for f, r in W),
                                     sorted(I.FILES[f]+str(r) for f, r in B), mover))
                I.STATS["ep_false_pass"] += 1
                if wp or bp:
                    return orig_after(W, B, ep, mover, False)
                return 0, [I.enc(*c) for c in I.split(W, B, ep)]
    return orig_after(W, B, ep, mover, was_double)


def run(label_filter=None):
    for faithful in (False, True):
        I.after_move = faithful_after if faithful else orig_after
        for rule in ("count", "mover", "opponent"):
            for split_mode in (True, False):
                I.CFG.update(ep=True, rule=rule, split=split_mode)
                print(f"--- faithful_ep={faithful} rule={rule} split={'comp' if split_mode else 'whole'}")
                for label, X, oc, alts in I.claims(True):
                    I.reset()
                    text = I.POS[label]
                    o = I.outcome(I.root_state(text))
                    if X == "AH":
                        res = "equals {k|*} k=" + str([k for k, g in I.AH.items() if I.equals(text, g)])
                    elif X is None:
                        res = f"claimed outcome {oc}"
                    else:
                        res = f"equals claimed X: {I.equals(text, X)}"
                    print(f"    {label:7s} outcome {o}  {res}   e.p.-capturable 'passed' events {I.STATS['ep_false_pass']}")
    print("examples (white, black, mover):")
    for e in EXAMPLES:
        print("   ", e)


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=run); t.start(); t.join()
