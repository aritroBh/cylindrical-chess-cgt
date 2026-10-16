## engine/runs/sf19_nodes.json
| limit | positions | best move wins | eval matches tablebase |
|---|---|---|---|
| nodes 1000 | 233 | 232 (100%) | 229 (98%) |
| nodes 10000 | 233 | 232 (100%) | 232 (100%) |
| nodes 100000 | 233 | 233 (100%) | 233 (100%) |
| nodes 1000000 | 233 | 233 (100%) | 233 (100%) |

Eval mismatches at nodes 1000000, by CGT value class: {'nimber': '0/17', 'switch': '0/37', 'number': '0/57', 'other-tame': '0/20', 'infinitesimal': '0/27', 'hot-BIG': '0/68', 'decided': '0/7'}
## engine/runs/sf19_depth.json
| limit | positions | best move wins | eval matches tablebase |
|---|---|---|---|
| depth 1 | 233 | 211 (91%) | 163 (70%) |
| depth 2 | 233 | 226 (97%) | 163 (70%) |
| depth 4 | 233 | 229 (98%) | 195 (84%) |
| depth 6 | 233 | 231 (99%) | 222 (95%) |
| depth 8 | 233 | 232 (100%) | 229 (98%) |
| depth 12 | 233 | 232 (100%) | 232 (100%) |

Eval mismatches at depth 12, by CGT value class: {'nimber': '0/17', 'switch': '0/37', 'number': '1/57', 'other-tame': '0/20', 'infinitesimal': '0/27', 'hot-BIG': '0/68', 'decided': '0/7'}
    ('cgt007', 'win', 'cp -3', 'number')

## Share of Stockfish 19 evaluations that match the tablebase, by CGT value class (depth sweep)

| CGT class | n | depth 1 | depth 2 | depth 4 | depth 6 | depth 8 | depth 12 |
|---|---|---|---|---|---|---|---|
| hot-BIG | 68 | 81% | 78% | 91% | 97% | 99% | 100% |
| number | 57 | 79% | 81% | 84% | 93% | 95% | 98% |
| switch | 37 | 73% | 78% | 89% | 100% | 100% | 100% |
| infinitesimal | 27 | 30% | 26% | 59% | 85% | 100% | 100% |
| other-tame | 20 | 60% | 50% | 75% | 95% | 100% | 100% |
| nimber | 17 | 53% | 65% | 88% | 100% | 100% | 100% |
| decided | 7 | 100% | 100% | 86% | 100% | 100% | 100% |
