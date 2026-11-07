#!/bin/sh
# Runs every M2 check in order (c1-c20) on the files as they stand and writes checks/m2/OUTPUT.txt, so that every
# number in checks/M2-REPORT.md is reproduced by one run (about 40 minutes). From the repository root:
#   sh checks/m2/run_all.sh
# c1-c7 are the first pass's scripts (written for D1's #23 and D2's #24); since the third pass they read today's files
# (what they read was changed, never what they test), and c17 prints where their output differs from the first pass's
# run of record, which the history holds at d11cae2 (git show d11cae2:checks/m2/OUTPUT.txt; REPORT sections 1-4 cite
# its lines, section 10.2 the differences and their causes). c8-c15 are the second pass; c16 (the near-even notes), c18
# (Louisiana 2024, #62), c19 (the deciding rounds, #60) and c20 (route (c)'s size bins, #61) the third.
# Needs python3 with numpy, scipy and openpyxl, and the sources fetched outside the repository (m2lib.CACHE: the
# Economist's economist_model_output.zip, 538's four checking-our-work CSVs, the Economist's us-potus-model
# README.md, Cha's .dta, MEDSL's Senate CSV, The Downballot's lines sheets, Klarner's contest file, and for c18
# Louisiana's four 2024 workbooks; each script says what it needs and skips what is absent).
set -e
cd "$(dirname "$0")/../.."
OUT=checks/m2/OUTPUT.txt
{
  echo "M2 checks: $(date -u +%Y-%m-%dT%H:%MZ), repository HEAD $(git rev-parse --short HEAD), python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
  echo
  for s in c1_recompute c2_college c3_chambers c4_congress c4b_president_538 c5_published c6_record c7_first_screen \
           c17_first_pass_diff \
           c8_recompute2 c9_fit2 c10_backtest2 c11_k_reading c12_control2 c13_governors2 c14_d3_recompute c15_d3_refit \
           c16_notes c18_louisiana c19_deciding_rounds c20_sizebins; do
    echo "##### $s"
    python3 -I checks/m2/$s.py 2>&1
    echo
  done
} > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
