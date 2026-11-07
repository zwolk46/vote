---
name: vote-tracker
description: Zach's "Vote Work" tracker artifact for the vote site, its URL, schema, and who keeps it current
metadata:
  type: reference
  modified: 2026-11-07T03:02:18.210Z
---

Zach watches the vote site's work in the "Vote Work" artifact: https://claude.ai/artifact/DzVTr4wvWE92sNxxEx6wKH (published 2026-11-07 by the orchestrator, a copy of "Midterms Work" https://claude.ai/artifact/FVgfkAoKfKgzHGLi1KHkSf). Source: `tracker/vote-work.html` in zwolk46/vote.

Rows live in the db collection `tasks`, one doc per item: `{s: "doing"|"todo"|"done", t: plain text, o: order number, link?: https URL, linkLabel?}`. Write them with ArtifactData; never republish the page to change rows.

**Why:** his ask of 2026-11-07 02:58: watch what is going on, open previews from one place, kept by a dedicated thread "analogous to the thread run in the midterms project".
**How to apply:** the tracker thread (brief `briefs/T1-tracker.md`) keeps it current; rows name pages and features in his words, not code names. See [[vote-project]].
