---
name: teaching-context
description: Set up or update a teaching-context.md file that records who you teach, what, where and how (school type, subjects, exam boards and codes, year groups, class sizes, timetable, delivery mode, house style, rules and student needs) so every other teaching skill can read it instead of asking again. Use first when someone starts using these skills, or when they say "remember my classes", "set up my teaching profile", or their timetable, subjects or rules change.
---

# Teaching Context

Every teaching skill in this library works better when it knows the teacher. This skill writes that knowledge down once, in a file the other skills read first.

## Where it lives

`teaching-context.md` in the project root, or `.agents/teaching-context.md`. If one exists, read it, show a short summary, and ask only what has changed.

## Interview (one topic at a time, skip anything already known)

1. **You**: name as students should see it, role (class teacher, tutor, head of department, SENCO), years of experience.
2. **Setting**: school type (state, independent, faith school, online school, tuition centre, home education), country and curriculum.
3. **Delivery**: in person, live online (which platform: Zoom, Teams), or hybrid. Devices students have. Any LMS (Google Classroom, Teams, Canvas, Neo).
4. **What you teach**: for each class or student: subject, year group, exam board and specification code, tier, class size, lessons per week and length.
5. **Timetable**: days and times (optional, used for planning and reminders).
6. **Where they are**: current topic per class and what's next.
7. **Students**: overall attainment, common needs (SEND, EAL, attention, confidence), what motivates them. No names unless the teacher wants them stored.
8. **House rules**: e.g. "no self-marking", "summary after every page", "no answer patterns in MCQs", "British spelling", "no activities built on untrue statements", "no music in videos".
9. **Voice and style**: how student-facing material should sound; brand fonts or colours for resources.
10. **Assessment**: assessment windows, report deadlines, how reports reach parents.
11. **Data rules**: which AI tools the school has approved, whether student names may be used in them, and anything that must never be shared (for example health or safeguarding information). If unsure, record "anonymise everything".

## The file

```markdown
# Teaching context (updated YYYY-MM-DD)
## Me
## Setting and delivery
## Classes
| Class | Subject | Board / code | Year | Size | Lessons/wk | Current topic |
## Students: needs and motivation
## House rules (every skill must follow these)
## Voice and resource style
## Assessment calendar
## Data rules (what may and may not go into AI tools)
```

## Rules

- Record only what the teacher says. Don't guess grades or needs.
- Keep student names out unless the teacher explicitly wants them in, and never store sensitive details about individual children (health, safeguarding, family circumstances).
- Every other skill: if this file exists, read it first, follow its house rules, and don't re-ask what it answers.
- In anything written for the teacher, students or parents, never mention skills, skill files, checklists or this context file. Just do the work.
