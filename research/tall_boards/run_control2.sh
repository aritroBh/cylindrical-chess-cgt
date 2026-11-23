#!/bin/bash
# Validation 2b: flat 5 files, R = 8, 10 pawns: documented 134,920,191 roots (2+8 2,658,896; 3+7 22,341,596; 4+6 64,796,378; 5+5 45,123,321), 75 *2, 3 *3, 0 >= *4
O=results/control; for nw in 2 3 4 5; do echo "## f5p10 5 0 8 $nw $((10-nw))" >> $O/control2.out; nice -n 15 ./tw --scan 5 0 8 $nw $((10-nw)) --maxtab 25 >> $O/control2.out; done; echo finished >> $O/control2.out
