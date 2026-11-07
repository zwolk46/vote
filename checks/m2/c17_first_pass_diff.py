"""C17. The first pass's scripts (c1-c7) on today's files against their run of record (the orchestrator, 2026-11-07
10:54, the third pass's item 1): checks/m2/OUTPUT.txt as written so far by run_all.sh (c1-c7 first) against the
OUTPUT.txt of the first pass in the history at d11cae2 (`git show d11cae2:checks/m2/OUTPUT.txt`, repository HEAD
503657b). For each script: the lines identical and differing, and the differing summary lines (those that carry a count,
a largest difference, a 'beyond' or an expected/seen pair), each as '- record' / '+ today', capped. The causes are in
checks/M2-REPORT.md section 10.1; this prints the evidence. [measured]
"""
import difflib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m2lib as L  # noqa: E402

RECORD = "d11cae2"
HEAD = re.compile(r"^C\d+b?\. ")
SUMMARY = re.compile(r"compared|largest|beyond|contests:|expected|seen|national sd|units|rows rebuilt|\d+ of \d+|"
                     r"differ|reproduced|ratio|P\(seen", re.I)
CAP = 40


def sections(text):
    lines = text.split("\n")
    heads = [i for i, l in enumerate(lines) if HEAD.match(l)]
    out = {}
    for a, b in zip(heads, heads[1:] + [len(lines)]):
        sec = [l for l in lines[a:b] if not l.startswith("repository HEAD") and not l.startswith("##### ")]
        out[lines[a].split(".")[0]] = sec
    return out


def main():
    print("C17. THE FIRST PASS'S SCRIPTS ON TODAY'S FILES AGAINST THEIR RUN OF RECORD")
    print(f"repository HEAD {L.git_head()}; the run of record: {RECORD} (the first pass, repository HEAD 503657b)")
    here = os.path.join(L.ROOT, "checks", "m2", "OUTPUT.txt")
    today = sections(open(here).read()) if os.path.exists(here) else {}
    rec = sections(subprocess.run(["git", "show", f"{RECORD}:checks/m2/OUTPUT.txt"], cwd=L.ROOT, capture_output=True,
                                  text=True, check=True).stdout)
    print(f"  today's OUTPUT.txt so far holds {sorted(today, key=lambda k: (len(k), k))}; the record holds {sorted(rec, key=lambda k: (len(k), k))}")
    for k in sorted(rec, key=lambda k: (len(k), k)):
        if k not in today:
            print(f"\n  {k}: not in today's OUTPUT.txt yet (run_all.sh writes c1-c7 before this script)")
            continue
        o, n = rec[k], today[k]
        sm = difflib.SequenceMatcher(None, o, n, autojunk=False)
        same = sum(b.size for b in sm.get_matching_blocks())
        print(f"\n  {k} ({o[0][:70]}): record {len(o)} lines, today {len(n)}; identical {same}; differing: record {len(o) - same}, today {len(n) - same}")
        shown = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            for l in o[i1:i2]:
                if SUMMARY.search(l) and shown < CAP:
                    print(f"    - {l.strip()[:230]}")
                    shown += 1
            for l in n[j1:j2]:
                if SUMMARY.search(l) and shown < CAP:
                    print(f"    + {l.strip()[:230]}")
                    shown += 1
        if shown >= CAP:
            print(f"    ... (capped at {CAP} summary lines; per-contest lines are not shown)")


if __name__ == "__main__":
    main()
