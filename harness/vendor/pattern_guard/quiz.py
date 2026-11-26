"""Load, check and repair quiz files.

Accepted JSON shapes
--------------------
A list of questions, or {"questions": [...]} with any extra keys kept as-is.

Multiple choice:  {"q": "...", "options": ["...", "..."], "answer": 2}
                  "answer" may be the option index or the option text.
Sort / match:     {"type": "sort", "items": [{"text": "...", "bucket": "Input"}, ...]}
"""
from __future__ import annotations

import copy
import json
import random
import re
from pathlib import Path
from typing import Any

from .core import LETTERS, Report, _bad_extension, analyse, plan_key, reorder_options


def load(path: str | Path) -> tuple[Any, list[dict]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    questions = data["questions"] if isinstance(data, dict) else data
    return data, questions


def answer_index(q: dict) -> int:
    ans, opts = q["answer"], q["options"]
    if isinstance(ans, int):
        if not 0 <= ans < len(opts):
            raise ValueError(f"answer index {ans} out of range in: {q.get('q', '')[:60]}")
        return ans
    if isinstance(ans, str) and len(ans) == 1 and ans.upper() in LETTERS[: len(opts)] and ans not in opts:
        return LETTERS.index(ans.upper())
    try:
        return opts.index(ans)
    except ValueError:
        raise ValueError(f"answer {ans!r} is not one of the options in: {q.get('q', '')[:60]}") from None


def mcq_items(questions: list[dict]) -> list[dict]:
    return [q for q in questions if "options" in q]


def check_mcq(questions: list[dict], strict: bool = True) -> Report | None:
    mcqs = mcq_items(questions)
    if not mcqs:
        return None
    key = [answer_index(q) for q in mcqs]
    width = max(len(q["options"]) for q in mcqs)
    return analyse(key, width, strict)


def check_sort(task: dict, strict: bool = False) -> Report:
    buckets: list[str] = []
    for it in task["items"]:
        if it["bucket"] not in buckets:
            buckets.append(it["bucket"])
    key = [buckets.index(it["bucket"]) for it in task["items"]]
    rep = analyse(key, len(buckets), strict)
    rep.unit, rep.labels = "item ", buckets
    fixed = []
    for f in rep.findings:
        if f.rule == "unused":
            continue
        detail = f.detail.replace(" is correct ", " items ")
        for i, b in enumerate(buckets):
            detail = re.sub(rf"\b{LETTERS[i]}\b", b, detail)
        fixed.append(type(f)(f.rule, f.severity, f.start, f.length, detail))
    rep.findings = fixed
    return rep


PINNED_RE = re.compile(
    r"^\s*(all|none|both|neither)\b.*\b(above|these|them|of the options)\b|^\s*(all|none) of (the above|these|them)\s*$"
    r"|^\s*both [a-d] and [a-d]\s*$|^\s*[a-d] and [a-d]( only)?\s*$",
    re.IGNORECASE,
)


def pinned_slots(options: list) -> set[int]:
    """Positions that must not move: "All of the above", "None of these", "A and B" and similar."""
    return {i for i, o in enumerate(options) if isinstance(o, str) and PINNED_RE.search(o)}


def _plan_constrained(allowed: list[list[int]], width: int, seed: int | None, strict: bool,
                      attempts: int = 400) -> list[int]:
    """Pattern-free key where position i may only take values in allowed[i]."""
    rng = random.Random(seed)
    best = None
    for _ in range(attempts):
        key: list[int] = []
        counts = [0] * width
        budget = [5000]

        def place(i: int) -> bool:
            if i == len(allowed):
                return True
            budget[0] -= 1
            if budget[0] <= 0:
                return False
            choices = allowed[i][:]
            rng.shuffle(choices)
            choices.sort(key=lambda v: counts[v])  # keep the spread even
            for v in choices:
                key.append(v)
                counts[v] += 1
                if not _bad_extension(key, strict) and place(i + 1):
                    return True
                key.pop()
                counts[v] -= 1
            return False

        if place(0):
            rep = analyse(key, width, strict)
            if rep.clean:
                return key
            if rep.ok and best is None:
                best = key[:]
    if best is None:
        raise RuntimeError("could not find a pattern-free key with these fixed options; reword one")
    return best


def fix_mcq(questions: list[dict], seed: int | None = None, strict: bool = True) -> list[dict]:
    """Reorder options so the key has no pattern. Options such as "All of the above"
    keep their position; if one of them is the answer, that question's position is fixed."""
    out = copy.deepcopy(questions)
    mcqs = [q for q in out if "options" in q]
    if not mcqs:
        return out
    rng = random.Random(seed)
    width = min(len(q["options"]) for q in mcqs)  # every target must exist in every question
    allowed = []
    for q in mcqs:
        idx = answer_index(q)
        pins = pinned_slots(q["options"])
        if idx in pins:
            allowed.append([idx])
        else:
            free = [i for i in range(width) if i not in pins]
            allowed.append(free or [idx])
    target_key = _plan_constrained(allowed, width, seed, strict)
    for q, target in zip(mcqs, target_key):
        idx = answer_index(q)
        as_text = not isinstance(q["answer"], int)
        opts = q["options"]
        pins = pinned_slots(opts)
        if idx in pins:
            free = [i for i in range(len(opts)) if i not in pins]
            movers = [opts[i] for i in free]
            rng.shuffle(movers)
            new_opts = opts[:]
            for slot, o in zip(free, movers):
                new_opts[slot] = o
            new = idx
        else:
            correct = opts[idx]
            free = [i for i in range(len(opts)) if i not in pins]
            others = [opts[i] for i in free if i != idx]
            rng.shuffle(others)
            new_opts = opts[:]
            it = iter(others)
            for slot in free:
                new_opts[slot] = correct if slot == target else next(it)
            new = target
        q["options"] = new_opts
        q["answer"] = new_opts[new] if as_text else new
    return out


def fix_sort(task: dict, seed: int | None = None) -> dict:
    out = copy.deepcopy(task)
    rng = random.Random(seed)
    buckets: dict[str, list] = {}
    for it in out["items"]:
        buckets.setdefault(it["bucket"], []).append(it)
    names = list(buckets)
    for v in buckets.values():
        rng.shuffle(v)
    counts = {k: len(v) for k, v in buckets.items()}
    best, best_score = None, None
    for _ in range(600):
        bag = [names.index(k) for k, c in counts.items() for _ in range(c)]
        rng.shuffle(bag)
        rep = analyse(bag, len(names), strict=False)
        if not rep.ok:
            continue
        score = len(rep.findings)
        if best_score is None or score < best_score:
            best, best_score = bag, score
            if score == 0:
                break
    if best is None:
        raise RuntimeError("could not reorder sort items without a pattern")
    pools = {k: list(v) for k, v in buckets.items()}
    out["items"] = [pools[names[b]].pop() for b in best]
    return out


def fix_file(data: Any, seed: int | None = None, strict: bool = True) -> Any:
    questions = data["questions"] if isinstance(data, dict) else data
    fixed = fix_mcq(questions, seed=seed, strict=strict)
    fixed = [fix_sort(q, seed=seed) if q.get("type") == "sort" else q for q in fixed]
    if isinstance(data, dict):
        data = dict(data)
        data["questions"] = fixed
        return data
    return fixed
