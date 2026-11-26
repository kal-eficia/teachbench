---
name: script-marker
description: Mark student answers or scripts against a mark scheme consistently: award each mark with its evidence, flag borderline and unreadable answers for the teacher, give short feedback per answer and summarise patterns across the class. Use when a teacher shares student answers with a mark scheme and asks for marking, provisional marks, feedback on answers or help getting through a pile of marking.
---

# Script Marker

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.
>
> **Student data:** use initials or numbers instead of names, and leave out health, SEND diagnoses, safeguarding and family details unless your school's data protection and AI policy allow this tool to handle them. If you can't tell, anonymise first.

AI marking is a first pass for the teacher to check, never the final mark. Its value is speed, consistency and a clear trail of why each mark was given.

## Rules

1. **Mark only against the mark scheme.** Award a mark only where the answer contains a creditable point; quote the words that earned it.
2. **Accept equivalent wording** the scheme would allow; don't accept what it explicitly rejects.
3. **Don't reward length**, confidence or style unless the scheme does.
4. **Flag, don't guess**: borderline answers, illegible text, and anything that might need a teacher's judgement are marked "teacher check" with the reason.
5. **Be consistent**: the same answer gets the same mark wherever it appears. Check the first five answers again at the end.
6. **Levels-marked questions**: place the answer in a level with the descriptor that fits, then a mark within the level, and say why.
7. **Privacy**: work with first names or codes only; don't store scripts beyond the task.

## Feedback per answer (one or two lines, to the student)

What earned marks, and the one thing that would earn the next mark: "You explained the effect. Add *why* it happens, using *volatile*."

## Output

- A marks table: student, question, mark, evidence quoted, teacher-check flag
- Short feedback per student
- Class patterns: the most common missing point per question (feed into `whole-class-feedback`)
- A list of every flagged answer for the teacher to decide

## With the classroom tools

If the `mark_answers` tool is available, use it for a first pass on short answers, then read every answer it flags for a teacher check and correct any mark where it matched the words but missed the meaning.
