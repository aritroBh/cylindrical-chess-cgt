# Axioms used by each theorem

From the `#print axioms` lines of a clean `lake build` (Lean 4.36.0, no Mathlib). "kernel" means the Lean kernel checked the proof;
"compiled code" means `native_decide`: the statement was evaluated by compiled Lean code and the compiler is trusted
(one axiom `<theorem>._native.native_decide.ax_1_1` per theorem). No theorem depends on `sorryAx` or on any other axiom.

| Theorem | Checked by | Standard axioms |
|---|---|---|
| `CylChess.Dawson.g_table` | kernel | propext |
| `CylChess.Dawson.g_recurrence` | kernel | propext |
| `CylChess.Dawson.ring_win_list` | kernel | propext |
| `CylChess.Dawson.ring_outcome` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Dawson.ring_win_range` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Dawson.ring_grundy` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Dawson.ring_structure` | compiled code (native_decide) | propext |
| `CylChess.Dawson.strip_check` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Dawson.no_promotion` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Dawson.ring_naive_kernel` | kernel | propext |
| `CylChess.Dawson.strip_naive_kernel` | kernel | propext |
| `CylChess.Dawson.naive_native` | compiled code (native_decide) | propext |
| `CylChess.Claims.eighth_empty_table_default_kernel` | kernel | propext |
| `CylChess.Claims.eighth_every_race_function` | compiled code (native_decide) | propext |
| `CylChess.Claims.star2seven_shape` | compiled code (native_decide) | propext |
| `CylChess.Claims.star2seven_default` | compiled code (native_decide) | propext |
| `CylChess.Claims.star2seven_not_ep_off` | compiled code (native_decide) | propext |
| `CylChess.Claims.star2seven_not_opponent` | compiled code (native_decide) | propext |
| `CylChess.Claims.star2seven_table_extra` | compiled code (native_decide) | propext |
| `CylChess.Claims.eighth_nine_settings` | compiled code (native_decide) | propext |
| `CylChess.Claims.eighth_mirror_nine_settings` | compiled code (native_decide) | propext |
| `CylChess.Claims.eighth_race_counts` | compiled code (native_decide) | propext |
| `CylChess.Claims.eighth_all_assignments` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.eighth_default_kernel` | kernel | propext |
| `CylChess.Claims.sumcounter_shape` | compiled code (native_decide) | propext |
| `CylChess.Claims.sumcounter_W` | compiled code (native_decide) | propext |
| `CylChess.Claims.sumcounter_S` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.sumcounter_S_spec_big24` | compiled code (native_decide) | propext |
| `CylChess.Claims.sumcounter_W_white_kernel` | kernel | propext |
| `CylChess.Claims.sumcounter_W_black_kernel` | kernel | propext |
| `CylChess.Claims.star2_A_white_kernel` | kernel | propext |
| `CylChess.Claims.star2_B_white_kernel` | kernel | propext |
| `CylChess.Claims.star2_B_black_kernel` | kernel | propext |
| `CylChess.Agrees.family_size` | compiled code (native_decide) | none |
| `CylChess.Agrees.search_agrees_on_family` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Agrees.search_agrees_eighth` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.fam_generator_brute` | compiled code (native_decide) | propext |
| `CylChess.Claims.Cut.fam_nonvacuous` | compiled code (native_decide) | propext |
| `CylChess.Claims.Cut.cut_step_3_5_6` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_3_8_4` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_4_5_4` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_4_6_4` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_4_8_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_5_5_4` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_5_6_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_5_8_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_6_8_2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_7_5_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_step_8_5_2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_value_3_5_4` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_value_4_5_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_value_5_4_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Cut.cut_value_4_6_3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.anyOpt_mono` | kernel | propext |
| `CylChess.Claims.comp_options_le` | kernel | propext |
| `CylChess.Claims.sum_options_le` | kernel | propext |
| `CylChess.Claims.wins_mono` | kernel | propext |
| `CylChess.Claims.isValue_mono` | kernel | propext |
| `CylChess.Claims.eighth_empty_table_nine_settings` | compiled code (native_decide) | propext |
| `CylChess.Claims.notHSS_way_in` | kernel | propext |
| `CylChess.Wide.anyOpt_true_of_mem` | kernel | propext |
| `CylChess.Wide.WH_heap_win` | kernel | propext, Quot.sound |
| `CylChess.Wide.WH_all_larger_heaps` | kernel | propext, Quot.sound |
| `CylChess.WideAgrees.passed_agrees` | compiled code (native_decide) | none |
| `CylChess.WideAgrees.family_open_size` | compiled code (native_decide) | none |
| `CylChess.WideAgrees.wide_agrees_spec` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.WideAgrees.wide_agrees_slow_rings` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.HeapsAgrees.heaps_agree_spec` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.HeapsAgrees.heaps_agree_search` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.HeapsAgrees.heaps_agree_census_spec` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.HeapsAgrees.heaps_agree_census_search` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.named_rings_are_family_members` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.ring6_shape` | compiled code (native_decide) | propext |
| `CylChess.Claims.ring6_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.ring6_ep_off_zero` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.rings_M10_O11_star2_sum` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.rings_M10_O11_star2_whole` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.star3_nine_pawns` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.star2_seven_ranks` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.c4_seven_pawn_rings` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.c6_nine_pawn_ring` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.c7_ten_pawn_rings` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.c8_ten_pawn_rings` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.c8_wall_example_is_E8` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.c11_twelve_pawn_ring_sum` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.wall_rings_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.P_rings_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.R_rings_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Q_rings_star3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Qo_rings_star3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.T_rings_star3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.S_rings_star3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.M_rings_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.oddOnePerFile_rings_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.F1_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.F2_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.F3_star2` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.TT_star3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.SS_star3` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.Mobius_controls` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.controls_cylinder` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.census_small` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.census_big` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.ring_min_C3_below` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.ring_min_C3_six` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.ring_min_C4` | compiled code (native_decide) | propext, Classical.choice, Quot.sound |
| `CylChess.Claims.roots_open_AB` | kernel | none |
| `CylChess.Claims.roots_open_G` | kernel | none |
| `CylChess.Claims.roots_open_X` | kernel | none |
| `CylChess.Claims.bd_white_threat` | kernel | none |
| `CylChess.Claims.fh_black_threat` | kernel | none |
| `CylChess.Claims.fh_race_line` | kernel | none |
| `CylChess.Claims.census_all_groups_covered` | kernel | none |
| `CylChess.Claims.census_totals` | kernel | none |
| `CylChess.Dawson.g_period_to_300` | compiled code (native_decide) | propext |
| `CylChess.Dawson.g_last_exception` | compiled code (native_decide) | propext |
