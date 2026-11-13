#!/bin/sh
# Runs every M2 check in order (c1-c40) on the files as they stand and writes checks/m2/OUTPUT.txt, so that every
# number in checks/M2-REPORT.md is reproduced by one run (about 45 minutes, plus the first-time summaries of MEDSL's
# raw files, see below). From the repository root:
#   sh checks/m2/run_all.sh
# c1-c7 are the first pass's scripts (written for D1's #23 and D2's #24); since the third pass they read today's files
# (what they read was changed, never what they test), and c17 prints where their output differs from the first pass's
# run of record, which the history holds at d11cae2 (git show d11cae2:checks/m2/OUTPUT.txt; REPORT sections 1-4 cite
# its lines, section 10.2 the differences and their causes). c8-c15 are the second pass; c16 (the near-even notes), c18
# (Louisiana 2024, #62 and #68), c19 (the deciding rounds, #60), c20 (route (c)'s size bins, #61) and c21 (New Jersey
# 2024 by county, #65 and #66), c22 (Louisiana 2023, #70), c23 (North Carolina's rounds keyed by place, #72), c24 (office
# types read by the office, #73), c25 (the odd-year governors, #74), c26 (2023 feeding the later years, #75) c27 (local questions' thresholds, #77), c28 (governor incumbency codes, #78 and #76) c29 (D3's fixes from c24, #80) and c30 (each held statewide question's ballot text, #81) the third; c31 (statewide questions filed local, citations by proposer, notes at other thresholds, #82), c32 (the certified count wins, #84) and c33 (one-county titles counted whole, #85) the fourth. c31-c33 read the pages checks/m2/fetch_fourth_pass.sh fetches.
# c34 (towns, townships and counties' own questions, #86), c35 (statewide executive offices, #87) and c36 (statewide judges,
# commission seats, the lost p and New Mexico's PEC, #88) are the fifth; they read what checks/m2/fetch_fifth_pass.sh fetches
# (MEDSL's raw precinct files of 2016-2024, the State Board's results_pct files, New Mexico's pages) through
# checks/m2/m2medsl.py, which summarizes each raw file once into ~/.cache/vote-m2/fifth/derived/ (an hour or so the first
# time, for about 20 million rows; read from there after).
# c37 (statewide contests filed in pieces, the holds, North Dakota's judgeships, the over-ballot and one-seat-board rules, the
# quote URLs, #90) is the sixth; it reads what checks/m2/fetch_sixth_pass.sh fetches (Washington's and North Dakota's pages
# and exports, the 20 quote pages, the two rule pages) and MEDSL's files of the fifth cache.
# c38 (the input-volume check: every state-year's n against a count from another file, the seventh pass) reads what
# checks/m2/fetch_seventh_pass.sh fetches (MEDSL's state-level presidential file, Indiana's 2024 certified JSON, the State
# Board's 2000-2012 results_pct files) and every MEDSL raw file fetch_fifth_pass.sh lists (its lists extended again: every
# 2018, 2022 and 2024 file a p rests on), summarised once into fifth/derived/<file>.volume.json by m2medsl.volume_summary
# (about 25 minutes the first time).
# c39 (the comparison of c38's list with D3's volume test, data/local/check-volume.json) reads c38's two JSON outputs.
# c40 (the PR checks of the seventh pass: #92 New Jersey's legislatures, #93 Virginia's, #95 the volume fixes) reads the five
# New Jersey Official Lists fetch_seventh_pass.sh fetches (pdftotext -layout), Klarner's contest file, and the records at the
# four main commits around the PRs, checked out once as detached worktrees under ~/.cache/vote-m2/seventh/wt/ (git worktree).
# c47 and c48 (section 19: D3's #109, b350d5e -> b35fede) have their own run appended to OUTPUT.txt. c47 (the governors: the
# moves file and the count reconciliation, CT and NY 2018's fusion lines, IN 2024's certified count, UT 2008's state figures and
# MO's from Algara and Amlani's county returns (read by checks/m2/m2rdata.py, an RData reader of my own), WV 2012 held, the refit,
# the fusion scan with D3's rules copied, Klarner's lines) reads what fetch_eighth_pass.sh governors|aa|klarner fetches. c48 (the
# district checks' third pass: the moves file, Indiana 2016 by candidate and the 0.4% two-witness rule, the spelling pairs, the
# over-seats test on every record of 2016, 2018 and 2022, the zero-row counties, DC's ballots, New York 2018's reasons) passes
# once over every MEDSL raw file of those years (eighth/derived/p19-<file>.json, about 10 minutes the first time).
# c46 (section 18: D3's #106, the district checks' second pass, 78a82f2 -> 72d1d60: the moves file, the 284 newly tested
# records with D3's matcher copied, Indiana's 2016 archive and Utah's 2016 canvass, the Census's 2022 block equivalency files
# (D3's copies at /mnt/project-files/d3/census-sld/, copied to ~/.cache/vote-m2/eighth/src/census_sld/), Michigan's precinct
# joins, Rutland, Wayne, Arenac's official file, DC's certified PDF, Virginia's notes, D2's totals) reads what
# checks/m2/fetch_eighth_pass.sh fetches into ~/.cache/vote-m2/eighth/src/ and has its own run appended to OUTPUT.txt.
# c45 (section 17: Virginia 2023's gate whole from D3's copies of the Department's files, ~/.cache/vote-m2/eighth/src/va-2023/,
# placed by D3 in /mnt/project-files/d3/va-2023/; nothing requested from Virginia) has its own run appended to OUTPUT.txt.
# c43 (#100, D3's district checks: the moves, the 141 districts, the coverage rule from the raw files, Idaho's coarse tier,
# the flags' outcomes, the over-ballot rows; the records at 346273e and d680bd4) and c44 (#101: the held one-name records and
# Virginia 2023's local records; d680bd4 and 4831b16) are section 16's, with their own run appended to OUTPUT.txt
# (c43's section 3 summarizes each MEDSL raw file once into fifth/derived/<file>.cover.json, about 30 minutes the first time).
# The eighth pass (c41, c42): the records at 46825da, 9118755 and 2ea7c2e under ~/.cache/vote-m2/eighth/wt/, the sources in
# ~/.cache/vote-m2/eighth/src/ (index.txt: Oregon's 2024 abstract, Idaho's 2022 canvass zip, MEDSL's nj22/vt22_cleaned.csv), and
# m2medsl.ballots_summary over every 2018, 2022 and 2024 MEDSL file (derived/<file>.ballots.json, about nine minutes once).
# Needs python3 with numpy, scipy and openpyxl, and the sources fetched outside the repository (m2lib.CACHE: the
# Economist's economist_model_output.zip, 538's four checking-our-work CSVs, the Economist's us-potus-model
# README.md, Cha's .dta, MEDSL's Senate CSV, The Downballot's lines sheets, Klarner's contest file, and for c18
# Louisiana's four 2024 workbooks and two statute pages, for c21 New Jersey's three Official Lists, MEDSL's 2024 New Jersey
# precinct file and four county clerks' files, for c22 Louisiana's seven 2023 workbooks and the posted multi-parish results of each
# date; each script says what it needs and skips what is absent).
# c49 (section 20: D3's #111, bddef1ae -> 11c852dc) has its own run appended to OUTPUT.txt: the unopposed comparator at every level,
# Virginia's school boards nonpartisan by the Code (the three law.lis pages read again by fetch_eighth_pass.sh va_code), Virginia 2025's
# local contests from the Department's export (D3's copy under eighth/src/va-2025), Indiana 2018's Senate from the state's archive
# (fetch_eighth_pass.sh in_2018), the local like-race pools from the records, route (a) refitted with c40's rows and fits.
# c50 (section 20, D3's #113, 11c852dc -> 9ad2d3d5): moves-37.json against my diff, Indiana 2018's House from the archive's State
# Representative file (fetch_eighth_pass.sh in_2018_house) against the records and the six flags, route (a) refitted, the notes.
# c51 (section 21, D3's #115, e3e9b921 -> f6434077): the recount zone beside p (pipeline/local_recount.py, recount-zone.json): the
# 1,045 notes, the zone on every record with p above 0 by the rules copied, MATH 5.10 by my own quadrature, the two sources read apart
# (fetch_eighth_pass.sh recount).
# c52 (section 22, D3's #118, 30480c35 -> 4debd7e5): Singer's 2020 results as 2020's second count of the legislatures (pipeline/local_singer.py,
# check-2020-singer.json, moves-39.json): the record and the 56 files (fetch_eighth_pass.sh singer_record, singer_files), the federal gate,
# the district checks by the rules copied, Montana's canvass (mt_sos) and Maine's rows, every flag's outcome in the records, the moves.
set -e
cd "$(dirname "$0")/../.."
OUT=checks/m2/OUTPUT.txt
{
  echo "M2 checks: $(date -u +%Y-%m-%dT%H:%MZ), repository HEAD $(git rev-parse --short HEAD), python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
  echo
  for s in c1_recompute c2_college c3_chambers c4_congress c4b_president_538 c5_published c6_record c7_first_screen \
           c17_first_pass_diff \
           c8_recompute2 c9_fit2 c10_backtest2 c11_k_reading c12_control2 c13_governors2 c14_d3_recompute c15_d3_refit \
           c16_notes c18_louisiana c19_deciding_rounds c20_sizebins c21_new_jersey c22_louisiana_2023 c23_nc_rounds_by_place c24_office_types c25_odd_governors c26_feed_2023 c27_local_thresholds c28_governor_codes c29_fixes_c24 c30_ballot_texts c31_statewide_filed_local c32_certified_count c33_one_county \
           c34_towns_counties c35_statewide_officers c36_courts_commissions c37_statewide_pieces c38_input_volume c39_volume_compare c40_pr_checks \
           c41_governor_refit c42_held_totals c43_district_checks c44_one_name_va c45_va_gate c46_district_checks_2 \
           c47_governor_counts c48_district_checks_3 c49_va_local_2 c50_in_house_2018 c51_recount_zone c52_singer_2020; do
    echo "##### $s"
    python3 -I checks/m2/$s.py 2>&1 || echo "### $s exited with $?"
    echo
  done
} > "$OUT"
echo "wrote $OUT ($(wc -l < "$OUT") lines)"
