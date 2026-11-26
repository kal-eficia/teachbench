# Mapping your KS3 computing curriculum against the national curriculum

**Assumptions:** you are in England, following the national curriculum programme of study for computing at Key Stage 3, and you have schemes of work, lesson slides or resources, and any assessments for Years 7, 8 and 9. If you're elsewhere, swap in your own framework's statements and the method still applies.

The aim is a single picture showing, for every national curriculum requirement: where it's taught, how deeply, where it's assessed, and where it's revisited. Gaps, repetition and awkward ordering then become obvious.

---

## Step 1: Break the national curriculum into atomic points

The KS3 programme of study has nine bullet points, each of which contains several separate ideas. Split them so each row can be ticked or not. Give each a code. A workable list of about 20 rows:

| Code | Point (shortened from the programme of study) |
|---|---|
| A1 | Design, use and evaluate computational abstractions that model real-world problems |
| A2 | Understand key algorithms (e.g. sorting and searching) and compare alternatives using logical reasoning |
| P1 | Use two or more programming languages, at least one textual |
| P2 | Use data structures (lists, tables, arrays) appropriately |
| P3 | Design and develop modular programs using procedures or functions |
| L1 | Understand simple Boolean logic (AND, OR, NOT) and its use in circuits and programming |
| L2 | Represent numbers in binary; convert between binary and decimal |
| L3 | Carry out simple binary operations (e.g. addition) |
| H1 | Understand hardware and software components of computer systems |
| H2 | Understand how components and systems communicate (networks, internet) |
| H3 | Understand how instructions are stored and executed in a computer system |
| D1 | Represent text digitally in binary |
| D2 | Represent sound digitally in binary |
| D3 | Represent images digitally in binary |
| I1 | Creative projects selecting, using and combining multiple applications, ideally across devices |
| I2 | Collect and analyse data in projects |
| I3 | Meet the needs of known users |
| I4 | Create, reuse, revise and repurpose digital artefacts for an audience |
| I5 | Attention to trustworthy design and usability |
| S1 | Use technology safely, respectfully, responsibly and securely |
| S2 | Protect online identity and privacy |
| S3 | Recognise inappropriate content, contact and conduct; know how to report concerns |

Check the exact wording against the official document before you finalise your list. Your school may also want a second set of columns for your exam board's specification, to show readiness for GCSE.

## Step 2: Collect an honest inventory of what is taught

This is where most audits go wrong. Titles on a scheme of work overstate what happens in the lesson.

1. List every unit and every lesson: year, term, unit name, lesson title, number of lessons, and what the students actually do.
2. For each unit, ask the teacher who wrote or teaches it for 10 minutes: "What do students do in lessons 1, 3 and 5? What do they produce?"
3. Sample the real materials: slides, student books or folders, the end-of-unit test. If you can, look at a few books.
4. Note which lessons are taught by whom, and whether teachers actually follow the plan. A plan that isn't followed isn't the curriculum.

Record in a spreadsheet with one row per lesson (or per unit if lessons are too many to start with).

## Step 3: Tag the national curriculum codes to lessons

For each lesson, mark which codes it covers and at what depth:

- **I** = Introduced (first meeting, taught explicitly)
- **D** = Developed (extended, applied in new contexts)
- **A** = Assessed (a test question or marked task uses it)
- **R** = Retrieved (revisited later in a starter, quiz or later unit)

A lesson that mentions something in passing isn't "taught". Only tag it if students practise it.

## Step 4: Build the map

One row per national curriculum point (the 22 above). Columns by year and term, six or nine columns across Years 7 to 9. Fill cells with I, D, A, R. Add three final columns: **taught?** (Y/N), **assessed?** (Y/N), **status** (see below).

Illustrative layout (made-up entries to show the format):

| Code | Y7 T1 | Y7 T2 | Y7 T3 | Y8 T1 | Y8 T2 | Y8 T3 | Y9 T1 | Y9 T2 | Y9 T3 | Assessed | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 text language |  |  | I |  | D, A |  | D | D, A |  | Yes | Green |
| L1 Boolean logic |  |  |  | I |  |  | D |  |  | No | Amber (not assessed) |
| D2 sound |  |  |  |  |  |  |  |  |  | No | Red (gap) |
| S3 reporting concerns | I | R | R | R | R | R | R | R |  | Yes | Green, possibly over-repeated |

## Step 5: Find the problems

Look for these patterns in the map:

1. **Gaps.** Rows with nothing in them, usually the less glamorous ones (sound or image representation, Boolean logic, data structures, modularity, reporting concerns).
2. **Thin coverage.** Taught once, in one lesson, never revisited or assessed.
3. **Repetition.** The same thing taught in all three years with no progression (e-safety posters, or "intro to Scratch" again in Year 9).
4. **Order problems.** Something taught before the thing it depends on, e.g. binary addition before place value in binary; functions before basic programming; file formats before data representation.
5. **No progression in programming.** Check that a student moves from block-based to text-based and from sequence and selection to iteration, lists, functions, with a visible step up each year.
6. **Balance across the three strands**: computer science, information technology, digital literacy. Many departments end up heavily skewed to one.
7. **Delivery time.** Count the hours. If a unit has two weeks for "networks" and eight for "Scratch games", is that the right weighting?
8. **Disconnected sections.** Do units from different teachers use different language for the same idea (e.g. "variable" or "box")? Note it for later.

## Step 6: What the output should look like

A short pack, around four to six pages, that you can show to senior leaders and your team:

1. **The coverage map** (the table above, in full).
2. **A traffic-light summary** by strand (green = taught and assessed and retrieved; amber = taught but thin or not assessed; red = not taught).
3. **A progression view:** one line per big idea (programming, data, networks, logic, safety) showing the Y7, Y8, Y9 steps.
4. **Findings:** gaps, repetition and ordering clashes, in plain English with row references.
5. **The top five actions in order**, each with an owner and a date. Example: "Add a 3-lesson sound and image representation unit to Y8 T3 (D2, D3); move binary addition after binary conversion in Y8 T2; replace repeated Scratch intro in Y9 T1 with text-based programming."
6. **A plan for the time it takes:** if the gaps don't fit, say what to compress or cut, and don't try to squeeze them in everywhere.

## Practical tips for a new head of department

- Do the first pass yourself over about two weeks, then share it with the team and ask them to correct it. People are happier correcting a draft than being audited.
- Present it as "the curriculum we have inherited" and not as a judgement on colleagues' work.
- Fix the biggest gaps first. Don't rewrite everything in one go.
- Agree one shared set of definitions and vocabulary per topic so lessons in different years fit together.
- Repeat the map each summer: update it with what was actually taught, not what was planned.
