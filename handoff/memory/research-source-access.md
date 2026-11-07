---
name: research-source-access
description: Which research hosts answer curl and which refuse (bot checks), as found by the R2 pass on 2026-11-07
metadata:
  type: reference
---

With the networked cloud env, `curl -sSL` reached FEC, Clerk of the House, govinfo, senate.gov, Crossref, NBER, Springer (abstract only), FairVote, EAC, Caltech/MIT, state court sites (AK, MN, IN, FL via Justia/Cornell) and Harvard Dataverse (API, CC0 data) on 2026-11-07.

Bot-checked or refused, recorded as unread and not worked round: Ballotpedia (CloudFront 403), NCSL, Dave Leip's Atlas, ICPSR, Election Law Blog, CanLII, BAILII, decisions.scc-csc.ca, bioguide, several state election offices (FL, GA, AZ, WI, MS, NH, KY, IA), vpap.org. TLS failures (not bypassed): elections.alaska.gov, stateofelections.pages.wm.edu. MEDSL House files sit behind a Dataverse guestbook form (not filled).

**Why:** later threads should not spend requests on hosts that refuse; the first pass (WebFetch) reached Ballotpedia and NCSL but curl cannot, so their figures are one grade lower.
**How to apply:** go to the primary statute, court, FEC or Clerk source first; see research/historical-close-races-v2.md section 0 and the unread list. [[vote-system-pointers]]
