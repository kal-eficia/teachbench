#!/usr/bin/env python3
"""Unblind and score a TeachBench run.

usage: score.py WORKDIR [--publish NAME]
With --publish, copies answers into runs/NAME/ (by entrant and task) and writes runs/NAME/results.json.
"""
import json
import random
import re
import shutil
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from checks import check  # noqa: E402

CODE_WEIGHT = 2  # a code check counts like one more criterion worth 2 points


def bootstrap_ci(values, n=4000, seed=7):
    rng = random.Random(seed)
    k = len(values)
    means = sorted(statistics.mean(rng.choice(values) for _ in range(k)) for _ in range(n))
    return round(means[int(0.025 * n)], 1), round(means[int(0.975 * n) - 1], 1)


def score(work: Path):
    tasks = {t["id"]: t for t in json.loads((ROOT / "tasks" / "tasks.json").read_text(encoding="utf-8"))}
    key = json.loads((work / "secret" / "key.json").read_text(encoding="utf-8"))
    run = json.loads((work / "secret" / "run.json").read_text(encoding="utf-8"))
    grades = defaultdict(list)
    for f in sorted((work / "grades").glob("*.json")):
        for g in json.loads(f.read_text(encoding="utf-8"))["answers"]:
            if g.get("id") in key and len(g.get("scores", [])) == 6:
                grades[g["id"]].append({"scores": [max(0, min(2, int(s))) for s in g["scores"]], "note": g.get("note", "")})

    rows, missing = [], []
    for aid, info in key.items():
        p = work / "answers" / f"{aid}.md"
        t = tasks[info["task"]]
        if not p.exists() or not grades.get(aid):
            missing.append((info["entrant"], info["task"], "no answer" if not p.exists() else "not graded"))
            continue
        text = p.read_text(encoding="utf-8")
        gs = grades[aid]
        crit = [statistics.mean(g["scores"][i] for g in gs) for i in range(6)]
        points, maxp = sum(crit), 12
        auto = None
        if t.get("auto"):
            auto = check(t["auto"], text)
            points += CODE_WEIGHT if auto["pass"] else 0
            maxp += CODE_WEIGHT
        rows.append({
            "id": aid, "entrant": info["entrant"], "task": t["id"], "category": t["category"], "phase": t["phase"],
            "criteria": [round(c, 2) for c in crit], "pct": round(100 * points / maxp, 1), "auto": auto,
            "words": len(text.split()), "notes": [g["note"] for g in gs],
            "grader_gap": abs(sum(gs[0]["scores"]) - sum(gs[-1]["scores"])) if len(gs) > 1 else None,
        })

    entrants = {e["id"]: e for e in run["entrants"]}
    by_entrant = defaultdict(list)
    for r in rows:
        by_entrant[r["entrant"]].append(r)
    board = []
    for eid, rs in by_entrant.items():
        pcts = [r["pct"] for r in rs]
        cats = defaultdict(list)
        for r in rs:
            cats[r["category"]].append(r["pct"])
        autos = [r["auto"] for r in rs if r["auto"]]
        board.append({
            "entrant": eid, "name": entrants[eid]["name"], "model": entrants[eid]["model"],
            "skills": entrants[eid].get("skills"), "tasks": len(rs),
            "score": round(statistics.mean(pcts), 1), "ci95": bootstrap_ci(pcts),
            "categories": {c: round(statistics.mean(v), 1) for c, v in sorted(cats.items())},
            "code_checks": {"passed": sum(1 for x in autos if x["pass"]), "total": len(autos),
                            "format_missed": sum(1 for x in autos if x["pass"] is None)},
            "median_words": int(statistics.median(r["words"] for r in rs)),
        })
    board.sort(key=lambda b: -b["score"])

    # head to head: on each task, which entrant scored higher
    per_task = defaultdict(dict)
    for r in rows:
        per_task[r["task"]][r["entrant"]] = r["pct"]
    h2h = {}
    ids = [b["entrant"] for b in board]
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            both = [v for v in per_task.values() if a in v and b in v]
            h2h[f"{a} v {b}"] = {"wins": sum(1 for v in both if v[a] > v[b] + 1),
                                 "losses": sum(1 for v in both if v[b] > v[a] + 1),
                                 "level": sum(1 for v in both if abs(v[a] - v[b]) <= 1)}
    gaps = [r["grader_gap"] for r in rows if r["grader_gap"] is not None]
    meta = {"answers_scored": len(rows), "missing": missing,
            "grader_mean_gap_points": round(statistics.mean(gaps), 2) if gaps else None,
            "graders_within_2_points": round(100 * sum(1 for g in gaps if g <= 2) / len(gaps), 1) if gaps else None}
    return {"leaderboard": board, "head_to_head": h2h, "meta": meta, "answers": rows}


def main():
    work = Path(sys.argv[1]).resolve()
    res = score(work)
    for b in res["leaderboard"]:
        print(f"{b['name']:<40} {b['score']:>5}  CI {b['ci95']}  code {b['code_checks']}  n={b['tasks']}")
    print(json.dumps(res["head_to_head"], indent=1))
    print(json.dumps(res["meta"], indent=1)[:1500])
    if "--publish" in sys.argv:
        name = sys.argv[sys.argv.index("--publish") + 1]
        out = ROOT / "runs" / name
        if out.exists():
            shutil.rmtree(out)
        for r in res["answers"]:
            d = out / "answers" / r["entrant"]
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy(work / "answers" / f"{r['id']}.md", d / f"{r['task']}.md")
        (out / "grades").mkdir(parents=True, exist_ok=True)
        for f in (work / "grades").glob("*.json"):
            shutil.copy(f, out / "grades" / f.name)
        shutil.copy(work / "secret" / "key.json", out / "grades" / "answer-key.json")
        run = json.loads((work / "secret" / "run.json").read_text(encoding="utf-8"))
        res["run"] = {"name": name, "seed": run["seed"], "entrants": run["entrants"]}
        (out / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
        print("published", out)


if __name__ == "__main__":
    main()
