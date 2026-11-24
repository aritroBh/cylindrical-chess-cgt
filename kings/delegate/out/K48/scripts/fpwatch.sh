#!/bin/zsh
# K48: footprint watchdog for ONE own PID (RSS undercounts when the system compresses/swaps): kill that PID if top's MEM exceeds LIMIT_MB.
pid=$1; lim=$2; log=$3
while ps -p $pid >/dev/null 2>&1; do
  m=$(top -l 1 -pid $pid -stats mem | tail -1 | tr -d ' ')
  v=${m%%[KMG+-]*}; u=${m//[0-9.+-]/}
  case $u in G*) mb=$(( ${v%.*} * 1024 ));; M*) mb=${v%.*};; *) mb=0;; esac
  if (( mb > lim )); then echo "$(date +%H:%M:%S) fpwatch: pid $pid footprint $m > ${lim} MB, killing own pid $pid" >> $log; kill $pid; break; fi
  sleep 20
done
