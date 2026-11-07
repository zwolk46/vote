#!/bin/sh
# Runs every M2 check in order (c1-c29) on the files as they stand and writes checks/m2/OUTPUT.txt, so that every
# number in checks/M2-REPORT.md is reproduced by one run (about half an hour). From the repository root:
#   sh checks/m2/run_all.sh
# c1-c7 are the first pass's scripts (written for D1's #23 and D2's #24); since the third pass they read today's files
# (what they read was changed, never what they test), and c17 prints where their output differs from the first pass's
# run of record, which the history holds at d11cae2 (git show d11cae2:checks/m2/OUTPUT.txt; REPORT sections 1-4 cite
# its lines, section 10.2 the differences and their causes). c8-c15 are the second pass; c16 (the near-even notes), c18
# (Louisiana 2024, #62 and #68), c19 (the deciding rounds, #60), c20 (route (c)'s size bins, #61) and c21 (New Jersey
# 2024 by county, #65 and #66), c22 (Louisiana 2023, #70), c23 (North Carolina's rounds keyed by place, #72), c24 (office
# types read by the office, #73), c25 (the odd-year governors, #74), c26 (2023 feeding the later years, #75) c27 (local questions' thresholds, #77), c28 (governor incumbency codes, #78 and #76) and c29 (D3's fixes from c24, #80) the third.
# Needs python3 with numpy, scipy and openpyxl, and the sources fetched outside the repository (m2lib.CACHE: the
# Economist's economist_model_output.zip, 538's four checking-our-work CSVs, the Economist's us-potus-model
# README.md, Cha's .dta, MEDSL's Senate CSV, The Downballot's lines sheets, Klarner's contest file, and for c18
# Louisiana's four 2024 workbooks and two statute pages, for c21 New Jersey's three Official Lists, MEDSL's 2024 New Jersey
# precinct file and four county clerks' files, for c22 Louisiana's seven 2023 workbooks and the posted multi-parish results of each
# date; each script says what it needs and skips what is absent).
set -e
cd "$(dirname "$0")/../.."
OUT=checks/m2/OUTPUT.txt
{
  echo "M2 checks: $(date -u +%Y-%m-%dT%H:%MZ), repository HEAD $(git rev-parse --short HEAD), python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
  echo
  for s in c1_recompute c2_college c3_chambers c4_congress c4b_president_538 c5_published c6_record c7_first_screen \
           c17_first_pass_diff \
           c8_recompute2 c9_fit2 c10_backtest2 c11_k_reading c12_control2 c13_governors2 c14_d3_recompute c15_d3_refit \
           c16_notes c18_louisiana c19_deciding_rounds c20_sizebins c21_new_jersey c22_louisiana_2023 c23_nc_rounds_by_place c24_office_types c25_odd_governors c26_feed_2023 c27_local_thresholds c28_governor_codes c29_fixes_c24; do
    echo "##### $s"
    python3 -I checks/m2/$s.py 2>&1 || echo "### $s exited with $?"
    echo
  done
} > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
