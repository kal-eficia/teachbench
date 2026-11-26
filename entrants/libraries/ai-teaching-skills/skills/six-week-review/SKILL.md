---
name: six-week-review
description: Run a six-week progress review for a student or class: compare current performance with the baseline by topic and skill, show what has improved and what hasn't, and set the next six weeks' priorities, with a short report for the student and parents. Use when a teacher or tutor asks for a progress review, six-week review, half-termly check-in, progress report against a baseline, or whether their teaching is working.
---

# Six-Week Review

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.
>
> **Student data:** use initials or numbers instead of names, and leave out health, SEND diagnoses, safeguarding and family details unless your school's data protection and AI policy allow this tool to handle them. If you can't tell, anonymise first.

A six-week review answers one question honestly: is this working? Compare like with like, against where the student started.

## Inputs

The baseline (diagnostic results, first quiz scores, or the teacher's starting notes), the last six weeks of quiz and homework results, attendance, and the teacher's notes. If the questions were logged, [recall-engine](https://github.com/kal-eficia/recall-engine) can produce the topic-by-topic comparison.

## Steps

1. **Same measure, both times**: compare topic by topic using the same or equivalent questions.
2. **Show change**: baseline, now, change, for each topic or skill.
3. **Separate the stories**: topics that moved (keep doing what worked), topics that didn't (why: not taught yet, taught but not retrieved, or a misconception), and new gaps.
4. **Check the habits**: attendance, homework completion, confidence ratings.
5. **Set three priorities** for the next six weeks, each with the action.

## Report (student and parent version)

Sandwich form: a real strength with evidence, the one priority and what the student will do, a hopeful close (see `student-report-writer`). Plain language; say who does what at home.

## Output

A comparison table, a short analysis for the teacher, three priorities with actions, and the student or parent summary.

## With the classroom tools

If the `progress_review` tool is available and there is an attempts log, use it for the comparison table, then run the summary for home through `check_reports`.
