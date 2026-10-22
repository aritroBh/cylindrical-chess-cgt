#!/usr/bin/env python3
"""scan_wide_R.c = scan_wide.c with the variant-R change (any move clears all e.p. rights; real-chess expiry)."""
s = open('scan_wide.c').read()
old = """        uint32_t epcomp = (ep3 | ep6) ? component_files(occ, f) : 0;
        M base_ep3 = clear_component_ep(ep3, epcomp);
        M base_ep6 = clear_component_ep(ep6, epcomp);"""
new = """        /* VARIANT R: any move clears every e.p. right on the board (real-chess expiry) */
        M base_ep3 = 0, base_ep6 = 0;
        (void)component_files; (void)clear_component_ep;"""
assert old in s
open('scan_wide_R.c', 'w').write(s.replace(old, new))
