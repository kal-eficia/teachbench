# TeachBench

**How good is AI at the actual work of teaching?**

Most AI benchmarks test whether a model can answer exam questions. TeachBench tests the teacher's side of the desk: planning lessons, writing quizzes, explaining ideas, adapting work for SEND and EAL students, writing to parents, tutoring and leading staff.

There are 72 real requests a teacher might send, from Reception phonics to A level psychology. Every entrant answers all 72. Two graders score each answer blind against criteria that were written before any answers existed, and code checks whatever code can check.

**Leaderboard:** [kal-eficia.github.io/teachbench](https://kal-eficia.github.io/teachbench/)

## Run 1 · November 2026

| | Entrant | Score | 95% interval | Code checks |
|---|---|---|---|---|
| 1 | Claude Sonnet + [ai-teaching-skills](https://github.com/kal-eficia/ai-teaching-skills) | **95.8** | 94.1 to 97.3 | 7/8 |
| 2 | Claude Haiku + ai-teaching-skills | 85.0 | 82.0 to 87.7 | 6/8 |
| 3 | Claude Sonnet | 82.7 | 79.3 to 85.9 | 2/8 |

Head to head, task by task (a gap of 1 point or less counts as level):

- Sonnet with the skills beat plain Sonnet on 52 tasks, lost 4 and drew 16.
- Haiku with the skills against plain Sonnet: 30 higher, 33 lower, 9 level. In other words, the skills lifted the smallest model to roughly level with the bigger one. The intervals overlap, so this run doesn't show a clear winner between those two.

All 216 answers were scored. The two graders agreed within 2 points (out of 12) on 99.5% of answers. Every answer and every grade is in [`runs/2026-11-run1`](runs/2026-11-run1).

## How it works

1. **Tasks.** [`tasks/tasks.json`](tasks/tasks.json) holds 72 tasks, 9 in each of 8 categories: planning, retrieval, assessment, explaining, inclusion, pastoral and parents, tutoring and progress, and leadership and AI. Each task is written as a message a teacher would actually send, with 6 criteria a good answer must meet.
2. **Answers.** Each entrant answers in its own sessions, with no way to ask questions. An entrant with a skill library is given an index and chooses its own skill for each task, as it would in real use. Answer files are named by random ids only.
3. **Blind grading.** Each task goes to two graders. They see every entrant's answer side by side, shuffled, with names removed, and they read them in opposite orders. They score each criterion 0, 1 or 2.
4. **Code checks.** Where a task allows it, code checks the answer too: multiple-choice answer keys for guessable patterns (runs, repeats, alternation), student reports for repeated wording, messages for length and texts for reading age. A passed check adds 2 points to that answer.
5. **Score.** An entrant's score is the share of available points it earned, averaged over the tasks. The interval comes from resampling the tasks 4,000 times.

The harness is plain Python with no dependencies:

```
harness/prepare.py   writes the answer prompts, the blind grader prompts and a secret key
harness/checks.py    the code checks
harness/score.py     joins grades to the key, scores, and publishes a run
harness/build_site.py builds the leaderboard into _site/
```

## Limits

Read these before you quote a number.

- The graders are AI models (Claude Opus), not teachers. A teacher-graded round is the next step.
- Each entrant gave one answer per task. Single tasks vary, so the overall pattern and the intervals matter more than any single task.
- The tasks and criteria were written by Kalid Nur, who also wrote the ai-teaching-skills entrant. The criteria describe widely shared good practice, but they aren't neutral. Tasks from other teachers are very welcome.
- Each answering agent handled six tasks in one session and was told to treat each one as a new conversation.
- Most tasks follow UK curricula and are secondary level. Primary, early years and sixth form are included, with fewer tasks.

## Submit an entrant

An entrant is a model plus whatever you give it: a skill library, a system prompt, or nothing.

1. Add a JSON file to [`entrants/`](entrants), following the existing ones:
   ```json
   {"id": "your-entrant", "name": "Display name", "model": "sonnet",
    "skills": "entrants/libraries/your-library/skills",
    "source": "https://github.com/you/your-library",
    "notes": "One line on what it is."}
   ```
   Use `"skills"` for a folder of Agent Skills (each with a `SKILL.md`), or `"prompt"` for a system prompt. Leave both out for a plain model.
2. Put your skills under `entrants/libraries/`, or your prompt in the file itself.
3. Open a pull request. New entrants are run with the next round, against the same tasks, and graded blind alongside everyone else.

New tasks are just as welcome, especially from teachers in other subjects, phases and countries. Open an issue or a pull request against `tasks/tasks.json` with the request, the phase and subject, and six criteria.

## Run it yourself

```
python harness/prepare.py work --entrants sonnet-plain,sonnet-teaching-skills
# run each prompt in work/agents/ in its own session, then each in work/graders/
python harness/score.py work --publish my-run
python harness/build_site.py
python -m pytest -q tests
```

## Licence

MIT. Built by [Kalid Nur](https://github.com/kal-eficia), who teaches Computer Science, ICT and AI and trains schools and businesses to use Claude.
