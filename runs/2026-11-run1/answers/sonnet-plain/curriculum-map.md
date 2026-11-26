# Mapping your KS3 computing curriculum against the national curriculum

**Assumptions:** you are in an English school following the national curriculum programme of study for computing at KS3. You have schemes of work, slides or lesson plans in various states, and about two to three weeks of part-time effort before the end of a half term. Check my paraphrases of the statements against the DfE document before you finalise the grid.

## The approach in seven steps

### 1. Fix the reference list first
Break the national curriculum KS3 computing statements into small, separately testable strands. Several of the official bullets bundle two or three ideas, and you will miss gaps if you map the bundles. A workable split:

| Code | Strand |
|---|---|
| CS1 | Computational abstractions that model real-world problems and systems |
| CS2 | Key algorithms (searching, sorting) and comparing alternative algorithms by logical reasoning |
| CS3 | Programming in two or more languages, at least one textual |
| CS4 | Data structures (lists, tables, arrays) |
| CS5 | Modular programs using procedures or functions |
| CS6 | Boolean logic (AND, OR, NOT) in circuits and programming |
| CS7 | Binary representation of numbers; conversion and simple binary addition |
| CS8 | Hardware and software components, and how they communicate with each other and other systems (networks) |
| CS9 | How instructions are stored and executed (fetch-decode-execute, memory) |
| CS10 | Representation of text, sound and images as binary |
| IT1 | Creative projects combining multiple applications, across devices, with known users |
| IT2 | Collecting and analysing data |
| IT3 | Creating, reusing, revising and repurposing digital artefacts for an audience, with attention to trustworthiness, design and usability |
| DL1 | Safe, respectful, responsible and secure use of technology; protecting identity and privacy |
| DL2 | Recognising inappropriate content, contact and conduct, and knowing how to report concerns |

Use the same codes everywhere. Adding your own extra row for anything you want to teach that the national curriculum does not mention (for example, AI, cyber security or GCSE readiness) stops useful content looking like "off-curriculum" waste.

### 2. Build an inventory of what is actually taught
Do not start from the scheme of work titles. Titles lie. Collect, for every unit in Years 7, 8 and 9:

- Unit title, number of lessons and term
- Lesson-by-lesson titles and learning objectives
- Main activities and software or language used (Scratch, Python, Excel, Micro:bit and so on)
- Assessments (what is tested, in what form)
- Who teaches it and whether they use the shared resources

Where there are no lesson plans, ask each teacher to spend 15 minutes filling in a one-page template per unit, then check a sample by looking at the pupils' books or work folders and by dropping into a lesson. What is delivered often differs from what is written down.

### 3. Tag each lesson (not each unit)
For every lesson, assign one primary strand code and, if relevant, up to two secondary ones. Tag by what pupils actually do or learn, not by what the title suggests. Apply a depth code:

- **E**: Exposure only (teacher shows it, pupils do not practise it)
- **I**: Introduced (pupils practise with support)
- **D**: Developed (pupils apply independently in a new context)
- **S**: Secured (pupils are assessed and can do it in unfamiliar situations)

Two people tagging a sample of 10 lessons independently, then comparing, will quickly show whether your definitions are consistent. Agree the rule, then continue.

### 4. Build the map
Put strands down the side and Year 7, 8 and 9 (by term) across the top. Each cell contains the unit and depth code. This is the grid you will use for the rest of the exercise.

### 5. Analyse it for six problems
1. **Gaps:** strands with nothing, or only exposure, anywhere in KS3. (Common: DL2 reporting concerns, abstraction/modelling, using more than one language, data structures, sound/image representation, collecting and analysing data.)
2. **Late or thin coverage:** strands that appear only in Year 9, or only once. Pupils who choose other options in Year 9 may never see them.
3. **Repetition:** the same content taught at the same depth in two years (typically e-safety, introductory Scratch, binary conversion, "parts of a computer").
4. **Progression breaks:** a strand that jumps from I to S with no D, or where Year 8 assumes knowledge Year 7 never taught (for example, loops and variables before sequence).
5. **Over-weighting:** too many weeks on one strand, particularly digital literacy and presentation software, at the expense of programming and computer science.
6. **Assessment mismatch:** things taught but never assessed, or assessed but never taught.

Also check each year for balance across the three strands (computer science, information technology, digital literacy) and for the tools used. Two languages, one text-based, is a statutory requirement that is easy to miss.

### 6. Sense-check with the teachers
Share the draft map with the team before it goes anywhere else. Ask them to challenge tags, not to defend their units. You will catch mistakes and get the buy-in you need for any changes.

### 7. Turn findings into decisions
Do not try to fix everything. Rank each issue by statutory importance, size of gap and how easy it is to fix, then propose a short list for this year and a longer one for next year.

## What the output should look like

Produce **four things**, in this order of importance.

### A. One-page coverage grid (the headline document)
| Strand | Y7 Autumn | Y7 Spring | Y7 Summer | Y8 Autumn | Y8 Spring | Y8 Summer | Y9 Autumn | Y9 Spring | Y9 Summer | RAG |
|---|---|---|---|---|---|---|---|---|---|---|
| CS3 Programming | Scratch (I) | | | Python intro (I) | Python (D) | | Python project (S) | | | Green |
| CS4 Data structures | | | | | | | Lists (I) | | | Red: late and thin |
| CS10 Data representation | Binary (I) | | | | | | | Images (I) | | Amber: no sound or text |
| DL2 Report concerns | | | | | | | | | | Red: not taught |

RAG rule: Green = reached S (or secure D) with a progression; Amber = present but thin, late or no progression; Red = missing or exposure only.

### B. Gap and overlap report (one to two pages)
Three short lists, each with a recommendation:
- **Gaps** (statement not met): what, where it could fit, effort needed.
- **Overlaps and repetition**: where lessons could be removed or merged to free time.
- **Progression issues**: what needs adding or reordering.

### C. Proposed action plan
A table with: Issue | Evidence | Proposed change | Owner | Deadline | Effort (low/medium/high) | Priority. Split into "this half term", "this year" and "next year".

### D. Appendix: the working data
The lesson-by-lesson tagging spreadsheet (one row per lesson: year, term, unit, lesson, strand codes, depth, tools, assessment). Keep it so the map can be updated and so anyone can check your evidence.

## Practical tips
- Use a spreadsheet with filters. A pivot or COUNTIFS across strands and years produces your grid almost automatically.
- Record "lessons per strand per year" as a number alongside the colours. Time is as informative as coverage.
- Present findings neutrally ("the curriculum as it stands") rather than naming who wrote what.
- Once you have agreed the final map, publish it as a one-page "what is taught where" for staff, and revisit it annually.
- Consider including a short column on prior knowledge from KS2 and forward links to GCSE so that progression is visible at both ends.
