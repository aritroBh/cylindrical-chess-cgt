#!/bin/sh
# chain.sh waitpidfile bin jobs tag : wait until worker pid file disappears, then run jobs
cd "$(dirname "$0")"
while [ -f logs/$1 ]; do sleep 20; done
exec ./run_jobs.sh $2 $3 $4
