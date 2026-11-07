"""The office-type audit (the orchestrator, 2026-11-07 11:56: "list for each office type the twenty most common office
names it catches"): for each office type of the local races and primaries written (data/local/, data/primary/), the
twenty office names, as filed, that it holds most often, and how many contests and names it holds in all. The
states' other offices (office_scope "state") and the legislature's primaries are left out: their office type is not
the local one. Writes data/local/office-types-top20.json; data/local/REPORT.md section 15.

    python3 -I pipeline/office_types_audit.py
"""
import collections
import glob
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = 20


def main():
    names = collections.defaultdict(collections.Counter)
    files = sorted(glob.glob(os.path.join(REPO, "data", "local", "[0-9]*", "*.json"))
                   + glob.glob(os.path.join(REPO, "data", "primary", "[0-9]*", "*.json")))
    for path in files:
        with open(path) as f:
            d = json.load(f)
        for c in d.get("contests", []):
            if c.get("office_scope") == "state" or not c.get("office_type") or c.get("level") not in ("local", "primary"):
                continue
            o = " ".join((c.get("office_as_filed") or c["office"]).upper().split())
            if o in ("STATE-LOWER", "STATE-UPPER"):
                continue
            names[c["office_type"]][o] += 1
    commit = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    out = {"about": "for each office type of the local races and primaries in data/local/ and data/primary/, the "
                    f"{TOP} office names (as filed, in capitals) it holds most often, with their counts of contests; "
                    "the states' other offices (office_scope state) and the legislature's primaries left out. "
                    "data/local/REPORT.md section 15.",
           "code_commit": commit,
           "types": {t: {"contests": sum(v.values()), "names": len(v),
                         "top": [[o, n] for o, n in sorted(v.items(), key=lambda x: (-x[1], x[0]))[:TOP]]}
                     for t, v in sorted(names.items(), key=lambda x: -sum(x[1].values()))}}
    with open(os.path.join(REPO, "data", "local", "office-types-top20.json"), "w") as f:
        json.dump(out, f, indent=1)
    for t, x in out["types"].items():
        print(f"{t}: {x['contests']:,} contests, {x['names']:,} names")


if __name__ == "__main__":
    main()
