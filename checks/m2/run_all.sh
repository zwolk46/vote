#!/bin/sh
# Runs every M2 check in order and writes checks/m2/OUTPUT.txt, so that every number in checks/M2-REPORT.md
# is reproduced by one run. From the repository root:  sh checks/m2/run_all.sh
# Needs python3 with numpy and scipy, and the sources fetched outside the repository (m2lib.CACHE: the
# Economist's economist_model_output.zip, 538's four checking-our-work CSVs and the Economist's
# us-potus-model README.md; each script says what it needs and skips what is absent).
set -e
cd "$(dirname "$0")/../.."
OUT=checks/m2/OUTPUT.txt
{
  echo "M2 checks: $(date -u +%Y-%m-%dT%H:%MZ), repository HEAD $(git rev-parse --short HEAD), python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
  echo
  for s in c1_recompute c2_college c3_chambers c4_congress c4b_president_538 c5_published c6_record c7_first_screen; do
    python3 -I checks/m2/$s.py 2>&1
    echo
  done
} > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
