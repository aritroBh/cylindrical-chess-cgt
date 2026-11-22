#!/bin/sh
# usage: sh freespace.sh build/tog_review.pdf  -> pages and free space (in) in the last page's right column
P=$1; N=$(pdfinfo $P | awk '/Pages/{print $2}')
pdftotext -f $N -l $N -bbox $P - | grep "<word" | awk -F'"' -v n=$N '{x=$2; y=$8; if (x<306) {if (y>l) l=y} else {if (y>r) r=y}} END {if (r=="") r=54; printf "pages %d  left col ends %.0f pt, right col ends %.0f pt, free in right column %.2f in\n", n, l, r, (l-r)/72}'
