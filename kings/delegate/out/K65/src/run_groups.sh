#!/bin/zsh
# K65: run run_group.sh on every exact over group listed in a groups file (lines: <tag> | <pieces, Black king on z0> | <z1>),
# one after another; groups already done (logs/grp/<tag>_cmp.txt present) are skipped.  usage: run_groups.sh <groups file>
cd "$(dirname $0)/.."
while IFS='|' read tag G z1; do
  tag=${tag// /}; z1=${z1// /}; G=${G## }; G=${G%% }
  [[ -z $tag || -f logs/grp/${tag}_cmp.txt ]] && continue
  zsh src/run_group.sh $tag "$G" $z1
done < $1
