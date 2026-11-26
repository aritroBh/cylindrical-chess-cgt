#!/bin/zsh
# K65: exhaustive Definition 4.8 search on flat 8x8 (ranks 2..7, at most 3 + 3 pawns on the class's files, every king
# placement).  usage: run_search.sh A|R <files> [<files> ...]   A = p45a over orientation, R = r48 (under orientation).
# Each run through heavy.sh under /usr/bin/time -l with the 2.2 GB watchdog (hrun2.sh); finished classes are skipped.
cd "$(dirname $0)/.."
impl=$1; shift
for t in "$@"; do
  tag=search/${impl}88_f${t//,/_}
  [[ -f logs/$tag.done ]] && continue
  if [[ $impl == A ]]; then zsh src/hrun2.sh $tag bin/p45a --kind flat --W 8 --H 8 --files $t --nw 3 --nb 3 --mode over
  else zsh src/hrun2.sh $tag bin/r48 enum flat:8x8 $t 3 3; fi
done
