# filter.awk -- consume frontier_split TSV on stdout, keep only "interesting" rows
# (nimber >= 2 in at least one of the settings present) and write a per-split summary.
#
# The header line names the settings, e.g.
#   #position width npawns count/epon count/epoff count/epon/aware mover/epon ...
# Columns 1..3 are position, width, npawns; columns 4..NF are "outcome,nimber"
# (nimber -1 means "not a nimber").  The DEFAULT setting is "count/epon/aware";
# it must be present in the header.
#
# usage: awk -v sumfile=OUT.summary.txt -f filter.awk < scan.tsv

BEGIN {
    FS = "\t"
    DEFAULT = "count/epon/aware"
}
NR == 1 {
    nset = NF - 3
    for (i = 4; i <= NF; i++) setname[i] = $i
    defcol = 0
    for (i = 4; i <= NF; i++) if (setname[i] == DEFAULT) defcol = i
    if (defcol == 0) { print "filter.awk: default setting missing" > "/dev/stderr"; exit 1 }
    for (i = 4; i <= NF; i++) { s2[i]=0; s3[i]=0; smax[i]=-1 }
    next
}
{
    rows++
    maxnim = -1
    for (i = 4; i <= NF; i++) {
        split($i, a, ",")
        n = a[2] + 0
        if (n == 2) s2[i]++
        if (n >= 3) s3[i]++
        if (n > smax[i]) smax[i] = n
        if (n > maxnim) maxnim = n
    }
    split($defcol, d, ",")
    dn = d[2] + 0
    dout[d[1]]++
    if (dn == 2) def2++
    if (dn >= 3) def3++
    if (dn >= 2) defhit++
    if (maxnim >= 2) { print; hits++ }
}
END {
    f = sumfile
    print "rows\t" rows > f
    print "hits_any_setting\t" hits + 0 > f
    print "default_setting\t" DEFAULT > f
    print "default_setting_hits\t" defhit + 0 > f
    print "default_star2\t" def2 + 0 > f
    print "default_star3plus\t" def3 + 0 > f
    for (i = 4; i <= NF; i++)
        printf("set\t%s\tstar2=%d\tstar3plus=%d\tmax_nimber=%d\n", setname[i], s2[i], s3[i], smax[i]) > f
    printf("outcome_hist_default\t") > f
    for (k in dout) printf("%s:%d ", k, dout[k]) > f
    printf("\n") > f
    close(f)
}
