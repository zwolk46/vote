# How "one vote changes the outcome" works across electoral systems

*Research report (subagent "research-d", Sonnet 5.5), started 2026-11-06 UTC for the vote-importance site. IN PROGRESS: saved as the work goes; sections marked TODO are not yet filled.*

## 0. How this was read, and how far to trust it (read this first)

- **curl was refused for every host I tried.** One request each, spaced 3.5 s apart, to: `www.aceproject.org`, `www.idea.int`, `arxiv.org`, `www.cambridge.org`, `onlinelibrary.wiley.com`, `www.sciencedirect.com`, `academic.oup.com`, `pubs.aeaweb.org`, `mpra.ub.uni-muenchen.de`, `hal.science`, `eprints.lse.ac.uk`, `osf.io`, `www.econstor.eu`, `web.stanford.edu`, `www.electoral-reform.org.uk`, `commonslibrary.parliament.uk`. Every one ended `curl: (56) CONNECT tunnel failed, response 403`. The proxy status endpoint (`$HTTPS_PROXY/__agentproxy/status`) names the cause as "gateway answered 403 to CONNECT (policy denial or upstream failure)", and its list of recent refusals (from sibling subagents) adds `scholar.archive.org`, `core.ac.uk`, `www.semanticscholar.org`, `export.arxiv.org`, `statmodeling.stat.columbia.edu`, `www.researchgate.net`, `citeseerx.ist.psu.edu`, `www.pnas.org`, `projecteuclid.org`, `journals.sagepub.com`, `www.tandfonline.com`. This is the sandbox's egress policy (an allowlist), not the sites refusing us. I stopped at the first refusal for each host and did not route around it (no other proxy, no mirror of a blocked host through a reachable one). Per `read_documentation environment.network` the maker can widen "Allowed domains" in the cloud-environment settings; the hosts that mattered are in the unread list.
- **WebFetch was therefore used for the sources below, as the brief allows when curl is refused, and I say so here.** WebFetch returns a small model's answer to my prompt, not the page. I asked for short verbatim quotes each time. Every fact below is therefore **[stated via WebFetch]**: a source says it, per an extract I could not check against the raw page. Each such figure is one grade below a curl-read primary source; before it goes on the site it should be re-read raw.
- **WebSearch** was used only to find URLs. Its result lists include mirrors and aggregators; I did not use those as sources unless I say so.
- Tags: **[stated via WebFetch]** (source and where), **[measured]** (I computed it; how shown), **[inferred]** (my reading). Nothing is from memory; where I know a source exists and did not read it, it is in the unread list and no formula from it is given.

(Sections follow. TODO markers show unfilled parts.)

## 1. Plurality, three or more candidates
TODO

## 2. Two-round runoffs
TODO

## 3. Ranked-choice / instant-runoff voting
TODO

## 4. Proportional representation and mixed systems
TODO

## 5. Single transferable vote
TODO

## 6. Referendums and ballot measures
TODO

## 7. Primaries and multi-stage nominations
TODO

## 8. Chamber control (two-stage)
TODO

## 9. Very small electorates
TODO

## 10. Summary, open questions, unread list
TODO
