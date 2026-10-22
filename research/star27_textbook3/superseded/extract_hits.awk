BEGIN {
    FS = "\t"
    OFS = "\t"
    print "position", "width", "npawns", "setting", "outcome", "nimber", "source_file"
}

# Skip header line
NR == 1 && FNR == 1 { next }

# For each line, check columns 4-12 (the outcome/nimber pairs)
# Column indices: 4=count/epon, 5=count/epoff, 6=count/epon/aware
# 7=mover/epon, 8=mover/epoff, 9=mover/epon/aware
# 10=opponent/epon, 11=opponent/epoff, 12=opponent/epon/aware

{
    # Check each column for nimber >= 3
    for (i = 4; i <= 12; i++) {
        split($i, a, ",")
        outcome = a[1]
        nimber = a[2] + 0  # force numeric
        if (nimber >= 3) {
            # Determine setting name
            if (i == 4) setting = "count/epon"
            else if (i == 5) setting = "count/epoff"
            else if (i == 6) setting = "count/epon/aware"
            else if (i == 7) setting = "mover/epon"
            else if (i == 8) setting = "mover/epoff"
            else if (i == 9) setting = "mover/epon/aware"
            else if (i == 10) setting = "opponent/epon"
            else if (i == 11) setting = "opponent/epoff"
            else if (i == 12) setting = "opponent/epon/aware"
            
            print $1, $2, $3, setting, outcome, nimber, FILENAME
        }
    }
}
