#!/bin/zsh
# usage: watch.sh PID LIMIT_KB ; kills only that PID if RSS exceeds limit
while ps -p $1 >/dev/null 2>&1; do r=$(ps -o rss= -p $1); if [ -n "$r" ] && [ $r -gt $2 ]; then kill $1; echo "killed $1 at $r KB" >> watch.log; fi; sleep 3; done
