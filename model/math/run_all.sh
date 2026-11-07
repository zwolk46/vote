#!/bin/sh
# Runs every script in model/math in order and writes their output to OUTPUT.txt.
# Usage, from the repository root or this directory:  sh model/math/run_all.sh
# Needs Python 3 with numpy. Takes a few minutes (s7 re-runs R4's Monte Carlo scripts).
cd "$(dirname "$0")" || exit 1
{
  echo "OUTPUT.txt: produced by run_all.sh on $(date -u +%Y-%m-%d) with $(python3 --version 2>&1) and numpy $(python3 -c 'import numpy; print(numpy.__version__)')"
  echo "Every number in model/MATH.md is in this file, under the section label the text cites."
  echo
  for s in s1_two_way.py s2_conventions.py s4_two_stage.py s5_claims.py s6_simple_mode.py s7_systems.py s8_history.py; do
    python3 "$s" || echo "FAILED: $s"
    echo
  done
} > OUTPUT.txt 2>&1
echo "wrote $(wc -l < OUTPUT.txt) lines to OUTPUT.txt"
