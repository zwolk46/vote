# Brief B2: Try to break the law draft before it goes to the maker

*Written 2026-11-07 by the orchestrator. Model: **Fable 5.1**, effort **xhigh**. The project instructions' table puts "breaking the law and the model" on Fable, because an error in the law is carried into every tier below it (general law 2, 13). Read `briefs/_COMMON.md` whole first; it is part of this brief.*

## Your sub-end

**Find every place where `law/LAW-DRAFT-1.md` says something other than what the maker means, says it more narrowly or more broadly, or can be read more than one way, before he is asked to ratify it.**

*Why it matters:* once he ratifies it, its words are not changed (general law 16c), and every worker reads them literally. A break caught now costs a sentence. Caught later, it costs a ruling per case, or a site built on the wrong reading.

## What the draft is held to

- **The maker's words:** `brainstorm/2026-11-06-transcript.md`, `brainstorm/2026-11-07-transcript.md`, `inherited/MAKER-ASK.md` (his ask of 2026-11-06 15:34), and `RULINGS.md`. They are the standard. The law must leave out nothing he said that changes what gets made, and add nothing he did not say.
- **The general law:** `the-law-for-agents.md`, especially 2b, 4 to 5c, 7 to 7e, 14b, 16b and 16e. It says what a law must be.
- **The model it points to:** `model/MODEL-DRAFT-3.md`, and Fable's earlier breaks of draft 2, `model/BREAKS-draft-2.md`. Draft 3 is the method; the law is the end, the constraints and the path.

## What to do

1. **Breaks of intention** (general law 16b). For each principle, move one variable it bears on, hold the rest still, and ask whether the words still say what the maker means. Look in particular at:
   - the end (1) and whether it is his end, at the highest level that still changes what gets made (general law 4a);
   - 1a, which makes the site show the cases against his claim;
   - 1b, what is not the end;
   - the standard (2 to 2c), including 2a ("ex ante") and the race-and-ballot ruling;
   - the measures (3 to 6) and how they are held together (1c);
   - what the draft puts under lesser ends and considerations, and whether any of it is really the end or a constraint.

   Report each break as: the variable, the case, what the draft says, what his words suggest, and a fix in one sentence. A break may end in revised words, in a point left to rulings because of its gravity, or in a point marked open (16b).
2. **Breaks of reading.** Where could a stranger with a broad education, but no statistics and no knowledge of this project, read a term or a principle in a way the maker does not mean? Give each word or phrase, its readings, and a plainer wording.
3. **Breaks of form** (general law 7e, 16e, 18). A principle without its reason; a reason that does not support its principle; a term used in a second meaning; a word or sentence that can be removed with no loss.
4. **What is missing.** Anything he said that changes what gets made and is not in the draft; any constraint too obvious for him to say (general law 5c) whose answer would change the site.
5. **Facts.** Check every quotation against the transcripts, word for word, and every date and time.

## Path and constraints

- Write `law/BREAKS-draft-1.md`. Give each break a number, a kind (intention, reading, form, missing, fact), a severity (changes what gets made / wording) and a fix. Rank the most severe at the top. Then list what you checked and found sound.
- Do not edit the draft or any other file. The orchestrator decides what changes (`_COMMON.md` 3).
- Nothing needs fetching; if something does, `_COMMON.md` 6, 7 and 13 apply.
- Work on your own branch from `main`, and open a pull request that adds only `law/BREAKS-draft-1.md`. Push every turn.

## Done when

Every item above has been worked, the file is in a pull request, and you have reported to the orchestrator thread in at most fifteen lines, the most severe breaks first. Then stop (`_COMMON.md` 14).
