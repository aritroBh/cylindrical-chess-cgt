import json, sys
D = "bench/data/"
for sp in ["train", "val", "test", "test_heldout"]:
    main = {}
    for line in open(D + sp + ".jsonl"):
        r = json.loads(line); main[r["id"]] = line.strip()
    n = same = 0
    for line in open(D + sp + "_8file.jsonl"):
        r = json.loads(line); n += 1
        same += main.get(r["id"]) == line.strip()
    print(sp, "8file rows", n, "byte-identical rows in main split", same,
          "main rows with fits8", sum(json.loads(l)["fits8"] for l in main.values()))
