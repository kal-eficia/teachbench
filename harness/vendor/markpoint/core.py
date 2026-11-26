"""Mark short written answers against exam-style marking points.

A marking point is credited when the answer matches one of its accepted
phrasings. A phrasing is either a phrase, or a list of parts that must all
appear (in any order), where each part may list alternatives:

    {"id": "input", "label": "it takes inputs",
     "accept": ["input", [["takes", "receives"], ["signal", "value"]]]}

reads as: credit if the answer says "input" (or "inputs", or "imput"), or
if it says "takes"/"receives" and also "signal"/"value". A phrase preceded
by "not", "doesn't" and the like does not count.

The checker is deliberately plain: no model, no API, no guessing. A teacher
can read every rule and see exactly why a mark was or wasn't given.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

NEGATIONS = {"not", "no", "never", "cannot", "cant", "dont", "doesnt", "isnt", "arent", "wont", "without", "neither", "nor"}
NEGATION_WINDOW = 3  # words before a match that can cancel it
_SUFFIXES = ("ing", "ed", "es", "s", "ly")


def normalise(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().replace("'", "").replace("’", "")
    # keep clause breaks as "|" so a "not" in one clause can't cancel the next
    return re.findall(r"[a-z0-9]+|[,;.!?:]", text.replace(" but ", " , "))


def stem(word: str) -> str:
    for suf in _SUFFIXES:
        if len(word) > len(suf) + 3 and word.endswith(suf):
            word = word[: -len(suf)]
            if suf in ("ed", "ing") and len(word) > 3 and word[-1] == word[-2]:
                word = word[:-1]  # unplugged -> unplug
            return word
    return word


def close_enough(a: str, b: str) -> bool:
    """Same stem, or one typo away for longer words (students misspell)."""
    if not a[0].isalnum() or not b[0].isalnum():
        return False
    if a == b:
        return True
    a, b = stem(a), stem(b)
    if a == b:
        return True
    if min(len(a), len(b)) < 5 or abs(len(a) - len(b)) > 1:
        return False
    # Damerau-lite: allow one edit
    if len(a) == len(b):
        diffs = [i for i in range(len(a)) if a[i] != b[i]]
        if len(diffs) == 1:
            return True
        if len(diffs) == 2 and diffs[1] == diffs[0] + 1 and a[diffs[0]] == b[diffs[1]] and a[diffs[1]] == b[diffs[0]]:
            return True
        return False
    short, long_ = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(long_)):
        if long_[:i] + long_[i + 1 :] == short:
            return True
    return False


def find_phrase(tokens: list[str], phrase: str) -> list[int]:
    """Start indices where a (possibly multi-word) phrase occurs."""
    words = normalise(phrase)
    if not words:
        return []
    hits = []
    for i in range(len(tokens) - len(words) + 1):
        if all(close_enough(tokens[i + j], w) for j, w in enumerate(words)):
            hits.append(i)
    return hits


def negated(tokens: list[str], index: int) -> bool:
    for t in reversed(tokens[max(0, index - NEGATION_WINDOW):index]):
        if not t[0].isalnum():
            return False  # clause break: the negation belongs to an earlier clause
        if t in NEGATIONS:
            return True
    return False


@dataclass
class PointResult:
    id: str
    label: str
    got: bool
    evidence: str = ""
    blocked_by: str = ""


@dataclass
class Result:
    score: int
    max_marks: int
    points: list[PointResult] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    @property
    def got(self) -> list[PointResult]:
        return [p for p in self.points if p.got]

    @property
    def missing(self) -> list[PointResult]:
        return [p for p in self.points if not p.got]

    def feedback(self) -> str:
        if not self.got:
            head = "Not yet."
        elif not self.missing or self.score >= self.max_marks:
            head = "Full marks."
        else:
            head = "Good start."
        parts = [head]
        if self.got and self.missing and self.score < self.max_marks:
            parts.append("You have got: " + ", ".join(p.label for p in self.got) + ".")
        if self.missing and self.score < self.max_marks:
            parts.append("Still to add: " + ", ".join(p.label for p in self.missing) + ".")
        for f in self.flags:
            parts.append(f)
        return " ".join(parts)


def _group_hit(tokens: list[str], group: list[str]) -> tuple[int, str] | None:
    for word in group:
        for idx in find_phrase(tokens, word):
            if not negated(tokens, idx):
                return idx, word
    return None


def check_point(tokens: list[str], point: dict) -> PointResult:
    pid, label = point["id"], point.get("label", point["id"])
    for bad in point.get("forbid", []):
        hits = [i for i in find_phrase(tokens, bad) if not negated(tokens, i)]
        if hits:
            return PointResult(pid, label, False, blocked_by=bad)
    for phrasing in point.get("accept", []):
        parts = [phrasing] if isinstance(phrasing, str) else phrasing
        groups = [[p] if isinstance(p, str) else p for p in parts]
        found = []
        for group in groups:
            hit = _group_hit(tokens, group)
            if hit is None:
                break
            found.append(hit[1])
        else:
            return PointResult(pid, label, True, evidence=" + ".join(found))
    return PointResult(pid, label, False)


def mark(answer: str, question: dict) -> Result:
    tokens = normalise(answer)
    points = [check_point(tokens, p) for p in question["points"]]
    max_marks = int(question.get("marks", len(points)))
    score = min(max_marks, sum(1 for p in points if p.got))
    flags = []
    min_words = question.get("minWords")
    if min_words and len([t for t in tokens if t[0].isalnum()]) < min_words:
        flags.append(f"Write a little more: aim for at least {min_words} words.")
    for p in points:
        if p.blocked_by:
            flags.append(f'Check "{p.blocked_by}": that isn\'t right here.')
    return Result(score, max_marks, points, flags)
