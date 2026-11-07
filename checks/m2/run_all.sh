#!/bin/sh
# Runs the second pass's M2 checks in order (c8-c15) and writes checks/m2/OUTPUT.txt, so that every number in
# checks/M2-REPORT.md sections 5-9 is reproduced by one run (about 20 minutes). From the repository root:  sh checks/m2/run_all.sh
# The first pass's scripts (c1-c7) were written for the files of D1's #23 and D2's #24, and their run of record is the
# OUTPUT.txt of that pass, which the history holds at d11cae2 (git show d11cae2:checks/m2/OUTPUT.txt; sections 1-4
# cite its lines). They are kept as written and not rerun here: D2's #38 and later changed the files they read (c3 stops
# on a renamed input key), and c8-c13 check the same things on today's files.
# Needs python3 with numpy and scipy, and the sources fetched outside the repository (m2lib.CACHE: the
# Economist's economist_model_output.zip, 538's four checking-our-work CSVs, the Economist's us-potus-model
# README.md, and for the second pass Cha's .dta, MEDSL's Senate CSV, The Downballot's lines sheets and Klarner's
# contest file; each script says what it needs and skips what is absent).
set -e
cd "$(dirname "$0")/../.."
OUT=checks/m2/OUTPUT.txt
{
  echo "M2 checks: $(date -u +%Y-%m-%dT%H:%MZ), repository HEAD $(git rev-parse --short HEAD), python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
  echo
  for s in c8_recompute2 c9_fit2 c10_backtest2 c11_k_reading c12_control2 c13_governors2 c14_d3_recompute c15_d3_refit; do
    echo "##### $s"
    python3 -I checks/m2/$s.py 2>&1
    echo
  done
} > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
