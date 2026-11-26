import CylChess.SearchWideAgrees
import CylChess.WideLemmas
import CylChess.HeapsAgrees
import CylChess.Claims.L7a_NamedRings
import CylChess.Claims.L7a_S6Rings
import CylChess.Claims.L7b_Walls
import CylChess.Claims.L7b_Star3
import CylChess.Claims.L7b_S
import CylChess.Claims.L7b_OnePerFile
import CylChess.Claims.L7b_Mobius
import CylChess.Claims.L7b_MobiusSS
import CylChess.Claims.L7b_Controls
import CylChess.Claims.L10_Census
import CylChess.Claims.L11_RingMinC3
import CylChess.Claims.L11_RingMinC4

/-! The axioms every L7 / L10 / L11 theorem depends on (read the output of `lake build`). -/

#print axioms CylChess.Wide.anyOpt_true_of_mem
#print axioms CylChess.Wide.WH_heap_win
#print axioms CylChess.Wide.WH_all_larger_heaps
#print axioms CylChess.WideAgrees.passed_agrees
#print axioms CylChess.WideAgrees.family_open_size
#print axioms CylChess.WideAgrees.wide_agrees_spec
#print axioms CylChess.WideAgrees.casesOpen_valid_count
#print axioms CylChess.WideAgrees.passed_tall
#print axioms CylChess.WideAgrees.wide_tall
#print axioms CylChess.WideAgrees.wide_agrees_slow_rings
#print axioms CylChess.HeapsAgrees.heaps_agree_spec
#print axioms CylChess.HeapsAgrees.heaps_agree_search
#print axioms CylChess.HeapsAgrees.heaps_agree_census_spec
#print axioms CylChess.HeapsAgrees.heaps_agree_census_search
#print axioms CylChess.Claims.named_rings_are_family_members
#print axioms CylChess.Claims.ring6_shape
#print axioms CylChess.Claims.ring6_star2
#print axioms CylChess.Claims.ring6_ep_off_zero
#print axioms CylChess.Claims.rings_M10_O11_star2_sum
#print axioms CylChess.Claims.rings_M10_O11_star2_whole
#print axioms CylChess.Claims.star3_nine_pawns
#print axioms CylChess.Claims.star2_seven_ranks
#print axioms CylChess.Claims.c4_seven_pawn_rings
#print axioms CylChess.Claims.c6_nine_pawn_ring
#print axioms CylChess.Claims.c7_ten_pawn_rings
#print axioms CylChess.Claims.c8_ten_pawn_rings
#print axioms CylChess.Claims.c8_wall_example_is_E8
#print axioms CylChess.Claims.c11_twelve_pawn_ring_sum
#print axioms CylChess.Claims.c11_twelve_pawn_ring_whole
#print axioms CylChess.Claims.wall_rings_star2
#print axioms CylChess.Claims.P_rings_star2
#print axioms CylChess.Claims.R_rings_star2
#print axioms CylChess.Claims.Q_rings_star3
#print axioms CylChess.Claims.Qo_rings_star3
#print axioms CylChess.Claims.T_rings_star3
#print axioms CylChess.Claims.S_rings_star3
#print axioms CylChess.Claims.M_rings_star2
#print axioms CylChess.Claims.oddOnePerFile_rings_star2
#print axioms CylChess.Claims.F1_star2
#print axioms CylChess.Claims.F2_star2
#print axioms CylChess.Claims.F3_star2
#print axioms CylChess.Claims.TT_star3
#print axioms CylChess.Claims.SS_star3
#print axioms CylChess.Claims.Mobius_controls
#print axioms CylChess.Claims.controls_cylinder
#print axioms CylChess.Claims.controls_cylinder_open
#print axioms CylChess.Claims.Mobius_controls_open
#print axioms CylChess.Claims.census_small
#print axioms CylChess.Claims.census_big
#print axioms CylChess.Claims.census_all_groups_covered
#print axioms CylChess.Claims.census_totals
#print axioms CylChess.Claims.ring_min_C3_below
#print axioms CylChess.Claims.ring_min_C3_six
#print axioms CylChess.Claims.ring_min_C4
