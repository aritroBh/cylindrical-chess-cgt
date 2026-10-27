#!/bin/zsh
# agree.sh A B : compare the W/D/L results of two result files line by line (position text + first result letter pair)
diff <(awk -F' [|] ' '{split($2,a," "); print $1" | "a[1]a[2]}' $1) <(awk -F' [|] ' '{split($2,a," "); print $1" | "a[1]a[2]}' $2) > /dev/null && echo "AGREE $1 $2 ($(wc -l < $1) lines)" || echo "DISAGREE $1 $2"
