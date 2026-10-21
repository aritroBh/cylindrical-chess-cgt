"""Evaluate trained model on test set; accuracy by total length."""
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from ml.dawson.model import ValueNet, pad_position
from ml.dawson.env import outcome_strips

OUT = "/Users/aritro/Downloads/Research/Chessendgames/ml/dawson"
DATA = "/Users/aritro/Downloads/Research/Chessendgames/ml/dawson/data"

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = ValueNet(hidden=64).to(device)
model.load_state_dict(torch.load(os.path.join(OUT, "model.pt"), map_location=device))
model.eval()

# group test by total
rows = [json.loads(l) for l in open(os.path.join(DATA, "test.jsonl"))]
# bin totals
from collections import defaultdict
bins = defaultdict(list)
for r in rows:
    bins[sum(r["lengths"])].append(r)

print("total  n    acc_net  acc_majority?  base_winrate")
for T in sorted(bins):
    rs = bins[T]
    Ls=[]; Ms=[]; ys=[]
    for r in rs:
        v,m = pad_position(r["lengths"])
        Ls.append(v); Ms.append(m); ys.append(r["label"])
    Lt=torch.tensor(Ls,dtype=torch.float32).to(device)
    Mt=torch.tensor(Ms,dtype=torch.float32).to(device)
    with torch.no_grad():
        pred=(torch.sigmoid(model(Lt,Mt))>0.5).float().cpu().numpy()
    acc=float((pred==np.array(ys)).mean())
    base=float(np.mean(ys))
    print(f"{T:5d}  {len(rs):4d} {acc:.4f}   {base:.4f}")

# overall
Ls=[]; Ms=[]; ys=[]
for r in rows:
    v,m=pad_position(r["lengths"]); Ls.append(v); Ms.append(m); ys.append(r["label"])
Lt=torch.tensor(Ls,dtype=torch.float32).to(device); Mt=torch.tensor(Ms,dtype=torch.float32).to(device)
with torch.no_grad():
    pred=(torch.sigmoid(model(Lt,Mt))>0.5).float().cpu().numpy()
print("overall test acc", float((pred==np.array(ys)).mean()))

# exact rule accuracy (should be 1.0)
exact=np.array([outcome_strips(r["lengths"]) for r in rows])
print("exact rule acc", float((exact==np.array(ys)).mean()))
