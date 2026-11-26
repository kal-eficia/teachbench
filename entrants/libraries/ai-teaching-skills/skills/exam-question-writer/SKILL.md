---
name: exam-question-writer
description: Write original exam-style questions with mark schemes that match a named exam board's command words, mark allocations and assessment objectives (Cambridge IGCSE, GCSE AQA/Edexcel/OCR, A level and others). Use when a teacher asks for exam questions, past-paper style practice, a mock paper, a mark scheme, or "questions like the real exam".
---

# Exam Question Writer

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.

Students lose marks on questions they understand because they misread what the command word asks for. Practice questions only help if they behave like the real paper.

## Step 1: Pin the target

Confirm: board and specification code, topic (spec reference if possible), tier or paper, and how many questions or marks. If the teacher has past papers, read two or three first and match their style, layout and difficulty curve. Never copy a real past-paper question: write original ones in the same mould.

## Step 2: Use the command words properly

Each command word sets the depth of the answer and the marks. Defaults (check the board's own glossary when you can):

| Command word | Student must | Typical marks |
|---|---|---|
| State / Give / Identify / Name | Recall a fact, no explanation | 1 per point |
| Define | Give the precise meaning | 1-2 |
| Describe | Say what happens or what something is like, in steps or features | 2-4 |
| Explain | Give reasons: what happens **and why**, linked with "because / so / therefore" | 2-6 |
| Compare | Similarities and/or differences, both sides referred to in each point | 2-4 |
| Calculate | Work out with working shown | 1-4 |
| Evaluate / Discuss / Justify | Weigh points for and against and reach a supported judgement | 4-8 |

Marks must match demand: a 4-mark "explain" needs four creditable, linked points to exist.

## Step 3: Write each question

- Start with a short context when the board does (a school network, a shop's database, a patient's symptoms).
- One command word per part. Split multi-part questions into (a), (b), (c) of rising difficulty.
- Put the marks in brackets at the end of each part: **[3]**.
- Plain, unambiguous language. No trick wording. No double negatives.
- For multiple choice: real misconceptions as distractors, and no answer patterns across the set (see `no-answer-patterns`).

## Step 4: Write the mark scheme

For each part:
- **Marking points**, one per mark, written as an examiner would ("Data is lost when power is removed (1)").
- **Accept**: other wording that earns the same mark.
- **Do not accept**: common answers that look close but don't earn the mark, with the reason.
- For levels-marked questions: level descriptors and an indicative content list.
- A model answer at full marks.

Write the marking points so they could feed [mark-point-checker](https://github.com/kal-eficia/mark-point-checker) directly if the teacher wants automatic feedback.

## Step 5: Check

- [ ] Every command word matches its marks and its mark scheme
- [ ] Each mark is independently creditable
- [ ] Nothing outside the named specification
- [ ] Difficulty rises through the paper
- [ ] No answer patterns in MCQs

## Before you hand over

- Match the board and tier exactly. A 'do not accept' list should only reject what the board's own mark schemes reject; at foundation tier, don't demand a term the specification doesn't require.
- Cover the core content of the topic the teacher named (for enzymes: active site, temperature, pH, denaturing), not just one corner of it.
- When the teacher says students struggle with a command word, build the parts on one shared context so a 'describe' part leads into the 'explain' part, and show the linking words in the model answer.

## With the classroom tools

If the `check_answer_key` tool is available, check any multiple-choice section. Write marking points so `mark_answers` can use them: an `id`, a `label`, and `accept` phrases.
