import CylChess.Claims.L5_EmptyTable
import CylChess.Claims.RootsOpen
import CylChess.Claims.L6_NotHSS
import CylChess.Dawson
import CylChess.Claims.L9_Cut
import CylChess.Claims.L8_Period

/-! The axioms the corrections after the first outside read, the ring rule (L8) and the cut lemma (L9) depend on
(read the output of `lake build`). -/

#print axioms CylChess.Claims.anyOpt_mono
#print axioms CylChess.Claims.comp_options_le
#print axioms CylChess.Claims.sum_options_le
#print axioms CylChess.Claims.wins_mono
#print axioms CylChess.Claims.isValue_mono
#print axioms CylChess.Claims.eighth_empty_table_nine_settings
#print axioms CylChess.Claims.eighth_empty_table_default_kernel
#print axioms CylChess.Claims.eighth_every_race_function
#print axioms CylChess.Claims.roots_open_AB
#print axioms CylChess.Claims.roots_open_G
#print axioms CylChess.Claims.roots_open_X
#print axioms CylChess.Claims.notHSS_way_in
#print axioms CylChess.Claims.bd_white_threat
#print axioms CylChess.Claims.fh_black_threat
#print axioms CylChess.Claims.fh_race_line
#print axioms CylChess.Dawson.g_table
#print axioms CylChess.Dawson.g_recurrence
#print axioms CylChess.Dawson.ring_win_list
#print axioms CylChess.Dawson.ring_outcome
#print axioms CylChess.Dawson.ring_win_range
#print axioms CylChess.Dawson.ring_grundy
#print axioms CylChess.Dawson.ring_structure
#print axioms CylChess.Dawson.strip_check
#print axioms CylChess.Dawson.no_promotion
#print axioms CylChess.Dawson.ring_naive_kernel
#print axioms CylChess.Dawson.strip_naive_kernel
#print axioms CylChess.Dawson.naive_native
#print axioms CylChess.Claims.Cut.fam_generator_brute
#print axioms CylChess.Claims.Cut.fam_nonvacuous
#print axioms CylChess.Claims.Cut.cut_step_3_5_6
#print axioms CylChess.Claims.Cut.cut_step_3_8_4
#print axioms CylChess.Claims.Cut.cut_step_4_5_4
#print axioms CylChess.Claims.Cut.cut_step_4_6_4
#print axioms CylChess.Claims.Cut.cut_step_4_8_3
#print axioms CylChess.Claims.Cut.cut_step_5_5_4
#print axioms CylChess.Claims.Cut.cut_step_5_6_3
#print axioms CylChess.Claims.Cut.cut_step_5_8_3
#print axioms CylChess.Claims.Cut.cut_step_6_8_2
#print axioms CylChess.Claims.Cut.cut_step_7_5_3
#print axioms CylChess.Claims.Cut.cut_step_8_5_2
#print axioms CylChess.Claims.Cut.cut_value_3_5_4
#print axioms CylChess.Claims.Cut.cut_value_4_5_3
#print axioms CylChess.Claims.Cut.cut_value_5_4_3
#print axioms CylChess.Claims.Cut.cut_value_4_6_3
#print axioms CylChess.Dawson.g_period_to_300
#print axioms CylChess.Dawson.g_last_exception
