"""Value network for Dawson's chess positions (sums of strips). LSTM over strips."""
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence

MAX_STRIPS = 80
MAX_LEN = 80


class ValueNet(nn.Module):
    def __init__(self, hidden=128):
        super().__init__()
        self.hidden = hidden
        self.embed = nn.Sequential(nn.Linear(1, hidden), nn.ReLU())
        self.lstm = nn.LSTM(hidden, hidden, num_layers=1, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, 1))

    def forward(self, lengths, mask=None):
        if mask is None:
            mask = (lengths > 0).float()
        B, S = lengths.shape
        x = (lengths / MAX_LEN).unsqueeze(-1)  # (B,S,1)
        e = self.embed(x)  # (B,S,H)
        # seq lengths
        seq_lens = mask.sum(dim=1).long().clamp(min=1)
        # sort by length descending for packing
        sorted_lens, idx = torch.sort(seq_lens, descending=True)
        e_sorted = e[idx]
        packed = pack_padded_sequence(e_sorted, sorted_lens.cpu(), batch_first=True, enforce_sorted=True)
        out, (hn, cn) = self.lstm(packed)
        hn = hn[-1]  # (B,H) but sorted
        # unsort
        unsort = torch.argsort(idx)
        hn = hn[unsort]
        return self.head(hn).squeeze(-1)

    def strip_embed(self, lengths_tensor):
        x = (lengths_tensor / MAX_LEN).unsqueeze(-1)
        return self.embed(x)


def pad_position(lengths):
    v = [0.0] * MAX_STRIPS
    m = [0.0] * MAX_STRIPS
    sl = list(lengths)[:MAX_STRIPS]
    for i, L in enumerate(sl):
        v[i] = float(L)
        m[i] = 1.0
    return v, m
