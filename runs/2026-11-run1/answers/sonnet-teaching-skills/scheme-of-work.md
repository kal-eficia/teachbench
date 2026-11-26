# Year 8 Computing: Python programming basics (half-term plan)

## Assumptions

- 6 weeks, 2 lessons a week, 50 minutes each = **12 lessons**. Weeks and lessons are numbered rather than dated, because I don't have your calendar. Check them against real dates and any lost lessons.
- Pupils did Scratch in Year 7 and have **never typed code**. Typing accuracy, capital letters, brackets and quotation marks will be the first barrier. Lesson 1 is built around that.
- Computers are available in every lesson, with Python through a school IDE or a browser editor, so nothing needs installing at home. If homework needs home access, flag it a week ahead.
- No spec reference is needed beyond KS3 National Curriculum Computing: *use two or more programming languages, at least one of which is textual, to solve a variety of computational problems; make appropriate use of data structures; design and develop modular programs.* Lists and functions are deliberately left for next half-term, so this half-term sets a solid base.
- **Pace:** one new idea per lesson. Assessment and checkpoint lessons introduce nothing new.
- The assessment is in **Week 6, Lesson 1** (Lesson 11), with the final lesson used for feedback and fixing gaps.

## Dependency chain

print and running code, then variables, then input, then data types and arithmetic, then selection (if/else, then elif and logic), then iteration (for, then while), then combining them. Each step needs the one before it, so the order can't change much.

## Scratch-to-Python bridge (use from Lesson 1)

| Scratch | Python |
|---|---|
| say [Hello] | `print("Hello")` |
| set [score] to 0 | `score = 0` |
| ask [Name?] and wait / answer | `name = input("Name? ")` |
| if / else | `if ... :` / `else:` |
| repeat 10 | `for i in range(10):` |
| forever / repeat until | `while ...:` |

Put this on the board in every lesson for the first three weeks. It tells pupils they already know the ideas, and only the typing is new.

---

## Lesson table

| Wk | Lesson | Objective | Starter draws from | Main task type | Check | Resources |
|---|---|---|---|---|---|---|
| 1 | **1. First lines of Python** | Type and run a program with `print()`; read and fix a syntax error | Scratch: "which blocks made a sprite talk, ask, repeat?" (Year 7) | Predict, run, then fix 5 broken one-line programs (missing bracket, missing quote, capital P). Typing accuracy game. | Exit ticket: write one line that prints your name | Computers with IDE, Scratch-to-Python table, broken-code sheet |
| 1 | **2. Variables** | Store a value in a variable, change it, and print it | L1: print, syntax errors | Predict then run (`x = 5`, `print(x)`); modify; make: a profile card using 3 variables | 3 hinge-style MCQs: what does this print? | Slides, worked examples, modify tasks |
| 2 | **3. Input** | Use `input()` to get a value from the user and store it | L2: variables, L1: print (1 and 3 lessons ago) | Worked example, then guided: a "greeter" and "mad libs" program; add one feature of their own | Spot the error in a program that reuses a variable name | Mad-libs starter code |
| 2 | **4. Data types and arithmetic** | Say the difference between a string and an integer; use `int()` and `+ - * /` | L3: input, L2: variables | Predict: `"5" + "5"` vs `5 + 5`; fix a program that crashes when adding two inputs; make a simple calculator | Short quiz (5 Qs) | Predict-the-output sheet |
| 3 | **5. Consolidation and Checkpoint 1** (no new content) | Combine print, variables, input, types in one program | L1-L4 (spaced: one question from each) | Mini-project: tip or pocket-money calculator, with a fixed success list; peer test | 8-question low-stakes quiz, with a confidence column. Teacher records who needs reteach. | Project brief, quiz, class tracker |
| 3 | **6. Selection: if and else** | Write a program that makes a decision with `if`/`else` and `==`, `>`, `<` | L2: variables, L4: types (Why must I use `int()` here?) | Scratch if blocks translated to Python; predict; fix indentation errors; make: password checker | Hinge question on `=` vs `==` | Indentation fix-it sheet |
| 4 | **7. More conditions: elif, and, or** | Choose between several outcomes using `elif`, `and`, `or` | L6: if/else, L3: input | Flow chart to code: grade boundaries, age-ticket pricing; add a rule; debug a program with two overlapping conditions | Predict the output for three inputs | Flow chart sheet |
| 4 | **8. Iteration: for loops** | Repeat code a set number of times using `for` and `range()` | L6: if (3 lessons ago), L5: project (6 lessons ago) | Scratch "repeat 10" to Python; predict; modify; make: times-table generator; trace what `i` is on each pass | Trace table for one loop | Trace table template |
| 5 | **9. Iteration: while loops** | Repeat until a condition is met using `while` | L8: for, L7: elif, L2: variables | Worked example: password retry; "guess the number" with a fixed number; spot the infinite loop | Which loop would you use: `for` or `while`? 4 scenarios | Guessing-game starter |
| 5 | **10. Flex and Checkpoint 2** (no new content) | Combine selection and iteration; fix gaps flagged on Checkpoint 1 and L9 | L1-L9, weighted to wrong answers on the quiz | Reteach in groups by gap (teacher-led group, independent group, extension group); finish the guessing game; revision on assessment format | 8-question mixed quiz, same format as assessment | Gap list from L5, past-style question sheet |
| 6 | **11. ASSESSMENT** (own slot) | Demonstrate Python basics: read, predict, fix, write | L1-L10, with a revision starter 5 min | 20 min written (predict output, spot error, trace table, short MCQs) plus 25 min practical (write a short program using input, a variable, selection and a loop) | Marked against the mark scheme | Assessment papers, mark scheme, IDE |
| 6 | **12. Feedback and reteach** | Fix the three most common errors; improve own assessment program | The three most common errors from Lesson 11 | Whole-class feedback; each pupil completes one improvement task and re-writes one wrong answer | Pupils re-answer one question, correctly | Whole-class feedback sheet, improvement task |

**Flex lessons:** Lessons 5, 10 and 12 contain no new content, so a lost or reteach lesson can borrow from them without losing the assessment date.

---

## Spaced retrieval (named starters)

Every lesson from Lesson 2 opens with a 5-minute retrieval starter drawing from 1, 3 and 6+ lessons ago, as shown in the table. For the early lessons, where there isn't six lessons' history, use Scratch knowledge. After Lesson 5, include one question on `print`, one on variables and one on input in the starter, because they decay fastest when later topics crowd them out.

## Assessment calendar

| When | What | Purpose |
|---|---|---|
| Lesson 5 (Wk 3) | Checkpoint 1: low-stakes quiz and mini-project | Find who needs reteach before selection begins |
| Lesson 10 (Wk 5) | Checkpoint 2: mixed quiz in assessment format | Rehearse the format; last gap-fill |
| Lesson 11 (Wk 6) | End-of-unit assessment | Written plus practical |
| Lesson 12 (Wk 6) | Feedback and reteach | Close the loop before the next unit |
| Start of next half-term | Retrieval starter on this unit | Spaced check |

**Keep for later:** your six-week review against baseline. If you gave no baseline, use Lesson 1's exit ticket and Lesson 5's quiz as starting points.

## Key vocabulary per phase

| Unit | Words |
|---|---|
| L1-L2 | program, syntax, error, run, string, variable, assign |
| L3-L5 | input, output, integer, float, convert, operator |
| L6-L7 | selection, condition, indentation, comparison operator, Boolean |
| L8-L10 | iteration, loop, range, counter, infinite loop, trace |
| L11-L12 | debug, predict, test |

## Common misconceptions

| Topic | Misconception | Fix |
|---|---|---|
| print | `print(name)` prints the word "name" | Compare `print(name)` and `print("name")` side by side |
| Syntax | Python will "know what I meant" | Computers do exactly what is typed; show one missing bracket stopping everything |
| Variables | `x = 5` is a maths equation | It means "put 5 into the box called x". Read it aloud as "x becomes 5" |
| Input | `input()` gives a number | It always gives a string; show `"5" + "5"` giving `"55"` |
| Selection | `=` and `==` are the same | `=` stores, `==` asks a question |
| Indentation | Spaces don't matter | The indented lines are the ones that belong to the `if`; the spaces are the program's structure |
| range | `range(5)` goes 1 to 5 | It goes 0 to 4. Trace it |
| while | The loop stops when it reaches the right value | It stops when the condition is false; if the variable never changes, it never stops |
| Case | `Print` and `print` are the same | Python is case sensitive |

## Home heads-up list

| When | What families need to know |
|---|---|
| Week 1 | Pupils start Python this half-term, typed code, not blocks. Mention the browser editor if there's a login. |
| Week 2 (before Lesson 3) | If homework uses a browser editor, confirm they can access it at home. School computers if not. |
| Week 4 | Checkpoint 2 and the assessment are coming; the retrieval quiz they bring home helps. |
| Week 5 | The assessment is next week. Practise with the guessing game. No new material. |
| Week 6 | Assessment results and the improvement task come back after Lesson 12. |

## Checks against the plan

- [x] Each lesson introduces one new idea only (L5, L10, L11, L12 introduce none)
- [x] No lesson depends on something taught later
- [x] The assessment is in its own slot
- [x] Creative and exam-style lessons both appear every fortnight (projects at L2, L3, L5, L8, L9, L10; predict/trace/debug in every lesson)
- [x] Flex and reteach time exists (L5, L10, L12)
- [x] Retrieval is built into every starter
