# Report D4 (law): every state's rule for a tie and a recount

*By worker D4, 2026-11-07 (brief `briefs/D4-data-cost-and-ties.md`, items 4 and 5). The files are `data/law/ties.json` and `data/law/recounts.json`, built by `python3 pipeline/intake/state_law.py build` from the 51 curated readings in `data/law/src/`; their fields are in `data/README.md`. Every count and table below is printed by `python3 pipeline/intake/state_law.py tables` from those two files; nothing here was typed from memory. Marks: [measured] the rule is the statute's own text, read at the state's own publisher, with a quotation that the script found word for word; [stated] the text is an agency's guide, or the Secretary of State's reprint of the code (a lower grade, named in each state's `sections`); [inferred] my reader's reading of what the text implies, said in the rule's `note`.*

## 1. What was done, and how it was checked

- **51 readings** (50 states and DC), each made by one of six readers (subagents) one section at a time through `state_law.py fetch` (curl's own user agent, at least four seconds between two requests to one host even across runs, a stop at the first refusal). **243 tie rules and 200 recount rules.**
- **Every quotation is checked by script** against the page the script fetched (`state_law.py check`): the statute's words must appear word for word, after Unicode normalisation, plain quotation marks and dashes, and one-space white space; `[...]` marks a cut. All 51 readings pass, and every rule that carries a quotation has `quotations_verified: true` (tie rules 197, recount rules 196). A rule that records an absence (none found) or an unread law carries no quotation and says which chapters were read (tie rules 46, recount rules 4).
- **Grades.** 33 states are read, 11 partly read, 7 unread. Of the tie rules that carry a quotation, 107 are [measured], 27 [stated] and 63 [inferred]; of the recount rules, 166 are [measured], 25 [stated] and 5 [inferred]. Nine states have rules that rest on an agency guide or a Secretary of State reprint: AL, AR, CA, CT, GA, IN, LA, MS, TX (section 4).
- **No state was read through a compilation.** The orchestrator's ruling of 07:21 UTC allowed Justia and Cornell LII ("via compilation") where a state's own site refuses or serves only a script shell. Justia answered HTTP 403 to the first request in each of the five readings that tried it (AL, GA, NH, PA, TX); every other reader stopped there and made no request to that host (Mississippi did not need it: a plain PDF of the code was on the state's own site). Cornell LII: its pages for AL and GA do not carry the state's code, and a search of it found no Texas Election Code page; it was not otherwise tried.
- **Hawaii** was read at `data.capitol.hawaii.gov`, the Legislature's own document host, after `www.capitol.hawaii.gov` answered HTTP 403. The orchestrator ruled (07:48 UTC) that the data host counts as the Legislature's own publisher; the reading says so.

## 2. What a tie does, by kind of office

The brief: p counts a tie as half a decision where a tie goes to a lot; where the law sends it to a new election, a runoff, the legislature or a party committee, p means something else. The counts below say where each holds. A state can appear in several cells of one column, for different offices or on different conditions (North Carolina sends a general-election tie to a new election when more than 5,000 voters cast ballots in the item, and to a method of random selection at 5,000 or fewer).

### Resolution by kind of office (states with at least one rule of that resolution)

| Resolution | federal | presidential-electors | statewide | state-legislative | local | primary | measure |
|---|---|---|---|---|---|---|---|
| lot | 18 | 17 | 15 | 18 | 20 | 17 | 1 |
| new election | 7 | 1 | 6 | 7 | 5 |  | 1 |
| legislature | 1 | 4 | 18 | 2 | 2 |  |  |
| runoff | 4 | 1 | 3 | 4 | 7 | 8 |  |
| recount, then lot | 5 | 4 | 5 | 7 | 6 | 9 |  |
| recount, then new election | 3 | 2 | 2 | 2 | 1 | 1 |  |
| party committee |  |  |  | 1 |  | 10 |  |
| court |  |  |  |  | 1 |  |  |
| other | 3 | 1 | 3 | 2 | 3 | 6 | 6 |
| none found | 3 | 9 | 1 | 2 | 3 | 3 | 28 |
| unread | 12 | 12 | 13 | 11 | 12 | 9 | 12 |

### States by kind of office: what the rules found say

| Kind | Only a lot (or recount, then lot) | Another rule for some office or condition | Lot and a part unread | Searched, none found | Not read | No rule recorded |
|---|---|---|---|---|---|---|
| federal | 19 | 17 | 1 | 3 | 11 | 0 |
| presidential-electors | 20 | 9 | 0 | 9 | 12 | 1 |
| statewide | 11 | 26 | 1 | 1 | 12 | 0 |
| state-legislative | 21 | 18 | 0 | 1 | 11 | 0 |
| local | 22 | 17 | 0 | 2 | 10 | 0 |
| primary | 19 | 22 | 0 | 1 | 9 | 0 |
| measure | 0 | 7 | 0 | 28 | 12 | 4 |

How to read the second table. "Only a lot" means the rules found for that kind are a lot, or a recount and then a lot, and nothing else. "Lot and a part unread" is Mississippi, whose rule for the kind is a lot and whose Constitution (the Governor's tie) is unread. "Not read" means every rule recorded for that kind is "unread". Presidential electors: Texas has no entry. Ballot measures: Massachusetts, Maryland, Michigan and Texas have no entry; 28 states were searched and no provision was found (an absence in the chapters named in each reading, not a finding that no rule exists).

**Where a tie is not a lot.** A new election (federal: DE, IA, IN, LA, MA, NC, RI); a runoff (federal: AR, GA, MO, SC); a recount and then a new election (federal: MT, OR, VT); the legislature (statewide: 18 states); a party committee (primary: AR, DE, IA, IN, MA, MD, NC, NY, RI, VT). Other rules are named in each rule's `steps`.

**Where a recount comes first.** In ten states a recount comes before the lot for at least one kind of office: AK, CO, FL, ME, MT, ND, NE, OR, SD, UT. The Florida reader notes that no section read says "recount, then draw lots" in so many words: the recount step is the reader's combination of 100.181 (lot) with 102.141(7) (a tie is a margin of zero, inside the half-percent that orders a recount), and the lot itself is the statute's words (see the rule's `note`).

## 3. Automatic recounts and requested ones

`recounts.json` holds 53 automatic-recount rules, 127 on request, 8 by a court and 12 of other kinds (200). Twenty-eight states have at least one rule for an automatic recount (the state or county recounts with no one's request), listed below with the trigger in each reading's own words. 38 states have a rule for a recount on request; read the quotation in `recounts.json`, which also carries who may ask, the margin if any, the cost, and the deadline. Connecticut's automatic step is a recanvass of the returns, not a hand recount.

### Automatic recounts (a recount with no one's request), as each reading records them

28 states: AK AL AZ CO CT DC DE FL GA HI KY ME MI MN MT ND NE NY OH OK OR SC SD TX UT VT WA WY

| State | Offices | Trigger, in the reading's words | Mark |
|---|---|---|---|
| AK | federal, presidential-electors, statewide, state-legislative, primary | only on a tie: the director initiates the recount | measured |
| AL | federal, statewide, state-legislative, local, measure | a margin of defeat of not more than one-half of one percent of the votes cast for the office or ballot measure | stated |
| AZ | federal, statewide, state-legislative, local, primary, measure | a margin of one-half of one percent or less of the votes cast for the top two candidates (or for and against a state-level measure): the recount is required | measured |
| CO | federal, presidential-electors, statewide, state-legislative, local, primary, measure | a difference between the highest and the next highest vote of one-half of one percent or less of the highest vote: a recount is held | measured |
| CO | local | a difference between the highest and the next highest vote of one-half of one percent or less of the highest vote: the designated election official orders a recount | measured |
| CT | federal, presidential-electors, statewide, state-legislative, local | a plurality of less than one-half of one percent of the votes cast for the office, but not more than two thousand votes, brings a recanvass of the returns | stated |
| CT | federal, presidential-electors, statewide, state-legislative, local | a plurality of less than twenty votes brings a recanvass of the returns | stated |
| CT | federal, presidential-electors, statewide, state-legislative, local | only on a tie: there is a recanvass of the returns for the office | stated |
| CT | measure | a Yes-No difference of less than one-half of one percent of the votes cast on the question, and not more than two thousand votes, brings a recanvass | stated |
| CT | primary | a primary plurality of less than one-half of one percent of the votes cast, but not more than one thousand votes, or of less than twenty votes, brings a recanvass | stated |
| DC | federal, presidential-electors, statewide, state-legislative, local | a margin of victory of less than one percent of the total votes cast for the office: the Board shall conduct a recount, at no cost to any candidate | measured |
| DC | measure | a difference between the votes for and against of less than one percent of the total votes cast: the Board shall conduct a recount | measured |
| DE | state-legislative, local | a margin of less than 1,000 votes or 1/2 of 1% of all votes cast for the 2 candidates, whichever is less: the Court recounts the ballots at state expense | measured |
| DE | primary | a primary margin of less than 1,000 votes (statewide) or 1/2 of 1% of all votes cast for the 2 candidates (any other contest), whichever is less: the Department recounts the ballots at state expense as part of the canvass | measured |
| DE | local | a difference between the top 2 candidates of 1/2 of 1% or less of the total votes cast for the office: the municipal Board of Elections recounts the ballots | measured |
| FL | federal, statewide, state-legislative, local, primary, measure | a candidate defeated or eliminated, or a measure approved or rejected, by one-half of one percent or less of the votes cast, makes a recount mandatory | measured |
| FL | presidential-electors | a margin of one-half of one percent or less between the tickets makes a recount mandatory | inferred |
| FL | federal, statewide, state-legislative, local, primary, measure | after the machine recount, a margin of one-quarter of one percent or less makes a manual recount of overvotes and undervotes mandatory | measured |
| GA | statewide | a margin of not more than one-half of one percent of the votes cast in a statewide executive contest that is the first or second contest on the ballot makes a manual recount of all ballots mandatory | measured |
| HI | federal, statewide, state-legislative, local, primary, measure | a margin equal to or less than one hundred votes or one-half of one percent of the votes cast in the contest, whichever is lesser, makes a recount of all votes in the contest mandatory | measured |
| HI | presidential-electors | the same lesser of one hundred votes and one-half of one percent, read to cover the presidential election | inferred |
| KY | federal, statewide, state-legislative | a candidate defeated by a margin of not more than one-half of one percent of the votes cast for the office makes a recount mandatory | measured |
| ME | federal, presidential-electors, statewide, state-legislative, local, primary, measure | an apparent tie vote only: the Secretary of State automatically initiates a recount, and the tie-break applies if the recount confirms the tie | measured |
| MI | federal, statewide, measure | a recount of all precincts is conducted automatically when a statewide primary or election is certified as decided by a vote differential of 0.1% or less of the votes cast, unless the loser files a waiver within 48 hours | measured |
| MI | state-legislative | a recount of the whole state senate district is automatic at a vote differential of 75 votes or less in a general election | measured |
| MI | state-legislative | a recount of the whole state representative district is automatic at a vote differential of 25 votes or less in a general election | measured |
| MN | measure | when the 'yes' votes on ratification of a proposed constitutional amendment are within one-quarter percent of all the other ballots cast at the election, the canvassing board recounts that question by hand with no request | measured |
| MT | federal, statewide, state-legislative, local, primary, measure | a tie vote brings a recount without any petition | measured |
| ND | primary | a recount must be conducted where an individual failed to be nominated by one percent or less of the highest vote cast for a candidate seeking nomination for the office | measured |
| ND | federal, presidential-electors, statewide, state-legislative, local | a recount must be conducted where an individual failed to be elected in a general or special election by one-half of one percent or less of the highest vote cast for a candidate for that office | measured |
| ND | measure | a recount must be conducted where a measure was decided by a margin not exceeding one-fourth of one percent of the total vote cast for and against | measured |
| NE | federal, statewide, state-legislative, local, primary | a losing candidate is entitled to a recount where the margin is one percent or less of the votes received by the winning candidate (the last qualifying candidate where there are several seats), if more than 500 votes were cast for the office | measured |
| NE | federal, statewide, state-legislative, local, primary | a losing candidate is entitled to a recount where the margin is two percent or less of the votes received by the winning candidate (the last qualifying candidate where there are several seats), if 500 or fewer votes were cast for the office | measured |
| NY | federal, presidential-electors, statewide, state-legislative, local, primary | a full manual recount of all ballots for the contest where the margin of victory is twenty votes or less, or is 0.5% or less | measured |
| NY | federal, presidential-electors, statewide, state-legislative, local, primary | a full manual recount where one million or more ballots were cast in the contest and the margin of victory is less than 5,000 votes | measured |
| OH | local, primary, measure | a margin under one-half of one percent of the total vote in a county or municipal election (the winner's lead does not reach one-half of one percent) | measured |
| OH | federal, state-legislative, local, primary, measure | a margin under one-half of one percent of the total vote in a district election | inferred |
| OH | federal, presidential-electors, statewide, primary, measure | a margin under one-fourth of one percent of the total vote in a statewide election | measured |
| OK | measure | a margin required for approval of one-half of one percent or less (statutory state question) or one percent or less (constitutional state question) of the votes cast for and against, if the revolving fund held $250,000 or more on election day | measured |
| OR | federal, presidential-electors, statewide, state-legislative, local, primary | a tie, or a difference between the apparent winner and the closest apparently defeated opponent of not more than one-fifth of one percent of the total votes for both candidates | measured |
| OR | statewide, local | a candidate's vote total within one-fifth of one percent of the total votes cast for the office of a majority (the threshold for winning outright at a nonpartisan election) | measured |
| OR | measure | a difference between votes for and votes against of not more than one-fifth of one percent of the total votes cast for and against the measure | measured |
| SC | federal, presidential-electors, statewide, state-legislative, local, primary | a difference of not more than one percent of the total votes cast for the office, between the declared winner and any other candidate, or at the runoff-qualification line in a primary | measured |
| SC | measure | a difference between the votes in favor and opposed of not more than one percent of the total cast on the amendment, question or issue | measured |
| SD | federal, presidential-electors, statewide, state-legislative, local, primary | a recount of all the votes involved happens when the canvass shows a tie | measured |
| TX | federal, statewide, state-legislative, local, primary | a recount with no request happens only when the election results in a tie | stated |
| UT | federal, statewide, state-legislative, local, primary | a recount with no request happens when two or more candidates for an office receive an equal and the highest number of votes (or, in an at-large race, an equal number of votes where one of them must be eliminated to fill the offices) | measured |
| VT | federal, statewide, state-legislative | on a tie vote the canvassing committee itself must petition the Superior Court for a recount; no candidate's request is needed | measured |
| WA | federal, statewide, state-legislative, local, primary | a difference of less than 2,000 votes and also less than one-half of one percent of the votes cast for both candidates: the county canvassing board recounts all votes cast on that position, with no request | measured |
| WA | statewide | a difference of less than 1,000 votes and also less than one-fourth of one percent of the votes cast for both candidates: the votes are recounted manually | measured |
| WA | federal, state-legislative, local, primary | a difference of less than 150 votes and also less than one-fourth of one percent of the votes cast for both candidates: the votes are recounted manually | measured |
| WY | federal, statewide, state-legislative, local, primary | a difference of less than one percent of the votes cast for the lowest winning candidate: all the votes for the office are recounted, with no request | measured |
| WY | measure | the proposition receives a number of votes, greater or lesser, within one percent of the number of votes required for passage | measured |

## 4. Not read, with the reason

Every reason below is the one the reading records (`unread` in each state's file). Three legislature sites fail with an incomplete certificate chain (`ilga.gov`, `cga.ct.gov`, `billstatus.ls.state.ms.us`: "SSL certificate problem: unable to get local issuer certificate"). The environment's guide says never to disable verification; none was. If the orchestrator wants these three read, it needs a route that does not weaken TLS.

| State | Status | Why |
|---|---|---|
| IL | unread | `ilga.gov` and `www.ilga.gov`: certificate failure, as above (not bypassed) |
| NH | unread | `gc.nh.gov`: curl error 52, empty reply (the earlier reader saw the same twice, and `sos.nh.gov` HTTP 403); Justia HTTP 403 |
| NJ | unread | the Legislature's statute viewer returns 132 characters of text (a script shell); Justia not asked for NJ after its refusal to the NH reading |
| NM | unread | `nmonesource.com`: HTTP 403 on its home page, its navigation page 128 characters (a script shell); Justia not asked after its refusal |
| PA | unread | `legis.state.pa.us`: HTTP 403 on the first request; Justia HTTP 403 |
| TN | unread | the official code viewer (LexisNexis) returns 0 characters (a script shell); `sos.tn.gov/elections` HTTP 403; Justia not asked after its refusal to the PA reading |
| WI | unread | `docs.legis.wisconsin.gov`: connection reset on the first request; the Elections Commission's recount manual page HTTP 403; Justia not asked |
| AL | partly | the Code of Alabama unreachable: the older site refused by the environment's proxy (502), the current ALISON page a script shell, `sos.alabama.gov` HTTP 403, Justia HTTP 403. Every rule rests on the Alabama Law Institute's Election Handbook (20th edition) [stated]; the tie sections for general and primary elections (17-12-23, 17-13-21) and the Code's recount sections are unread |
| AR | partly | no free statute site of the state was found; Justia refused. Every rule rests on the State Board of Election Commissioners' 2026 county manual [stated] |
| CA | partly | `leginfo.legislature.ca.gov`: HTTP 403 twice. The one recount rule rests on the Secretary of State's Recounts FAQ [stated]; the tie rule (the section the search results call Elec. Code 15651) is unread |
| CT | partly | `cga.ct.gov`: certificate failure. Every rule rests on the Secretary of the State's 2012 recanvass manual [stated], which reproduces the 2012 statutes and may be out of date; a general-election tie after the recanvass is unread |
| GA | partly | the Code is served only through a script application; Justia HTTP 403. The tie rule rests on the text of a bill (House Substitute to S.B. 202, 2021) [inferred]; the recount on request rests on a georgia.gov guide [stated]; the automatic recount rests on the 2026 special-session Act S.B. 3EX [measured, as an Act, not the Code] |
| IN | partly | `iga.in.gov` returns a script shell (24 characters). Every rule rests on the Election Division's 2026 Election Administrator's Manual (revised April 2026) [stated] |
| LA | partly | `legis.la.gov`: connection reset on the first request. Rules read in the Secretary of State's PDF of Title 18 (page footers "January, 2026") [stated]; the Constitution and the Titles other than 18 are unread |
| MS | partly | the state's code site could not be read. Rules read in the Secretary of State's PDF of Chapter 15, the 2017 printing, and the 2026 county handbook (rev. 12/24/2025) [stated]; the Governor's tie rule, changed in 2020, is unread (`sos.state.ms.us` HTTP 403; the legislature's host a certificate failure) |
| ND | partly | no refusal: every request was answered. Unread are the city, school-district, township and park-district tie rules, the presidential-elector and measure chapters, the Constitution and election contests |
| NY | partly | no refusal: every request was answered. Unread are court-ordered recounts and contests (Article 16), the Constitution's provisions on the Governor and on each house judging its members, and the town and city laws. No tie method for a general election was found in the sections read; it is recorded as none found |
| TX | partly | `statutes.capitol.texas.gov` returns one 250,874-byte script shell for every address; `www.sos.texas.gov` HTTP 403 on a second PDF; Justia HTTP 403. Every rule rests on the Secretary of State's Recount Guide (rev. 3/2/2026) [stated]: a tie brings an automatic recount, and what follows if the tie survives it is unread |

## 5. Leads from the earlier report, checked

The earlier report (`research/historical-close-races-v2.md`, sections 3a and 3b) read 16 states and left the others unread. Where this reading can say, from the readers' notes:

- **Borne out:** Florida (100.181 and 100.061 draw lots; the recount triggers at one-half and one-quarter of one percent) and Iowa (50.44 draws lots; 50.48 on written request at the lesser of one percent or fifty votes, fifteen hundredths of one percent for statewide and federal office).
- **Corrected:** New York's automatic manual recount is at twenty votes or less, or 0.5% or less (the earlier "less than 20 votes" was wrong at the boundary), and there is a third trigger for contests with a million or more ballots (a margin under 5,000). Virginia's "lot (24.2-674)" is right for local, legislative, congressional and elector offices but not for the three statewide executive offices, which go to the General Assembly; and a tie after a recount goes to a special election except for Governor, Lieutenant Governor, Attorney General and electors. Washington's "lot, RCW 29A.60.221" is right for the offices that section names but not for the statewide executive offices, which the Constitution (Article III, section 4) sends to a joint vote of the legislature; the recount figures (2,000 votes and 0.5%; manual tiers at 1,000 or 150 votes and 0.25%) are confirmed. Connecticut's "recount, then a special election three weeks after a general-election tie" was not confirmed; the three-week adjourned primary is a primary rule (Sec. 9-446).
- **Now confirmed for Georgia:** the earlier "automatic at 0.5% in the first or second statewide executive races" was unread then and is borne out by the 2026 Act S.B. 3EX; the "runoff in 28 days" applies to a non-federal general-election runoff, a federal one being on the ninth week's Tuesday (S.B. 202 substitute text).

## 6. Surprises worth knowing

- South Carolina breaks a tie by a runoff two weeks later, not by a lot, for general, special and primary elections. West Virginia has neither a lot nor a new election: the canvassers, or the Governor after thirty days on a tied person's application, select one of the tied persons.
- Missouri: a special election among the tied candidates only, or the General Assembly for six state officers and electors; a lot only if every tied candidate agrees. Montana: every certified tie is recounted first, then a special election (Congress), an appointment by the Governor (a supreme court justice, a district judge or a legislator), the legislature by joint ballot (state executives), or a lot (a primary).
- Mississippi: since 2017 a tie for a district office, or a seat on the Supreme Court or Court of Appeals, is decided by drawing straws from an opaque bag, and the Election Code as printed has no recount, only a look at the ballot boxes and a contest (rules [stated], from the Secretary of State's 2017 printing).
- A tied ballot measure is lost in Arizona ("deemed to have failed"), Utah, and Vermont (after a recount); in Kansas and Maine the "no" vote prevails; Iowa's measure is not adopted on an exact tie, with no other tie-break provided in the sections read; North Carolina's rule for a "ballot item" (a new election above 5,000 voters, random selection at 5,000 or fewer) is read as covering measures [inferred]. 28 states had no provision found for a tie on a measure.
- Louisiana has two systems at once since 2026: closed party primaries for Congress, the supreme court, BESE and the Public Service Commission, and an open primary and general election for the rest; its recount is only of the absentee-by-mail and early-voting ballots, at the requester's cost, when those ballots could change the result.
- Iowa's primary tie for a General Assembly seat goes to the party's precinct committee members (43.75); other primary ties go by lot.
- Michigan's automatic recount at 0.1% (75 votes for the Senate, 25 for the House) is from 2024 PA 74, effective April 2, 2025.

## 7. State by state

Tie rule by kind of office, from the reading's rules; "automatic recount" says whether the reading records one.

| State | Status | U.S. Senate/House | Statewide | State legislature | Local | Primary | Automatic recount |
|---|---|---|---|---|---|---|---|
| AK | read | recount, lot | recount, lot | recount, lot | none found | recount, lot | yes |
| AL | partly-read | unread | unread | unread | unread; legislature | other | yes |
| AR | partly-read | runoff | legislature; runoff | runoff | runoff | runoff; party committee | none found in the part read |
| AZ | read | lot | legislature; lot | lot | lot | lot | yes |
| CA | partly-read | unread | unread | unread | unread | unread | none found in the part read |
| CO | read | recount, lot | recount, lot; legislature | recount, lot | lot | other; recount, lot | yes |
| CT | partly-read | unread | unread | unread | unread | recount, new election | yes |
| DC | read | lot | lot | lot | lot | lot | yes |
| DE | read | new election; other | unread | new election | new election | party committee | yes |
| FL | read | recount, lot | recount, lot | recount, lot | recount, lot | recount, lot | yes |
| GA | partly-read | runoff | runoff | runoff | runoff | runoff | yes |
| HI | read | lot | lot | lot | lot | lot | yes |
| IA | read | lot; new election | lot; new election | lot; new election | lot | lot; party committee | none recorded |
| ID | read | lot | lot | lot | lot | lot | none recorded |
| IL | unread | unread | unread | unread | unread | unread | not read |
| IN | partly-read | new election | new election; legislature | new election | legislature | party committee | none found in the part read |
| KS | read | lot | lot; legislature | lot | lot | lot | none recorded |
| KY | read | lot | lot | lot | lot | none found | yes |
| LA | partly-read | new election | new election | new election | new election | other; lot | none found in the part read |
| MA | read | new election | legislature | new election; none found | new election | party committee | none recorded |
| MD | read | none found | legislature; other; new election | party committee | court; other; new election | party committee; none found; other | none recorded |
| ME | read | other | legislature | recount, new election | recount, new election | recount, lot | yes |
| MI | read | lot | lot | lot | lot | lot | yes |
| MN | read | lot | lot | lot | lot | lot | yes |
| MO | read | runoff; lot | legislature; lot | runoff; lot | runoff; lot | lot; runoff | none recorded |
| MS | partly-read | lot; unread | unread; lot | lot | lot; runoff | runoff; none found | none found in the part read |
| MT | read | recount, new election | other; legislature | other | other | recount, lot | yes |
| NC | read | new election; lot | new election; lot | new election; lot | new election; lot | runoff; party committee | none recorded |
| ND | partly-read | none found | new election | recount, lot | recount, lot | lot | yes |
| NE | read | lot | legislature | lot | recount, lot | recount, lot | yes |
| NH | unread | unread | unread | unread | unread | unread | not read |
| NJ | unread | unread | unread | unread | unread | unread | not read |
| NM | unread | unread | unread | unread | unread | unread | not read |
| NV | read | legislature | legislature | legislature | lot | lot; other | none recorded |
| NY | partly-read | none found | none found | none found | runoff; none found | party committee | yes |
| OH | read | lot | legislature; lot | lot; legislature | lot | lot | yes |
| OK | read | lot | lot; legislature | lot | lot | lot; runoff | yes |
| OR | read | recount, new election | recount, new election; legislature | recount, lot | recount, lot | recount, lot | yes |
| PA | unread | unread | unread | unread | unread | unread | not read |
| RI | read | new election | legislature | new election | none found | party committee | none recorded |
| SC | read | runoff | runoff | runoff | runoff; unread | runoff | yes |
| SD | read | recount, lot | recount, lot | recount, lot | recount, lot; lot | recount, lot; runoff | yes |
| TN | unread | unread | unread | unread | unread | unread | not read |
| TX | partly-read | unread | unread | unread | unread | unread | yes |
| UT | read | recount, lot | recount, lot | recount, lot | recount, lot | recount, lot | yes |
| VA | read | lot | legislature | lot | lot | lot | none recorded |
| VT | read | recount, new election | recount, new election | recount, new election | runoff | party committee | yes |
| WA | read | lot | legislature | lot | lot | lot | yes |
| WI | unread | unread | unread | unread | unread | unread | not read |
| WV | read | other | other | other | other | other | none recorded |
| WY | read | lot | lot | lot | lot | lot | yes |
