#!/bin/bash
# usage: guard.sh PID  -- stops only that PID (SIGTERM) if RSS > 3.8 GB
P=$1
while kill -0 $P 2>/dev/null; do
  r=$(ps -o rss= -p $P | tr -d ' ')
  if [ -n "$r" ] && [ "$r" -gt 3800000 ]; then echo "$(date) guard: pid $P rss $r KB > limit, SIGTERM" >> logs/guard.log; kill $P; fi
  sleep 10
done
