"""pipeline/intake/ms_governor_rule.py: how Mississippi elected its governor before the amendment of 2020, in the
Legislature's own text.

Written 2026-11-07 by worker D2 for the odd-year governors (the orchestrator, 12:01 UTC). Mississippi's p is not
computed for 1979-2019 on the rule this text gives (the orchestrator, 12:11: "Mark Mississippi's 1979-2019 governors
'p not computed' and cite HC 47 of 2020 with its section 140 words. Reason: under that rule, one vote can also decide
by crossing the popular majority line or by changing a House district's electoral vote, and the tie form measures
neither").

Source: Mississippi Legislature, 2020 Regular Session, House Concurrent Resolution 47, as adopted by the House and
Senate, https://billstatus.ls.state.ms.us/documents/2020/html/HC/HC0047SG.htm. It prints section 140 of the
Constitution of 1890 with the words it strikes marked <s> (and hidden), and sections 141 to 143 whole, "which reads
as follows". Read with D4's pipeline/intake/state_law.py, unchanged: the host leaves out an intermediate certificate,
and state_law.py completes the chain from the certificate's own CA Issuers address, with verification on (the
orchestrator's ruling of 2026-11-07 08:00 UTC). Justia's pages for sections 140 and 141 refused curl (HTTP 403, a
challenge) and WebFetch, and the Secretary of State's constitution page refused curl (403); neither was tried again.

Run from the repository root:  python3 -I pipeline/intake/ms_governor_rule.py
Writes CACHE/law/MS/hc47-2020-html.raw (and its .meta.json) and prints the struck and repealed words.
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import state_law as S  # noqa: E402

URL = "https://billstatus.ls.state.ms.us/documents/2020/html/HC/HC0047SG.htm"
NAME = "hc47-2020-html"
HOST = "billstatus.ls.state.ms.us"


def read():
    """(meta, the struck words of section 140, the text of section 141 as printed)."""
    S.complete_chain(HOST)
    meta, _ = S.fetch_section("MS", NAME, URL)
    with open(os.path.join(S.CACHE, S.raw_name("MS", NAME)), encoding="windows-1252", errors="replace") as f:
        raw = f.read()
    clean = lambda x: " ".join(html.unescape(re.sub(r"<[^>]+>", " ", x)).replace("\xa0", " ").split())
    struck = [clean(x) for x in re.findall(r"<s>(.*?)</s>", raw, re.S)]
    m = re.search(r"Section 141\.(.*?)</p>", raw, re.S)
    return meta, struck, clean(m.group(1)) if m else None


if __name__ == "__main__":
    meta, struck, s141 = read()
    print(meta)
    print("struck from section 140:", " | ".join(struck))
    print("section 141:", s141)
