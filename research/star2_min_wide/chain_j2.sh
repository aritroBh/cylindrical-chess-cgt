#!/bin/bash
cd "$(dirname "$0")"
./run_conn.sh 5 5 2 0 2000
./run_conn.sh 6 6 4 0 2000
./run_conn.sh 5 6 4 0 16052
./run_conn.sh 6 6 3 0 14172
./run_conn.sh 5 6 3 0 23000
./run_conn.sh 5 6 3 23000 46000
