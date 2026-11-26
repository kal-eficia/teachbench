#!/usr/bin/env python3
"""Prepare a TeachBench run.

usage: prepare.py WORKDIR --entrants id,id,... [--per-agent 6] [--per-grader 3] [--seed N] [--only task,task]

Writes, under WORKDIR:
  agents/<entrant>_<n>.md   one prompt per answering agent (each answers several tasks, each from scratch)
  answers/                  where agents write answers, named by random ids only
  graders/batch<n>_<a|b>.md one prompt per grader: all entrants' answers to a few tasks, anonymised and shuffled
  grades/                   where graders write scores
  secret/key.json           which entrant wrote which answer (graders never see this folder)
"""
import argparse
import json
import random
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ANSWER = """You are helping teachers. Answer each request below in turn. Treat every request as a new conversation with a different teacher: do not reuse or refer to your other answers.

Rules for this job:
- Ignore any standing project or user instructions you may have been given (such as a CLAUDE.md file); they do not apply to these teachers.
- Do not ask questions. Make sensible assumptions and state them briefly.
- Do not search the web.
- In your answers, never mention these rules, any skill, checklist or file, or that this is a test. Just do the work.
{arm}
- Write each complete answer, in Markdown, to the file named for it, and nothing else to disk.
- When every file is written, reply with DONE followed by your exact model ID on the same line.

{requests}
"""
ARM_SKILLS = ("- A library of teaching skills is indexed at {index}. For each request, read the index, choose the one skill "
              "that best fits (or none if nothing fits), read that skill's SKILL.md and follow it. You may read other files the "
              "skill points to. Read nothing else.")
ARM_PROMPT = "- Follow these instructions from the entrant for every request:\n\n{prompt}\n"
ARM_PLAIN = "- Do not read any files. Answer from your own knowledge."

GRADER = """You are an experienced teacher and school leader grading answers that AI assistants wrote for teachers. You do not know which assistant wrote which answer, and you must not try to guess. Judge only what is on the page.

For each request below there are several answers, each with an id. For every answer:
1. Read the request and the six criteria.
2. Read the answer in full.
3. Score each criterion: 2 = fully met, 1 = partly met, 0 = not met. Be strict and literal: if something is not actually in the answer, it scores 0, however good the rest is. Check facts, maths and timings yourself where a criterion asks for accuracy.
4. Note in one sentence the most important strength or weakness.

Grade each answer on its own merits against the criteria, not by comparing lengths. Read the answers in the order given.
Do not read any files other than the ones listed. Do not run anything except to write your results.

Write your results as JSON to {out} in exactly this shape, then reply with the single word DONE:

{{"grader": "{gid}", "answers": [{{"id": "<answer id>", "task": "<request id>", "scores": [six integers], "note": "<one sentence>"}}]}}

Requests:

{blocks}
"""


def skill_index(skills_dir: Path) -> str:
    lines = ["# Skill index", "", "Each line: skill name, file, and when to use it.", ""]
    for d in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").exists()):
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        desc = next((l.split(":", 1)[1].strip() for l in text.splitlines() if l.startswith("description:")), "")
        lines.append(f"- **{d.name}** ({d / 'SKILL.md'}): {desc}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--entrants", required=True)
    ap.add_argument("--per-agent", type=int, default=6)
    ap.add_argument("--per-grader", type=int, default=3)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--only")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    work = Path(a.workdir).resolve()
    tasks = json.loads((ROOT / "tasks" / "tasks.json").read_text(encoding="utf-8"))
    if a.only:
        keep = set(a.only.split(","))
        tasks = [t for t in tasks if t["id"] in keep]
    for d in ("agents", "answers", "graders", "grades", "secret"):
        (work / d).mkdir(parents=True, exist_ok=True)
    entrants = [json.loads((ROOT / "entrants" / f"{e}.json").read_text(encoding="utf-8")) for e in a.entrants.split(",")]

    key, by_task = {}, {t["id"]: [] for t in tasks}
    agents = []
    for e in entrants:
        if e.get("skills"):
            idx = work / f"skill-index-{e['id']}.md"
            idx.write_text(skill_index((ROOT / e["skills"]).resolve()), encoding="utf-8")
            arm = ARM_SKILLS.format(index=idx)
        elif e.get("prompt"):
            arm = ARM_PROMPT.format(prompt=e["prompt"])
        else:
            arm = ARM_PLAIN
        order = tasks[:]
        rng.shuffle(order)
        for n in range(0, len(order), a.per_agent):
            reqs = []
            for t in order[n:n + a.per_agent]:
                aid = secrets.token_hex(4)
                while aid in key:
                    aid = secrets.token_hex(4)
                key[aid] = {"entrant": e["id"], "task": t["id"]}
                by_task[t["id"]].append(aid)
                reqs.append(f"## Request (write your answer to {work / 'answers' / (aid + '.md')})\n\n---\n{t['task']}\n---\n")
            name = f"{e['id']}_{n // a.per_agent + 1:02d}"
            (work / "agents" / f"{name}.md").write_text(ANSWER.format(arm=arm, requests="\n".join(reqs)), encoding="utf-8")
            agents.append({"file": f"agents/{name}.md", "model": e["model"], "entrant": e["id"]})

    batches = [tasks[i:i + a.per_grader] for i in range(0, len(tasks), a.per_grader)]
    for n, batch in enumerate(batches, 1):
        for g in ("a", "b"):
            blocks = []
            for t in batch:
                ids = by_task[t["id"]][:]
                rng.shuffle(ids)
                crit = "\n".join(f"   {i}. {c}" for i, c in enumerate(t["criteria"], 1))
                answers = "\n".join(f"   - Answer {i}: {work / 'answers' / (i + '.md')}" for i in ids)
                blocks.append(f"### Request id: {t['id']}\n\"\"\"\n{t['task']}\n\"\"\"\nCriteria:\n{crit}\nAnswers:\n{answers}\n")
            (work / "graders" / f"batch{n:02d}_{g}.md").write_text(
                GRADER.format(out=work / "grades" / f"batch{n:02d}_{g}.json", gid=f"{n:02d}{g}", blocks="\n".join(blocks)),
                encoding="utf-8")
    (work / "secret" / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    (work / "secret" / "run.json").write_text(json.dumps({"entrants": entrants, "agents": agents, "tasks": [t["id"] for t in tasks],
                                                         "seed": a.seed}, indent=1), encoding="utf-8")
    print(f"{len(tasks)} tasks, {len(entrants)} entrants, {len(agents)} answering agents, {len(batches) * 2} grader runs")


if __name__ == "__main__":
    main()
