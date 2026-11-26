# OCR A level Computer Science NEA (H446): an 8-month plan and what help you can give

## Assumptions

- The component is OCR's A level Computer Science programming project (H446, about 20% of the qualification, 70 marks). Students choose their own problem, build a solution for a real or realistic end user, and write it up.
- "Next 8 months" runs from the start of the project (September) to the end of April. That leaves the first weeks of May for internal checking and marks before OCR's mark submission deadline (normally mid-May for the June series). **Check the exact dates in OCR's current key dates and the NEA guide.** If your start is later, squeeze the early stages first, not the build.
- The four assessed sections and their marks, as I understand the current specification, are: analysis (10), design (15), developing the solution (25) and evaluation (20). **Please check the weighting against the current OCR specification and marking criteria before you share any of this with students.**
- I've given weeks as "Week 1 to Week 34" so you can map them onto your calendar and holidays.

## Why students leave it to the last month, and the plan that fixes it

Students leave it late because the deadline feels far away and the first stage (analysis) feels like paperwork rather than programming. The build is the biggest section, so it needs the most time, but it is the part students most underestimate. The plan below front-loads small deadlines, makes evidence visible every fortnight, and puts a hard stop on analysis and design so the build starts early.

**Rules of the plan**

1. Every stage has an internal deadline that is earlier than it needs to be, and a buffer.
2. Every fortnight students show you something: a document, a screenshot, a working piece of code.
3. Evidence is created as they go (dated log, version history, screenshots, testing as each iteration is built). It can't be recreated at the end.
4. Development is split into iterations, each with its own mini-design, build, test and review. This stops a student building one giant program in April.

## The 8-month timeline

| Month | Weeks | Stage | What's done by the end | Hard internal deadline |
|---|---|---|---|---|
| 1 | 1 to 4 | **Choosing the problem** | Short problem proposal (one page): who the user is, what they need, why it needs computation, why it is complex enough. Teacher confirms it is suitable. Find and name a real end user or stakeholder. | End of week 3: problem approved. End of week 4: stakeholder contacted. |
| 2 | 5 to 8 | **Analysis** | Problem description, stakeholders, research (including interview or survey and existing similar solutions), essential features, limitations, requirements, success criteria. | End of week 8: analysis complete (first full draft). |
| 3 | 9 to 13 | **Design** | Decomposition, algorithms (pseudocode/flowcharts), data structures, UI mock-ups, validation, test plan with data. Plan the iterations. | End of week 13: design complete, and a **first working prototype of one small feature** shown to you. |
| 4 | 14 to 17 | **Build: iteration 1** | First usable core: the most important feature, working end to end. Annotated code, screenshots, tests carried out and recorded. | End of week 17: iteration 1 tested and documented. |
| 5 | 18 to 21 | **Build: iteration 2** | Next features, with review against the success criteria and stakeholder feedback. | End of week 21. |
| 6 | 22 to 26 | **Build: iteration 3 and polish** | Remaining features, validation, robustness, final testing against the full test plan. | End of week 26: **code freeze**. No new features after this. |
| 7 | 27 to 30 | **Testing and evaluation** | Full testing evidence, usability feedback from the stakeholder, evaluation against success criteria, limitations and future maintenance. | End of week 30: first full draft of the whole project complete. |
| 8 | 31 to 34 | **Review, fix, final submission** | Students review the whole report against the criteria. Final checks on referencing, acknowledgement of any AI use, file organisation and the declaration. | End of week 32: final student submission. Weeks 33 to 34: marking, internal standardisation and moderation sample prepared. |

If a student is far behind at any checkpoint, the time to act is **that week**, not the month before the deadline (see "When someone falls behind").

## Keeping them on track week to week

**A fortnightly checkpoint** (15 minutes in lessons, while the rest work independently): each student shows you where they are against the stage checklist. You record green (on track), amber (a week behind) or red (more than two weeks behind). Put it on a visible tracker.

**A one-page teacher tracker** (student by stage):

| Student | Problem approved | Analysis | Design | Iteration 1 | Iteration 2 | Iteration 3 | Testing | Evaluation | Final check | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| ... | date | date | date | date | date | date | date | date | date | G / A / R |

**Student stage checklists** (what must exist before they move on):

- *Analysis:* named end user and evidence of talking to them; research into at least one similar existing solution; success criteria that can be measured; limitations stated.
- *Design:* every success criterion has something in the design to meet it; algorithms for the hard parts; planned test data (normal, boundary, erroneous); an iteration plan.
- *Build:* each iteration has code (annotated, with meaningful names), screenshots, tests run with actual results, and a short review of what changed and why.
- *Evaluation:* refers back to each success criterion with evidence; includes feedback from the user; honest about what doesn't work and what would be improved.

**Evidence habits** to teach in the first week: save a dated version of the work every session, keep a short development log with reasons for decisions written at the time, take screenshots as you go, and never delete failed attempts. The criteria reward these and they are very hard to recreate later.

**Lessons that support the NEA:** use lesson time for a weekly 10-minute "stand-up" where each student says what they'll finish this week. It's quick, it creates a small public commitment, and procrastination shows up quickly. Also teach the technical skills they will need (OOP, recursion, data structures, file handling, databases, validation) in normal lessons, as general teaching, before they need them.

**Parents:** a short message at the start with the dates and a mid-year update on the stage reached. Ask parents to help with a regular work time, not with the content.

## When someone falls behind

| Trigger | Action |
|---|---|
| One amber checkpoint | Quiet conversation: what's blocking you? Agree what will be shown by the next checkpoint. |
| Two ambers in a row, or one red | Short written plan with dates; catch-up sessions in a supervised room at lunch or after school; note it for the head of sixth form. |
| Still red at the iteration 2 deadline | Meeting with parents. Scale back the project's ambition so something complete and well evidenced is submitted, since a smaller finished project beats an ambitious unfinished one. |
| Concerns about authenticity (see below) | Follow your centre's malpractice procedure straight away. |

## What help you're allowed to give

**Please read this against the current JCQ document *Instructions for conducting non-examination assessments*, the JCQ guidance on *AI use in assessments*, and OCR's own NEA guidance for H446 before you brief students.** The rules are strict, they can change, and your exams officer will have the current versions. What follows is my understanding of how they apply, so confirm anything marked "check".

### The principle

The work submitted must be the student's own, and the teacher must be able to **authenticate** it. Teachers may give **general** help and advice, but not detailed direction on what to change. Anything beyond general help must be recorded and may affect the marks.

### Generally fine

- Teaching the programming and computing content they need, in normal lessons, before and during the project (this is just teaching).
- Explaining the assessment criteria and what each section is looking for, using general or invented examples (not a model for their project).
- Checking that their chosen problem is suitable and complex enough, and that they have access to a real end user. (You may say "this is too simple to reach the top band", but not tell them which problem to choose.)
- Making sure they understand the process, the deadlines and the rules on authenticity and AI.
- Giving **general feedback** on their work at a stage (for example, "Your analysis doesn't yet say how you'll measure each success criterion" or "Your testing section has no erroneous data"). Point to the criterion and the gap.
- Asking questions that prompt them to think ("How would your user know this worked?"), as long as you aren't giving the answer.
- Monitoring progress and keeping a record of what each student has shown you.
- Reminding them to acknowledge sources, libraries and any permitted tools.

### Not allowed

- Choosing the problem for them, or giving them a project to copy.
- Writing or correcting their code, algorithms, designs, test plans or text. Don't fix bugs for them.
- Detailed or line-by-line feedback telling them exactly what to change to get more marks, or marking drafts repeatedly.
- Giving the same worked solution to the whole class to adapt. A model project for a **different** problem as general teaching is not the same, but check with OCR's guidance before using one.
- Letting students share code or work together in a way that makes their submissions the same. Discussing general ideas is fine; copying is not, and group work isn't permitted for an individual NEA.
- Changing work after it has been submitted for assessment.
- Reviewing and returning draft after draft. (JCQ rules allow a teacher to review work and give general feedback; check the current wording on how many times and in what form.)

### AI tools

- JCQ's guidance says students must be able to show the work is theirs; any use of AI must be acknowledged and clearly referenced, and work that cannot be authenticated as the student's own, or that relies on AI-generated material that isn't properly acknowledged, can be treated as malpractice.
- **Tell students on day one**, in writing, what your centre allows. A safe, simple stance: AI must not write their code, design, analysis or evaluation. If you permit it for something minor (such as explaining an error message), they must record it in their log: what tool, what they asked, what they used.
- Keep **the authentication evidence**: the development log, version history, dated screenshots, and your own record of seeing the work develop. Be ready to ask a student to explain their code in a short conversation; if they can't explain code they have submitted, that is a red flag.
- If you suspect AI use that hasn't been declared, or copied work, **don't investigate informally and don't accuse**. Speak to your exams officer and follow the malpractice procedure.

### Record keeping

- Keep a simple log of help given to each student (date, stage, what was said). It protects you and them.
- Make sure the student declaration and teacher declaration are completed at the end, as OCR requires. (Check which form and when.)

### Check before you start

- [ ] OCR's current key dates for H446 NEA and the mark submission deadline
- [ ] The current JCQ NEA instructions and the AI guidance (ask your exams officer)
- [ ] What your centre's own policy says, and who authorises any exceptions
- [ ] The current OCR marking criteria, and whether the section weightings I've used here are right
- [ ] Whether work for this component must be done under a specific level of supervision (check OCR's guidance)

## A first-week handout for students (outline)

1. The four sections, what each is worth, and what the top band looks like in plain language
2. The timeline and the hard deadlines
3. The evidence habits (version saves, log, screenshots)
4. What help they can and can't get from you
5. The rules on AI and acknowledgement
6. How to pick a good problem: a real person with a real need, enough complexity, something you can finish
