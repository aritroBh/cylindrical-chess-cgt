"""Generate train/test datasets for Dawson ML task."""
import json
import os
import sys

sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from ml.dawson.env import gen_positions, outcome_strips

OUT = "/Users/aritro/Downloads/Research/Chessendgames/ml/dawson/data"
os.makedirs(OUT, exist_ok=True)


def main():
    train = gen_positions(1, 30, 400, rng_seed=42)
    # test: totals 31..80
    test = gen_positions(31, 80, 200, rng_seed=7)
    # single-strip positions for probing (all lengths 1..80)
    probe = [((n,), outcome_strips([n])) for n in range(0, 81)]

    def dump(path, rows):
        with open(path, "w") as f:
            for lengths, label in rows:
                f.write(json.dumps({"lengths": list(lengths), "label": int(label)}) + "\n")

    dump(os.path.join(OUT, "train.jsonl"), train)
    dump(os.path.join(OUT, "test.jsonl"), test)
    dump(os.path.join(OUT, "probe.jsonl"), probe)
    print("train", len(train), "test", len(test), "probe", len(probe))


if __name__ == "__main__":
    main()
