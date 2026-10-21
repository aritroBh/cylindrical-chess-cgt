"""Train value net on Dawson sums of strips."""
import json
import os
import sys

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from ml.dawson.model import ValueNet, pad_position

DATA = "/Users/aritro/Downloads/Research/Chessendgames/ml/dawson/data"
OUT = "/Users/aritro/Downloads/Research/Chessendgames/ml/dawson"


def load(path):
    Ls, Ms, ys = [], [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            v, m = pad_position(o["lengths"])
            Ls.append(v)
            Ms.append(m)
            ys.append(float(o["label"]))
    return (torch.tensor(Ls, dtype=torch.float32),
            torch.tensor(Ms, dtype=torch.float32),
            torch.tensor(ys, dtype=torch.float32))


def main():
    Xtr_l, Xtr_m, ytr = load(os.path.join(DATA, "train.jsonl"))
    Xte_l, Xte_m, yte = load(os.path.join(DATA, "test.jsonl"))

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print("device", device)

    Xtr_l = Xtr_l.to(device); Xtr_m = Xtr_m.to(device); ytr = ytr.to(device)
    Xte_l = Xte_l.to(device); Xte_m = Xte_m.to(device); yte = yte.to(device)

    ds = TensorDataset(Xtr_l, Xtr_m, ytr)
    dl = DataLoader(ds, batch_size=256, shuffle=True)

    model = ValueNet(hidden=64).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.BCEWithLogitsLoss()

    epochs = 40
    for ep in range(1, epochs + 1):
        model.train()
        tot = 0.0
        for lb, mb, yb in dl:
            opt.zero_grad()
            logits = model(lb, mb)
            loss = loss_fn(logits, yb)
            loss.backward()
            opt.step()
            tot += loss.item() * lb.size(0)
        model.eval()
        with torch.no_grad():
            tr_pred = (torch.sigmoid(model(Xtr_l, Xtr_m)) > 0.5).float()
            te_pred = (torch.sigmoid(model(Xte_l, Xte_m)) > 0.5).float()
            tr_acc = (tr_pred == ytr).float().mean().item()
            te_acc = (te_pred == yte).float().mean().item()
        if ep % 5 == 0 or ep == 1:
            print(f"epoch {ep:3d} loss {tot/len(ytr):.4f} train_acc {tr_acc:.4f} test_acc {te_acc:.4f}")

    torch.save(model.state_dict(), os.path.join(OUT, "model.pt"))
    # save test data padded for eval/probe
    np.save(os.path.join(OUT, "Xtest_len.npy"), Xte_l.cpu().numpy())
    np.save(os.path.join(OUT, "Xtest_mask.npy"), Xte_m.cpu().numpy())
    np.save(os.path.join(OUT, "ytest.npy"), yte.cpu().numpy())
    print("saved model.pt")


if __name__ == "__main__":
    main()
