"""Spaced retrieval for teachers who run recall-first lessons.

Every lesson opens with a short starter. This module decides what goes in it:
what each student is about to forget, what they keep getting wrong, and what
they have not been asked for a while, interleaved so no topic sits in a block.

It works from two plain files you already have or can export:
  * a question bank  (id, topic, question, answer)
  * an attempts log  (student, question_id, date, result)
"""
from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable

# Leitner-style boxes. A right answer moves an item up one box, a wrong answer
# sends it back to box 0. The interval is how many days before it is due again.
INTERVALS = [1, 3, 7, 14, 30, 60]


@dataclass(frozen=True)
class Question:
    id: str
    topic: str
    question: str
    answer: str = ""


@dataclass(frozen=True)
class Attempt:
    student: str
    question_id: str
    day: date
    right: bool


@dataclass
class ItemState:
    box: int = 0
    seen: int = 0
    wrong: int = 0
    last: date | None = None

    def due(self, today: date) -> date:
        if self.last is None:
            return today
        return self.last + timedelta(days=INTERVALS[min(self.box, len(INTERVALS) - 1)])

    def overdue_by(self, today: date) -> int:
        return (today - self.due(today)).days


@dataclass
class Pick:
    question: Question
    reason: str
    state: ItemState


@dataclass
class TopicTrend:
    topic: str
    baseline: float | None
    recent: float | None
    asked_baseline: int
    asked_recent: int

    @property
    def change(self) -> float | None:
        if self.baseline is None or self.recent is None:
            return None
        return self.recent - self.baseline


# ---------------------------------------------------------------- loading

def _parse_day(s: str) -> date:
    return date.fromisoformat(s.strip()[:10])


def _truthy(s: str) -> bool:
    return str(s).strip().lower() in {"1", "true", "right", "correct", "yes", "y", "✓"}


def load_bank(path: str | Path) -> dict[str, Question]:
    path = Path(path)
    if path.suffix == ".json":
        rows = json.loads(path.read_text(encoding="utf-8"))
        rows = rows["questions"] if isinstance(rows, dict) else rows
    else:
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    bank = {}
    for r in rows:
        q = Question(str(r["id"]), r.get("topic", "General"), r.get("question") or r.get("q", ""), r.get("answer", ""))
        bank[q.id] = q
    return bank


def load_log(path: str | Path) -> list[Attempt]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return [
            Attempt(r["student"].strip(), str(r["question_id"]).strip(), _parse_day(r["date"]), _truthy(r["result"]))
            for r in csv.DictReader(f)
        ]


# ---------------------------------------------------------------- state

def replay(attempts: Iterable[Attempt], student: str, until: date | None = None) -> dict[str, ItemState]:
    states: dict[str, ItemState] = defaultdict(ItemState)
    for a in sorted(attempts, key=lambda a: a.day):
        if a.student != student or (until and a.day > until):
            continue
        s = states[a.question_id]
        s.seen += 1
        s.last = a.day
        if a.right:
            s.box = min(s.box + 1, len(INTERVALS) - 1)
        else:
            s.box = 0
            s.wrong += 1
    return dict(states)


def students(attempts: Iterable[Attempt]) -> list[str]:
    return sorted({a.student for a in attempts})


# ---------------------------------------------------------------- starter

def build_starter(bank: dict[str, Question], attempts: list[Attempt], student: str, today: date,
                  size: int = 8, covered_topics: Iterable[str] | None = None,
                  new_share: float = 0.25, seed: int | None = None) -> list[Pick]:
    """Choose `size` questions for a student's next starter.

    Priority: overdue items that went wrong last time, then other overdue items,
    then never-asked questions from topics already taught, then the weakest
    items that are not yet due. The result is interleaved by topic.
    """
    rng = random.Random(seed)
    states = replay(attempts, student, until=today)
    taught = set(covered_topics) if covered_topics else {bank[q].topic for q in states if q in bank}

    due_wrong, due_right, fresh, weak = [], [], [], []
    for qid, q in bank.items():
        s = states.get(qid)
        if s is None:
            if q.topic in taught:
                fresh.append(Pick(q, "not asked yet", ItemState()))
            continue
        if s.overdue_by(today) >= 0:
            (due_wrong if s.box == 0 else due_right).append(
                Pick(q, "got it wrong last time" if s.box == 0 else f"due (box {s.box})", s))
        elif s.wrong:
            weak.append(Pick(q, f"wrong {s.wrong} of {s.seen}", s))

    due_wrong.sort(key=lambda p: (-p.state.overdue_by(today), -p.state.wrong))
    due_right.sort(key=lambda p: (p.state.box, -p.state.overdue_by(today)))
    weak.sort(key=lambda p: -(p.state.wrong / p.state.seen))
    rng.shuffle(fresh)

    n_fresh = max(1, round(size * new_share)) if fresh else 0
    picks: list[Pick] = []
    chosen: set[str] = set()

    def take(pool: list[Pick], limit: int) -> None:
        for p in pool:
            if len(picks) >= min(limit, size):
                return
            if p.question.id not in chosen:
                picks.append(p)
                chosen.add(p.question.id)

    take(due_wrong, size - n_fresh)          # what they are losing right now
    take(due_right, size - n_fresh)          # what is due for a check
    take(fresh, len(picks) + n_fresh)        # a little new retrieval from taught topics
    for pool in (due_wrong, due_right, weak, fresh):
        take(pool, size)                     # fill any space left
    return interleave(picks)


def interleave(picks: list[Pick]) -> list[Pick]:
    """Order picks so no two neighbours share a topic, where that is possible."""
    by_topic: dict[str, list[Pick]] = defaultdict(list)
    for p in picks:
        by_topic[p.question.topic].append(p)
    out: list[Pick] = []
    last = None
    while any(by_topic.values()):
        options = sorted((t for t, v in by_topic.items() if v), key=lambda t: -len(by_topic[t]))
        topic = next((t for t in options if t != last), options[0])
        out.append(by_topic[topic].pop(0))
        last = topic
    return out


# ---------------------------------------------------------------- review

def topic_trends(bank: dict[str, Question], attempts: list[Attempt], student: str,
                 baseline_end: date, recent_start: date) -> list[TopicTrend]:
    """Compare each topic's hit rate in the baseline window against the recent window."""
    base, recent = defaultdict(list), defaultdict(list)
    for a in attempts:
        if a.student != student or a.question_id not in bank:
            continue
        t = bank[a.question_id].topic
        if a.day <= baseline_end:
            base[t].append(a.right)
        if a.day >= recent_start:
            recent[t].append(a.right)
    topics = sorted(set(base) | set(recent))
    rate = lambda xs: sum(xs) / len(xs) if xs else None  # noqa: E731
    return [TopicTrend(t, rate(base[t]), rate(recent[t]), len(base[t]), len(recent[t])) for t in topics]


def six_week_review(bank, attempts, student, today: date, baseline_weeks: int = 1) -> list[TopicTrend]:
    mine = [a for a in attempts if a.student == student]
    if not mine:
        return []
    first = min(a.day for a in mine)
    return topic_trends(bank, attempts, student,
                        baseline_end=first + timedelta(weeks=baseline_weeks) - timedelta(days=1),
                        recent_start=today - timedelta(weeks=2))
