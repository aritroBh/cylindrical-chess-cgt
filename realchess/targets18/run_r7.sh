#!/bin/zsh
# R7: solve the decisive end positions of up-second-star (W a2 b2 b6 / B a6 b7 c5) and tiny(1)
# (W a2 b2 b6 / B a6 b7 c6) exactly with kpsolve, one terminal at a time (both sides to move together),
# smallest first. It waits for the 1/8 cap-2 run to finish, so only one big kpsolve runs at a time.
#
#   zsh realchess/targets18/run_r7.sh [maxmen]      # default maxmen 9; 10-man terminals need maxmen=10
# Results go to realchess/targets18/r7/<terminal>.out; apply them with apply_kpsolve.py on each target's
# min_support_after.json.
cd "${0:A:h}/../.."
O=realchess/targets18
R=$O/r7
mkdir -p $R
maxmen=${1:-9}

# terminal blocks: a "# ... men=N ..." comment line and the two side lines after it; unique across targets
python3 - "$R" "$maxmen" $O/W_a2_b2_b6__B_a6_b7_c5/kp_needed.txt $O/W_a2_b2_b6__B_a6_b7_c6/kp_needed.txt <<'EOF'
import re, sys
R, maxmen, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
seen, blocks = set(), []
for f in files:
    lines = open(f).read().splitlines()
    for i, l in enumerate(lines):
        m = re.match(r"# (W: .*?)\s+men=(\d+)", l)
        if not m or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        blocks.append((int(m.group(2)), m.group(1), [l] + lines[i + 1:i + 3]))
blocks.sort(key=lambda b: (b[0], b[1]))
with open(f"{R}/queue.txt", "w") as q:
    for men, name, blk in blocks:
        if men > maxmen:
            continue
        slug = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
        open(f"{R}/{slug}.txt", "w").write("\n".join(blk) + "\n")
        q.write(f"{men} {slug}\n")
print(open(f"{R}/queue.txt").read(), end="")
EOF

while pgrep -f 'kpsolve --board flat:8x8 --ep on --promote Q --cap 2' >/dev/null; do sleep 60; done

while read men slug; do
  [[ -s $R/$slug.out ]] && { echo "skip $slug (done)"; continue; }
  echo "[$(date +%H:%M)] start $slug (men=$men)"
  (time nice -n 5 ./kings/kpsolve --board flat:8x8 --ep on --promote Q --cap 1 --threads 4 \
     < $R/$slug.txt > $R/$slug.out.tmp) 2> $R/$slug.err && mv $R/$slug.out.tmp $R/$slug.out
  echo "[$(date +%H:%M)] done $slug: $(grep -v '^#' $R/$slug.out 2>/dev/null | awk -F'|' '{print $2}' | tr '\n' ' ')"
  sysctl -n vm.swapusage
done < $R/queue.txt
echo "R7 queue finished"
