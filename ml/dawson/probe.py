"""Probe trained model's strip features against Grundy values g(n)."""
import os
import sys

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, "/Users/aritro/Downloads/Research/Chessendgames")
from ml.dawson.env import g
from ml.dawson.model import ValueNet

OUT = "/Users/aritro/Downloads/Research/Chessendgames/ml/dawson"
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = ValueNet(hidden=64).to(device)
model.load_state_dict(torch.load(os.path.join(OUT, "model.pt"), map_location=device))
model.eval()

# features for n=0..80
Ns = list(range(0, 81))
feats = []
labels = []
for n in Ns:
    t = torch.tensor([float(n)], dtype=torch.float32).to(device)
    with torch.no_grad():
        f = model.strip_embed(t).squeeze(0).cpu().numpy()
    feats.append(f)
    labels.append(g(n))
feats = np.array(feats)
labels = np.array(labels)
nclasses = int(labels.max()) + 1

# split: probe trained on n<=30, tested on n=31..80
train_idx = [i for i, n in enumerate(Ns) if 1 <= n <= 30]
test_idx = [i for i, n in enumerate(Ns) if 31 <= n <= 80]

def train_probe(idx_train, idx_test, epochs=2000):
    Xtr = torch.tensor(feats[idx_train], dtype=torch.float32).to(device)
    ytr = torch.tensor(labels[idx_train], dtype=torch.long).to(device)
    Xte = torch.tensor(feats[idx_test], dtype=torch.float32).to(device)
    yte = torch.tensor(labels[idx_test], dtype=torch.long).to(device)
    probe = nn.Linear(feats.shape[1], nclasses).to(device)
    opt = torch.optim.Adam(probe.parameters(), lr=1e-2)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        opt.zero_grad()
        logits = probe(Xtr)
        loss = loss_fn(logits, ytr)
        loss.backward()
        opt.step()
    probe.eval()
    with torch.no_grad():
        tr_acc = (probe(Xtr).argmax(1) == ytr).float().mean().item()
        te_acc = (probe(Xte).argmax(1) == yte).float().mean().item()
    return tr_acc, te_acc, probe

tr_acc, te_acc, probe = train_probe(train_idx, test_idx)
print(f"probe train (n=1..30) acc: {tr_acc:.4f}")
print(f"probe test  (n=31..80) acc: {te_acc:.4f}")
print("majority baseline (test):", float(np.mean(labels[test_idx] == np.bincount(labels[test_idx]).argmax())))

# in-sample fit on all
tr2, te2, _ = train_probe(list(range(len(Ns))), list(range(len(Ns))))
print(f"probe in-sample acc (all n): {tr2:.4f}")

# Also probe binary outcome g(n)!=0
bin_labels = (labels != 0).astype(int)
def train_bin(idx_train, idx_test, epochs=2000):
    Xtr = torch.tensor(feats[idx_train], dtype=torch.float32).to(device)
    ytr = torch.tensor(bin_labels[idx_train], dtype=torch.long).to(device)
    Xte = torch.tensor(feats[idx_test], dtype=torch.float32).to(device)
    yte = torch.tensor(bin_labels[idx_test], dtype=torch.long).to(device)
    probe = nn.Linear(feats.shape[1], 2).to(device)
    opt = torch.optim.Adam(probe.parameters(), lr=1e-2)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        opt.zero_grad()
        loss = loss_fn(probe(Xtr), ytr)
        loss.backward()
        opt.step()
    probe.eval()
    with torch.no_grad():
        tr = (probe(Xtr).argmax(1)==ytr).float().mean().item()
        te = (probe(Xte).argmax(1)==yte).float().mean().item()
    return tr, te
btr, bte = train_bin(train_idx, test_idx)
print(f"binary outcome probe train: {btr:.4f} test: {bte:.4f}")

# print g values
print("n  g(n)")
for n in range(0, 81):
    print(n, int(g(n)))
