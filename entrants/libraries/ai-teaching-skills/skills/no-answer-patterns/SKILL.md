---
name: no-answer-patterns
description: Check and fix multiple-choice quizzes and sort/match tasks so the correct answers form no guessable pattern (runs, repeats, A-B-C-D staircases, alternation, repeating blocks, lopsided spreads). Use whenever you write or review MCQs, quizzes, hinge questions, starters, worksheets or sort tasks, and whenever a teacher says students are "spotting the pattern".
---

# No Answer Patterns

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.

Students learn the shape of an answer key faster than they learn the content. If the last three answers were B, C, D, they will pick A next. This skill makes sure the key gives nothing away.

## What counts as a pattern

For a set of questions, write the correct positions as letters, e.g. `CADBDACB`. It fails if it has any of these:

| Pattern | Example | Rule |
|---|---|---|
| Repeat | `C A A D` | Same position twice in a row |
| Run | `B B B` | Same position three or more times |
| Staircase | `A B C`, `D C B` | Climbs or falls one step at a time, 3+ long |
| Alternation | `A C A C` | Two positions swapping, 4+ long |
| Repeating block | `A C B · A C B` | Any block of 3 to 5 that repeats |
| Lopsided | 5 of 8 are `B` | One position correct more than half the time |

For **sort tasks**, do the same with the bucket each item belongs to, in the order items appear. Never list all the "Input" items and then all the "Output" items.

## How to check (do it with code, not by eye)

Run the bundled checker on the quiz JSON. In Claude Code, `${CLAUDE_SKILL_DIR}` is this skill's folder; in the Claude app, the script is at `scripts/check_key.py` next to this file.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_key.py quiz.json          # report
python3 ${CLAUDE_SKILL_DIR}/scripts/check_key.py quiz.json --fix     # rewrite option order safely
python3 ${CLAUDE_SKILL_DIR}/scripts/check_key.py --key CADBDACB      # check a bare key
```

Quiz JSON is a list of `{"q", "options", "answer"}` (answer as index or option text) and optional `{"type": "sort", "items": [{"text", "bucket"}]}`. If your quiz lives in HTML, extract the questions to this shape first.

**Can't run code** (for example in a chat assistant without code tools)? Write the key out as letters, then check each rule in the table above one at a time and show your working for each: list every pair of neighbours for repeats, every three in a row for runs and staircases, and count each letter for lopsidedness. Say plainly that it was checked by hand.

For bigger projects, use the full [pattern-guard](https://github.com/kal-eficia/pattern-guard) CLI.

## How to fix

1. Plan the key first: decide the correct position for each question so the key is clean and spread evenly (`--fix` does this).
2. Move each correct option to its planned position and shuffle the distractors around it. Never edit the wording to fit a position.
3. Re-run the check. It must say `clean` before you hand anything over.
4. Watch options that must stay in order ("All of the above", numeric ranges like 1, 2, 4, 8). Keep their internal order and pick a key that respects it, or rewrite the option.

## Before you finish

- [ ] Every MCQ set and every sort task checked by the script
- [ ] Correct answers still correct after reordering (the script verifies this)
- [ ] Across a multi-page lesson, check the whole lesson's key, not each page alone

## With the classroom tools

If the `check_answer_key`, `fix_answer_key` and `plan_answer_key` tools are available (the Claude Code plugin provides them), use them instead of running the script by hand. Plan the key first with `plan_answer_key` when you are writing a new quiz.
