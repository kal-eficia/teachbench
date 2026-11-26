"""Answer-pattern detection and repair for multiple-choice and sort/match tasks.

Students learn the answer key faster than the content when the key has a shape.
This module finds the shapes (runs, repeats, staircases, alternation, cycles,
lopsided spreads) and can rebuild an order that has none of them.
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
