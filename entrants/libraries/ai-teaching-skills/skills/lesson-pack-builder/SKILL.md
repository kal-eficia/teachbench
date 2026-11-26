---
name: lesson-pack-builder
description: Build a complete, ready-to-teach lesson pack (teacher plan, interactive student page, homework, mark scheme and a quick-check solutions sheet) for any subject and age group. Use when a teacher or tutor asks for a lesson, session, lesson plan, lesson pack, student worksheet or "everything I need to teach X".
---

# Lesson Pack Builder

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.

A lesson pack is five things that work together. Build all five every time. A teacher who asked for a lesson and got only a plan has to do the rest at 11pm.

| File | Who sees it | What it's for |
|---|---|---|
| `teacher-plan.md` | Teacher only | Timings, what to say, what to watch for, where students usually go wrong |
| `student-page.html` | Students | The lesson itself: one self-contained, interactive page |
| `homework.md` (or `.html`) | Students | 15 to 25 minutes of retrieval and one stretch task |
| `mark-scheme.md` | Teacher | Model answers and the marking points, exam-board style |
| `solutions.md` | Teacher | A one-screen answer key to approve student work live, in class |

## Step 1: Pin down the brief (ask only what you can't infer)

You need: subject and spec (exam board and code if any), topic, age or year group, lesson length, live or remote, and what came last lesson. If the teacher gave a spec code, use its wording for learning objectives. If something is missing and a wrong guess would waste the lesson, ask one short question. Otherwise state your assumption in the teacher plan and build.

## Step 2: Shape the lesson

Use this default flow unless the teacher has their own:

1. **Starter (5 to 8 min), recall first.** 3 to 5 questions on *previous* lessons, answered from memory. Add a confidence check ("Guessing / Think so / Certain") so the teacher sees confident-but-wrong answers.
2. **Learn (10 to 15 min).** One idea per page. Short paragraphs, one worked example, one exam tip.
3. **Check (5 min).** Hinge questions whose wrong options are real misconceptions, not filler.
4. **Apply (10 to 15 min).** Sort tasks, short answers, then one exam-style written question.
5. **Exit (3 min).** One question that proves the objective was met.

## Step 3: Write the student page

The student page is written **to the student**. Rules that make the difference:

- Second person, warm, plain. Match the age: an 11-year-old and a 17-year-old need different sentences.
- Nothing the student doesn't need. No "Teacher note", no objectives jargon, no "this activity develops…". Those go in the teacher plan.
- A page summary block at the **end of every page**, with a "Copy my summary" button, so students paste their work into the class chat page by page.
- Students never mark their own written answers. Multiple choice and sort tasks can give instant feedback; written answers are captured for the teacher.
- Multiple-choice options and sort items must have **no answer pattern** (see the `no-answer-patterns` skill). Check the key before you finish.
- One self-contained HTML file. No logins, no external accounts. Fonts from a CDN are fine.

If [lesson-page-kit](https://github.com/kal-eficia/lesson-page-kit) is available, write the lesson as its JSON and use its engine: it already handles summaries, confidence checks and pattern-free keys.

## Step 4: Write the teacher plan

Include: objectives (spec wording), a minute-by-minute timeline, what to say at each transition (one line each), the two or three misconceptions to listen for and how to fix each, differentiation (one support move, one stretch move), and what to note for next lesson's starter.

## Step 5: Homework, mark scheme, solutions

- **Homework:** mostly retrieval from this and earlier lessons, then one stretch question. Say how long it should take.
- **Mark scheme:** model answers plus the marking points an examiner would credit, and common answers that *don't* get the mark.
- **Solutions sheet:** one line per question, numbered to match the student page, so the teacher can approve work at a glance while teaching.

## Step 6: Check before handing over

- [ ] All five files exist and question numbers match across them
- [ ] Student page has a summary after every page and no teacher-only text
- [ ] No answer patterns in MCQs or sort tasks (run the check, don't eyeball it)
- [ ] Every fact is right for the named spec; nothing invented
- [ ] Open the HTML and click through it once

## With the classroom tools

If the `validate_lesson` and `build_lesson_page` tools are available, write the student page as lesson JSON (lesson-page-kit format), validate it, fix every error and teacher-voice warning, then build `student-page.html` with `build_lesson_page`. Run homework quizzes through `check_answer_key`.
