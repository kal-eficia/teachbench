---
name: recall-starter
description: Build a 5 to 10 question retrieval starter for the next lesson from what students have already been taught and what they got wrong, using spaced, interleaved retrieval. Use when a teacher asks for a starter, a do-now, a retrieval quiz, a recap quiz or "questions to open the lesson".
---

# Recall Starter

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.
>
> **Student data:** use initials or numbers instead of names, and leave out health, SEND diagnoses, safeguarding and family details unless your school's data protection and AI policy allow this tool to handle them. If you can't tell, anonymise first.

The first five minutes of a lesson should make students pull old knowledge out of memory, not re-read it. That is what makes it stick. This skill builds those five minutes.

## What goes in (priority order)

1. **Recently got wrong.** Questions a student or the class missed last time it was asked. These are being forgotten right now.
2. **Due for a check.** Material taught 1, 3, 7, 14 or 30 days ago. Spacing beats cramming.
3. **Last lesson.** One or two questions on the previous lesson, so the thread is unbroken.
4. **Never asked.** One question from an older topic that hasn't come up in retrieval yet.

Not in: anything not yet taught. A starter is retrieval, not a pre-test.

## Rules

- 5 to 10 questions, answerable in 5 to 8 minutes. Mostly short-answer or MCQ.
- **Interleave**: no two neighbouring questions from the same topic.
- From memory only. Tell students: no notes, no searching, no AI.
- Add a confidence rating (Guessing / Think so / Certain) on MCQs if the teacher can see responses. Confident-and-wrong is the most useful signal in teaching.
- MCQ keys must have no answer pattern (use the `no-answer-patterns` skill).
- Give the teacher an answer key and one line on *why* each question was chosen.

## If you have data

If the teacher has a question bank and an attempts log (student, question id, date, right/wrong), use [recall-engine](https://github.com/kal-eficia/recall-engine) to pick the questions per student or per class:

```bash
recall-engine starter --bank bank.csv --log attempts.csv --student S07 --size 8 --answers
recall-engine review  --bank bank.csv --log attempts.csv --student S07   # six-week progress
```

If there's no data, ask what was taught in the last four lessons and what the class found hard, then build from that.

## Output

1. The student-facing starter (questions only, numbered).
2. The teacher key: answer, topic, and reason chosen, per question.

## With the classroom tools

If the `recall_starter` and `log_attempts` tools are available and the teacher keeps a question bank, use `recall_starter` to choose the questions and `log_attempts` to record the results afterwards. Run any multiple-choice questions through `check_answer_key`.
