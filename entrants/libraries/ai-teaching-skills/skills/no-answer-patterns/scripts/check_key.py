#!/usr/bin/env python3
"""Self-contained answer-pattern checker (from github.com/kal-eficia/pattern-guard, MIT).

Usage:
  check_key.py quiz.json [--fix] [--seed N]
  check_key.py --key CADBDACB [--options 4]
"""
from __future__ import annotations


import random
from dataclasses import dataclass, field
from typing import Iterable, Sequence

LETTERS = "ABCDEFGHIJ"


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str  # "fail" or "warn"
    start: int  # 0-based index of the first question involved
    length: int
    detail: str

    def where(self, unit: str = "Q") -> str:
        a, b = self.start + 1, self.start + self.length
        if unit.strip() == "item":
            return f"item {a}" if a == b else f"items {a}-{b}"
        return f"{unit}{a}" if a == b else f"{unit}{a}-{unit}{b}"


@dataclass
class Report:
    key: list[int]
    options: int
    findings: list[Finding] = field(default_factory=list)
    unit: str = "Q"
    labels: list[str] | None = None

    @property
    def ok(self) -> bool:
        return not any(f.severity == "fail" for f in self.findings)

    @property
    def clean(self) -> bool:
        return not self.findings

    def key_letters(self) -> str:
        if self.labels:
            return " ".join(self.labels[i][:3] for i in self.key)
        return "".join(LETTERS[i] for i in self.key)


def _runs(key: Sequence[int]) -> Iterable[tuple[int, int]]:
    i = 0
    while i < len(key):
        j = i
        while j + 1 < len(key) and key[j + 1] == key[i]:
            j += 1
        yield i, j - i + 1
        i = j + 1


def _longest_step_runs(key: Sequence[int], step: int) -> Iterable[tuple[int, int]]:
    i = 0
    while i < len(key) - 1:
        j = i
        while j + 1 < len(key) and key[j + 1] - key[j] == step:
            j += 1
        if j > i:
            yield i, j - i + 1
            i = j
        else:
            i += 1


def _alternations(key: Sequence[int]) -> Iterable[tuple[int, int]]:
    """Stretches like A B A B (two values, strictly alternating)."""
    i = 0
    while i < len(key) - 3:
        a, b = key[i], key[i + 1]
        if a == b:
            i += 1
            continue
        j = i + 1
        while j + 1 < len(key) and key[j + 1] == (a if (j + 1 - i) % 2 == 0 else b):
            j += 1
        length = j - i + 1
        if length >= 4:
            yield i, length
            i = j
        else:
            i += 1


def _cycles(key: Sequence[int], options: int) -> Iterable[tuple[int, int, int]]:
    """Repeating blocks like A C B | A C B (period 3+, at least two full turns)."""
    n = len(key)
    for period in range(3, max(3, options) + 2):
        i = 0
        while i + 2 * period <= n:
            block = key[i : i + period]
            if len(set(block)) < 2:
                i += 1
                continue
            j = i + period
            while j < n and key[j] == key[j - period]:
                j += 1
            if j - i >= 2 * period:
                yield i, j - i, period
                i = j
            else:
                i += 1


def analyse(key: Sequence[int], options: int, strict: bool = True) -> Report:
    """Check a correct-answer key (0-based positions) for guessable patterns.

    strict=True also fails on any back-to-back repeat (A A), which is the
    house standard for lesson pages. strict=False only fails on runs of 3+.
    """
    key = list(key)
    rep = Report(key=key, options=options)
    add = rep.findings.append

    for start, length in _runs(key):
        if length >= 3:
            add(Finding("run", "fail", start, length, f"{LETTERS[key[start]]} is correct {length} times in a row"))
        elif length == 2:
            add(Finding("repeat", "fail" if strict else "warn", start, 2, f"{LETTERS[key[start]]} twice in a row"))

    for step, word in ((1, "climbs"), (-1, "falls")):
        for start, length in _longest_step_runs(key, step):
            if length >= 3:
                seq = " ".join(LETTERS[k] for k in key[start : start + length])
                add(Finding("staircase", "fail", start, length, f"key {word} in order: {seq}"))

    for start, length in _alternations(key):
        seq = " ".join(LETTERS[k] for k in key[start : start + length])
        add(Finding("alternation", "fail", start, length, f"key alternates: {seq}"))

    for start, length, period in _cycles(key, options):
        block = " ".join(LETTERS[k] for k in key[start : start + period])
        add(Finding("cycle", "fail", start, length, f"block [{block}] repeats"))

    n = len(key)
    if n >= 6:
        counts = [key.count(o) for o in range(options)]
        top = max(counts)
        if top / n > 0.5:
            pos = LETTERS[counts.index(top)]
            add(Finding("lopsided", "fail", 0, n, f"{pos} is correct {top} of {n} times"))
        elif top / n > max(0.4, 1.6 / options):
            pos = LETTERS[counts.index(top)]
            add(Finding("lopsided", "warn", 0, n, f"{pos} is correct {top} of {n} times"))
        if n >= 2 * options:
            unused = [LETTERS[o] for o, c in enumerate(counts) if c == 0]
            if unused:
                add(Finding("unused", "warn", 0, n, f"never correct: {', '.join(unused)}"))
    return rep


def _bad_extension(key: list[int], strict: bool) -> bool:
    """Fast incremental test: does the last element create a pattern?"""
    n = len(key)
    if n >= 2 and key[-1] == key[-2] and (strict or (n >= 3 and key[-3] == key[-1])):
        return True
    if n >= 3:
        d1, d2 = key[-1] - key[-2], key[-2] - key[-3]
        if d1 == d2 and abs(d1) == 1:
            return True
    if n >= 4 and key[-1] == key[-3] and key[-2] == key[-4] and key[-1] != key[-2]:
        return True
    for period in range(3, 6):
        if n >= 2 * period and key[-period:] == key[-2 * period : -period]:
            return True
    return False


def plan_key(length: int, options: int, seed: int | None = None, strict: bool = True,
             attempts: int = 500) -> list[int]:
    """Build a pattern-free, evenly spread key of `length` answers."""
    if options < 2:
        raise ValueError("need at least two options")
    rng = random.Random(seed)
    best: list[int] | None = None
    for _ in range(attempts):
        # balanced bag, then a constrained shuffle by backtracking
        bag = [i % options for i in range(length)]
        rng.shuffle(bag)
        key: list[int] = []
        remaining = bag[:]
        ok = _place(key, remaining, strict, rng, budget=[4000])
        if ok and analyse(key, options, strict).ok:
            rep = analyse(key, options, strict)
            if rep.clean:
                return key
            best = best or key
    if best is None:
        raise RuntimeError("could not find a pattern-free key; try strict=False or more options")
    return best


def _place(key: list[int], remaining: list[int], strict: bool, rng: random.Random, budget: list[int]) -> bool:
    if not remaining:
        return True
    budget[0] -= 1
    if budget[0] <= 0:
        return False
    tried = set()
    order = list(range(len(remaining)))
    rng.shuffle(order)
    for i in order:
        v = remaining[i]
        if v in tried:
            continue
        tried.add(v)
        key.append(v)
        if not _bad_extension(key, strict):
            rest = remaining[:i] + remaining[i + 1 :]
            if _place(key, rest, strict, rng, budget):
                return True
        key.pop()
    return False


def reorder_options(options: list, correct_index: int, target: int, rng: random.Random) -> tuple[list, int]:
    """Move the correct option to `target`, shuffling the distractors around it."""
    correct = options[correct_index]
    distractors = [o for i, o in enumerate(options) if i != correct_index]
    rng.shuffle(distractors)
    distractors.insert(target, correct)
    return distractors, target

import copy
import json
import re
from pathlib import Path
from typing import Any


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


def _print(label, rep):
    status = "clean" if rep.clean else ("warnings" if rep.ok else "PATTERN")
    print(f"{label}  {rep.key_letters()}  {status}")
    for f in rep.findings:
        print(f"  {'x' if f.severity == 'fail' else '!'} {f.rule:<11} {f.where(rep.unit):<13} {f.detail}")


if __name__ == "__main__":
    import argparse, sys
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?")
    ap.add_argument("--key")
    ap.add_argument("--options", type=int)
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    if a.key:
        k = [LETTERS.index(c) for c in a.key.upper() if c in LETTERS]
        r = analyse(k, a.options or max(k) + 1)
        _print("key", r)
        sys.exit(0 if r.ok else 1)
    data, qs = load(a.file)
    if a.fix:
        data = fix_file(data, seed=a.seed)
        Path(a.file).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"fixed {a.file}")
        qs = data["questions"] if isinstance(data, dict) else data
    bad = False
    r = check_mcq(qs)
    if r:
        _print("MCQ", r); bad |= not r.ok
    for i, q in enumerate(qs):
        if q.get("type") == "sort":
            s = check_sort(q); _print(f"sort #{i + 1}", s); bad |= not s.ok
    sys.exit(1 if bad else 0)
