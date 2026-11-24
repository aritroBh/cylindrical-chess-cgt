#!/usr/bin/env python
"""Train ML baselines on ChessSums: MLP/CNN and Transformer."""

import json
import random
import time
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Outcome classes: L (Left/White wins), R (Right/Black wins), N (Next player wins), P (Previous player wins)
OUTCOME_TO_IDX = {"L": 0, "R": 1, "N": 2, "P": 3}
IDX_TO_OUTCOME = {v: k for k, v in OUTCOME_TO_IDX.items()}
NUM_CLASSES = 4

# Board: max 26 files x 8 ranks (from data generation)
MAX_FILES = 26
RANKS = 8

# Piece encoding: 0=empty, 1=white pawn, 2=black pawn
NUM_CHANNELS = 3


@dataclass
class ChessSumsExample:
    id: str
    board_files: int
    cylinder: bool
    white_pawns: list[tuple[int, int]]  # (file, rank) 0-indexed files, 1-indexed ranks
    black_pawns: list[tuple[int, int]]
    outcome: str
    k: int
    heldout: list[str]


def load_split(path: Path) -> list[ChessSumsExample]:
    examples = []
    with open(path) as f:
        for line in f:
            row = json.loads(line)
            white = [(FILES.index(sq[0]), int(sq[1:])) for sq in row["white"]]
            black = [(FILES.index(sq[0]), int(sq[1:])) for sq in row["black"]]
            examples.append(ChessSumsExample(
                id=row["id"],
                board_files=row["board"]["files"],
                cylinder=row["board"]["cylinder"],
                white_pawns=white,
                black_pawns=black,
                outcome=row["outcome"],
                k=row["k"],
                heldout=row["heldout"],
            ))
    return examples


FILES = "abcdefghijklmnopqrstuvwxyz"


def encode_board_onehot(ex: ChessSumsExample) -> torch.Tensor:
    """Encode as (3, 8, files) one-hot: channels = empty, white, black."""
    files = ex.board_files
    board = torch.zeros(NUM_CHANNELS, RANKS, files, dtype=torch.float32)
    board[0, :, :] = 1.0  # empty channel
    for f, r in ex.white_pawns:
        board[0, r - 1, f] = 0.0
        board[1, r - 1, f] = 1.0
    for f, r in ex.black_pawns:
        board[0, r - 1, f] = 0.0
        board[2, r - 1, f] = 1.0
    return board


def encode_board_per_file(ex: ChessSumsExample) -> torch.Tensor:
    """Encode as (files, 8, 3) per-file tokens for transformer."""
    files = ex.board_files
    tokens = torch.zeros(files, RANKS, NUM_CHANNELS, dtype=torch.float32)
    tokens[:, :, 0] = 1.0  # empty
    for f, r in ex.white_pawns:
        tokens[f, r - 1, 0] = 0.0
        tokens[f, r - 1, 1] = 1.0
    for f, r in ex.black_pawns:
        tokens[f, r - 1, 0] = 0.0
        tokens[f, r - 1, 2] = 1.0
    return tokens


class ChessSumsDataset(Dataset):
    def __init__(self, examples: list[ChessSumsExample], model_type: str = "mlp"):
        self.examples = examples
        self.model_type = model_type

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        ex = self.examples[idx]
        if self.model_type == "mlp":
            x = encode_board_onehot(ex)
            # Pad to MAX_FILES
            if x.shape[2] < MAX_FILES:
                pad = torch.zeros(NUM_CHANNELS, RANKS, MAX_FILES - x.shape[2])
                x = torch.cat([x, pad], dim=2)
        elif self.model_type == "cnn":
            x = encode_board_onehot(ex)
            if x.shape[2] < MAX_FILES:
                pad = torch.zeros(NUM_CHANNELS, RANKS, MAX_FILES - x.shape[2])
                x = torch.cat([x, pad], dim=2)
        elif self.model_type == "transformer":
            x = encode_board_per_file(ex)
            if x.shape[0] < MAX_FILES:
                pad = torch.zeros(MAX_FILES - x.shape[0], RANKS, NUM_CHANNELS)
                x = torch.cat([x, pad], dim=0)
        else:
            raise ValueError(f"Unknown model_type: {self.model_type}")
        y = OUTCOME_TO_IDX[ex.outcome]
        heldout_str = "+".join(ex.heldout) if ex.heldout else "none"
        return x, y, ex.id, ex.k, ex.cylinder, heldout_str


# ============================================================
# Models
# ============================================================

class MLPModel(nn.Module):
    """MLP on flattened one-hot board."""
    def __init__(self, hidden_dim=512, num_layers=3, dropout=0.1):
        super().__init__()
        input_dim = NUM_CHANNELS * RANKS * MAX_FILES
        layers = []
        prev_dim = input_dim
        for _ in range(num_layers - 1):
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, NUM_CLASSES))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        # x: (B, 3, 8, MAX_FILES)
        x = x.view(x.size(0), -1)
        return self.net(x)


class CNNModel(nn.Module):
    """Small CNN on one-hot board (3, 8, files)."""
    def __init__(self, channels=64, num_layers=4, dropout=0.1):
        super().__init__()
        layers = []
        in_ch = NUM_CHANNELS
        for i in range(num_layers):
            out_ch = channels * (2 ** min(i, 2))
            layers.append(nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1))
            layers.append(nn.BatchNorm2d(out_ch))
            layers.append(nn.ReLU())
            if i % 2 == 1:
                layers.append(nn.MaxPool2d(2))
            layers.append(nn.Dropout2d(dropout))
            in_ch = out_ch
        self.features = nn.Sequential(*layers)
        # Global average pooling
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Linear(in_ch, NUM_CLASSES)

    def forward(self, x):
        # x: (B, 3, 8, MAX_FILES)
        x = self.features(x)
        x = self.pool(x).view(x.size(0), -1)
        return self.classifier(x)


class TransformerModel(nn.Module):
    """Small transformer over per-file tokens."""
    def __init__(self, d_model=128, nhead=4, num_layers=3, dim_feedforward=256, dropout=0.1):
        super().__init__()
        self.input_proj = nn.Linear(RANKS * NUM_CHANNELS, d_model)
        self.pos_embedding = nn.Parameter(torch.randn(1, MAX_FILES, d_model) * 0.02)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward,
            dropout=dropout, batch_first=True, norm_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, NUM_CLASSES)
        )

    def forward(self, x):
        # x: (B, MAX_FILES, 8, 3)
        B, F, R, C = x.shape
        x = x.view(B, F, R * C)
        x = self.input_proj(x)
        x = x + self.pos_embedding[:, :F, :]
        x = self.transformer(x)
        # Global average pooling over files
        x = x.mean(dim=1)
        return self.classifier(x)


# ============================================================
# Training & Evaluation
# ============================================================

def train_epoch(model, loader, optimizer, device, criterion):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for x, y, *_ in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * x.size(0)
        pred = logits.argmax(dim=1)
        correct += (pred == y).sum().item()
        total += x.size(0)
    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    by_k = defaultdict(lambda: {"correct": 0, "total": 0})
    by_type = defaultdict(lambda: {"correct": 0, "total": 0})
    by_heldout = defaultdict(lambda: {"correct": 0, "total": 0})
    predictions = {}
    for x, y, ids, ks, cylinders, heldouts in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        pred = logits.argmax(dim=1)
        correct += (pred == y).sum().item()
        total += x.size(0)
        for i in range(x.size(0)):
            k = ks[i].item()
            cyl = cylinders[i].item()
            held = heldouts[i]  # already a string
            by_k[k]["correct"] += (pred[i] == y[i]).item()
            by_k[k]["total"] += 1
            by_type["cylinder" if cyl else "flat"]["correct"] += (pred[i] == y[i]).item()
            by_type["cylinder" if cyl else "flat"]["total"] += 1
            by_heldout[held]["correct"] += (pred[i] == y[i]).item()
            by_heldout[held]["total"] += 1
            predictions[ids[i]] = IDX_TO_OUTCOME[pred[i].item()]
    return correct / total, by_k, by_type, by_heldout, predictions


def majority_class_baseline(examples):
    """Return majority class accuracy."""
    cnt = Counter(ex.outcome for ex in examples)
    maj = cnt.most_common(1)[0][0]
    return sum(1 for ex in examples if ex.outcome == maj) / len(examples), maj


def cgt_oracle_accuracy(examples):
    """CGT oracle is 100% by construction."""
    return 1.0


def save_predictions(predictions, path):
    with open(path, "w") as f:
        for id_, pred in predictions.items():
            f.write(json.dumps({"item": f"{id_}:outcome", "answer": pred}) + "\n")


def run_training(model_name, model, train_loader, val_loader, test_loader, test_heldout_loader, device, epochs=30, lr=1e-3):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_val_acc = 0.0
    best_state = None
    history = []

    for epoch in range(1, epochs + 1):
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, device, criterion)
        val_acc, _, _, _, _ = evaluate(model, val_loader, device)
        scheduler.step()

        history.append({"epoch": epoch, "train_loss": train_loss, "train_acc": train_acc, "val_acc": val_acc})

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        if epoch % 5 == 0 or epoch == 1:
            print(f"  Epoch {epoch:3d}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, val_acc={val_acc:.4f}")

    # Load best model
    model.load_state_dict(best_state)

    # Evaluate on test and test_heldout
    test_acc, by_k, by_type, by_heldout, test_preds = evaluate(model, test_loader, device)
    heldout_acc, heldout_by_k, heldout_by_type, heldout_by_heldout, heldout_preds = evaluate(model, test_heldout_loader, device)

    return {
        "model": model_name,
        "best_val_acc": best_val_acc,
        "test_acc": test_acc,
        "test_heldout_acc": heldout_acc,
        "test_by_k": {k: v["correct"] / v["total"] for k, v in by_k.items()},
        "test_by_type": {k: v["correct"] / v["total"] for k, v in by_type.items()},
        "test_by_heldout": {k: v["correct"] / v["total"] for k, v in by_heldout.items()},
        "heldout_by_k": {k: v["correct"] / v["total"] for k, v in heldout_by_k.items()},
        "heldout_by_type": {k: v["correct"] / v["total"] for k, v in heldout_by_type.items()},
        "heldout_by_heldout": {k: v["correct"] / v["total"] for k, v in heldout_by_heldout.items()},
        "history": history,
        "test_predictions": test_preds,
        "heldout_predictions": heldout_preds,
    }


def main():
    data_dir = Path("bench/data")
    out_dir = Path("ml/chesssums_baseline")
    out_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load data
    print("Loading data...")
    train_examples = load_split(data_dir / "train.jsonl")
    val_examples = load_split(data_dir / "val.jsonl")
    test_examples = load_split(data_dir / "test.jsonl")
    test_heldout_examples = load_split(data_dir / "test_heldout.jsonl")

    print(f"Train: {len(train_examples)}, Val: {len(val_examples)}, Test: {len(test_examples)}, Test_heldout: {len(test_heldout_examples)}")

    # Baselines
    print("\n=== Baselines ===")
    maj_acc, maj_class = majority_class_baseline(test_examples)
    print(f"Majority class ({maj_class}): {maj_acc:.4f}")
    print(f"CGT Oracle: {cgt_oracle_accuracy(test_examples):.4f}")

    maj_acc_ho, _ = majority_class_baseline(test_heldout_examples)
    print(f"Majority class (heldout): {maj_acc_ho:.4f}")

    # DataLoaders
    batch_size = 256
    num_workers = 0

    results = {}

    # --- MLP ---
    print("\n=== Training MLP ===")
    train_ds = ChessSumsDataset(train_examples, "mlp")
    val_ds = ChessSumsDataset(val_examples, "mlp")
    test_ds = ChessSumsDataset(test_examples, "mlp")
    test_ho_ds = ChessSumsDataset(test_heldout_examples, "mlp")

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_ho_loader = DataLoader(test_ho_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    mlp = MLPModel(hidden_dim=512, num_layers=3, dropout=0.1).to(device)
    results["mlp"] = run_training("MLP", mlp, train_loader, val_loader, test_loader, test_ho_loader, device, epochs=50, lr=1e-3)

    # --- CNN ---
    print("\n=== Training CNN ===")
    train_ds = ChessSumsDataset(train_examples, "cnn")
    val_ds = ChessSumsDataset(val_examples, "cnn")
    test_ds = ChessSumsDataset(test_examples, "cnn")
    test_ho_ds = ChessSumsDataset(test_heldout_examples, "cnn")

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_ho_loader = DataLoader(test_ho_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    cnn = CNNModel(channels=64, num_layers=4, dropout=0.1).to(device)
    results["cnn"] = run_training("CNN", cnn, train_loader, val_loader, test_loader, test_ho_loader, device, epochs=50, lr=1e-3)

    # --- Transformer ---
    print("\n=== Training Transformer ===")
    train_ds = ChessSumsDataset(train_examples, "transformer")
    val_ds = ChessSumsDataset(val_examples, "transformer")
    test_ds = ChessSumsDataset(test_examples, "transformer")
    test_ho_ds = ChessSumsDataset(test_heldout_examples, "transformer")

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_ho_loader = DataLoader(test_ho_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    transformer = TransformerModel(d_model=128, nhead=4, num_layers=3, dim_feedforward=256, dropout=0.1).to(device)
    results["transformer"] = run_training("Transformer", transformer, train_loader, val_loader, test_loader, test_ho_loader, device, epochs=50, lr=1e-3)

    # Save results
    with open(out_dir / "results.json", "w") as f:
        # Convert predictions to serializable format
        serializable = {}
        for k, v in results.items():
            serializable[k] = {kk: vv for kk, vv in v.items() if kk not in ("test_predictions", "heldout_predictions")}
        json.dump(serializable, f, indent=2)

    # Save predictions for scoring
    for model_name, res in results.items():
        save_predictions(res["test_predictions"], out_dir / f"preds_{model_name}_test.jsonl")
        save_predictions(res["heldout_predictions"], out_dir / f"preds_{model_name}_test_heldout.jsonl")

    print("\n=== Summary ===")
    for model_name, res in results.items():
        print(f"\n{model_name}:")
        print(f"  Val acc: {res['best_val_acc']:.4f}")
        print(f"  Test acc: {res['test_acc']:.4f}")
        print(f"  Test heldout acc: {res['test_heldout_acc']:.4f}")
        print(f"  Test by k: {res['test_by_k']}")
        print(f"  Heldout by k: {res['heldout_by_k']}")

    print("\nDone!")


if __name__ == "__main__":
    main()