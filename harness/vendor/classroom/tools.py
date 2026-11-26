"""Classroom tools: the checks and builders the teaching skills rely on.

Every tool is a plain function taking keyword arguments and returning a
JSON-serialisable dict. No network, no AI model, standard library only.
"""
from __future__ import annotations

import csv
import html
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from markpoint import mark
from pattern_guard import analyse, check_mcq, check_sort, fix_file, plan_key
from pattern_guard.core import LETTERS
from pattern_guard.quiz import answer_index, pinned_slots
from recall_engine import Attempt, Question, build_starter, load_bank, load_log, six_week_review, students

VENDOR = Path(__file__).resolve().parent.parent / "vendor"


class ToolError(ValueError):
    """A problem with the caller's input, reported back as a readable message."""


# ------------------------------------------------------------------ helpers

def _read_json(path: str) -> Any:
    p = Path(path).expanduser()
    if not p.exists():
        raise ToolError(f"file not found: {path}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ToolError(f"{path} is not valid JSON: {e}") from None


def _questions(questions=None, quiz_path=None) -> tuple[Any, list[dict]]:
    if questions is None and quiz_path is None:
        raise ToolError("give either questions or quiz_path")
    data = questions if questions is not None else _read_json(quiz_path)
    qs = data["questions"] if isinstance(data, dict) else data
    if not isinstance(qs, list):
        raise ToolError("questions must be a list (or an object with a 'questions' list)")
    return data, qs


def _report(rep, label: str) -> dict:
    return {
        "set": label,
        "key": rep.key_letters(),
        "status": "clean" if rep.clean else ("warnings" if rep.ok else "pattern"),
        "findings": [
            {"rule": f.rule, "severity": f.severity, "where": f.where(rep.unit), "detail": f.detail}
            for f in rep.findings
        ],
    }


def _check_all(qs: list[dict]) -> list[dict]:
    out = []
    try:
        rep = check_mcq(qs)
    except (ValueError, KeyError) as e:
        raise ToolError(f"could not read the questions: {e}") from None
    if rep is not None:
        out.append(_report(rep, "multiple choice"))
    for i, q in enumerate(qs):
        if q.get("type") == "sort":
            out.append(_report(check_sort(q), f"sort task {q.get('id', i + 1)}"))
    return out


def _today(today: str | None) -> date:
    if not today:
        return date.today()
    try:
        return date.fromisoformat(today)
    except ValueError:
        raise ToolError(f"today must be YYYY-MM-DD, got {today!r}") from None


def _bank(bank) -> dict[str, Question]:
    if isinstance(bank, str):
        if not Path(bank).expanduser().exists():
            raise ToolError(f"question bank not found: {bank}")
        return load_bank(Path(bank).expanduser())
    out = {}
    for r in bank or []:
        if "id" not in r:
            raise ToolError("every bank question needs an id")
        q = Question(str(r["id"]), r.get("topic", "General"), r.get("question") or r.get("q", ""), r.get("answer", ""))
        out[q.id] = q
    if not out:
        raise ToolError("the question bank is empty")
    return out


def _truthy(v) -> bool:
    return v is True or str(v).strip().lower() in {"1", "true", "right", "correct", "yes", "y"}


def _log(log) -> list[Attempt]:
    if isinstance(log, str):
        p = Path(log).expanduser()
        return load_log(p) if p.exists() else []
    out = []
    for r in log or []:
        try:
            out.append(Attempt(str(r["student"]).strip(), str(r["question_id"]).strip(),
                               date.fromisoformat(str(r["date"])[:10]), _truthy(r["result"])))
        except (KeyError, ValueError) as e:
            raise ToolError(f"bad attempt row {r}: {e}") from None
    return out


# ------------------------------------------------------------ answer keys

def check_answer_key(key: str | None = None, options: int | None = None,
                     questions=None, quiz_path: str | None = None) -> dict:
    """Check a bare key (e.g. "CADB") or a set of questions for guessable patterns."""
    if key:
        letters = [c for c in key.upper() if c.isalpha()]
        bad = [c for c in letters if c not in LETTERS]
        if bad or not letters:
            raise ToolError("key must be letters A to J, for example CADBDACB")
        k = [LETTERS.index(c) for c in letters]
        rep = analyse(k, options or max(max(k) + 1, 2))
        reports = [_report(rep, "key")]
    else:
        _, qs = _questions(questions, quiz_path)
        reports = _check_all(qs)
        if not reports:
            raise ToolError("no multiple-choice questions or sort tasks found")
    ok = all(r["status"] != "pattern" for r in reports)
    return {"ok": ok, "reports": reports,
            "summary": "No answer patterns." if ok else "Answer patterns found: fix before giving this to students."}


def fix_answer_key(questions=None, quiz_path: str | None = None, seed: int | None = None,
                   write: bool = False) -> dict:
    """Reorder options (and sort items) so the key has no pattern. Wording never changes."""
    data, qs = _questions(questions, quiz_path)
    before = _check_all(qs)
    try:
        fixed = fix_file(data, seed=seed)
    except (RuntimeError, ValueError, KeyError) as e:
        raise ToolError(str(e)) from None
    fixed_qs = fixed["questions"] if isinstance(fixed, dict) else fixed
    after = _check_all(fixed_qs)
    for old, new in zip([q for q in qs if "options" in q], [q for q in fixed_qs if "options" in q]):
        if old["options"][answer_index(old)] != new["options"][answer_index(new)]:
            raise ToolError("internal error: an answer changed during reordering")  # pragma: no cover
    out = {"before": before, "after": after, "questions": fixed,
           "ok": all(r["status"] != "pattern" for r in after)}
    if write:
        if not quiz_path:
            raise ToolError("write=true needs quiz_path")
        Path(quiz_path).expanduser().write_text(json.dumps(fixed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out["written_to"] = quiz_path
    return out


def plan_answer_key(length: int, options: int = 4, seed: int | None = None) -> dict:
    """Plan a pattern-free, evenly spread key before writing the questions."""
    if not 1 <= int(length) <= 200:
        raise ToolError("length must be between 1 and 200")
    if not 2 <= int(options) <= 10:
        raise ToolError("options must be between 2 and 10")
    try:
        k = plan_key(int(length), int(options), seed=seed)
    except RuntimeError as e:
        raise ToolError(str(e)) from None
    letters = "".join(LETTERS[i] for i in k)
    return {"key": letters, "positions": [i + 1 for i in k], "spread": dict(sorted(Counter(letters).items()))}


# ------------------------------------------------------------ retrieval

def recall_starter(bank, log=None, student: str | None = None, size: int = 8, today: str | None = None,
                   covered_topics: list[str] | None = None, seed: int | None = None,
                   show_answers: bool = True) -> dict:
    """Pick a spaced, interleaved starter for one student from a bank and an attempts log."""
    b, attempts = _bank(bank), _log(log)
    known = students(attempts)
    if not student:
        if len(known) == 1:
            student = known[0]
        elif not known:
            student = "class"
        else:
            raise ToolError(f"say which student: {', '.join(known)}")
    if not covered_topics and student not in known:
        covered_topics = sorted({q.topic for q in b.values()})
    picks = build_starter(b, attempts, student, _today(today), size=int(size),
                          covered_topics=covered_topics, seed=seed)
    return {
        "student": student,
        "date": _today(today).isoformat(),
        "questions": [
            {"n": i + 1, "id": p.question.id, "topic": p.question.topic, "question": p.question.question,
             **({"answer": p.question.answer} if show_answers else {}), "why_chosen": p.reason}
            for i, p in enumerate(picks)
        ],
        "note": None if picks else "No questions could be chosen: check the bank and the covered topics.",
    }


def progress_review(bank, log, student: str | None = None, today: str | None = None,
                    baseline_weeks: int = 1) -> dict:
    """Compare a student's first week(s) with their last two weeks, topic by topic."""
    b, attempts = _bank(bank), _log(log)
    known = students(attempts)
    if not known:
        raise ToolError("the attempts log is empty")
    if not student:
        if len(known) != 1:
            raise ToolError(f"say which student: {', '.join(known)}")
        student = known[0]
    if student not in known:
        raise ToolError(f"no attempts for {student!r}. Students in the log: {', '.join(known)}")
    trends = six_week_review(b, attempts, student, _today(today), baseline_weeks=int(baseline_weeks))
    pct = lambda x: None if x is None else round(x * 100)  # noqa: E731
    rows = [{"topic": t.topic, "baseline_pct": pct(t.baseline), "recent_pct": pct(t.recent),
             "change_points": pct(t.change), "asked_baseline": t.asked_baseline, "asked_recent": t.asked_recent}
            for t in trends]
    moved = sorted((r for r in rows if r["change_points"] is not None), key=lambda r: r["change_points"])
    return {
        "student": student,
        "topics": rows,
        "biggest_gain": moved[-1]["topic"] if moved and moved[-1]["change_points"] > 0 else None,
        "needs_attention": [r["topic"] for r in rows
                            if r["recent_pct"] is not None and r["recent_pct"] < 60][:3],
        "not_comparable": [r["topic"] for r in rows if r["change_points"] is None],
        "caution": "Topics with fewer than 3 questions in either window are weak evidence.",
    }


def log_attempts(log_path: str, attempts: list[dict], today: str | None = None) -> dict:
    """Append quiz results to the attempts log (CSV), creating it if needed."""
    if not attempts:
        raise ToolError("no attempts given")
    p = Path(log_path).expanduser()
    rows = []
    for r in attempts:
        try:
            rows.append([str(r["student"]).strip(), str(r["question_id"]).strip(),
                         str(r.get("date") or _today(today).isoformat())[:10],
                         "right" if _truthy(r["result"]) else "wrong"])
        except KeyError as e:
            raise ToolError(f"attempt {r} is missing {e}") from None
        date.fromisoformat(rows[-1][2])
    new = not p.exists() or p.stat().st_size == 0
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["student", "question_id", "date", "result"])
        w.writerows(rows)
    return {"appended": len(rows), "log_path": str(p), "students": sorted({r[0] for r in rows})}


# ------------------------------------------------------------ marking

def mark_answers(answers: list, question: dict | None = None, questions_path: str | None = None,
                 question_id: str | None = None) -> dict:
    """Mark short answers against marking points. Borderline answers are flagged for the teacher."""
    if question is None:
        if not questions_path:
            raise ToolError("give a question (with points) or questions_path and question_id")
        data = _read_json(questions_path)
        qs = data["questions"] if isinstance(data, dict) else data
        matches = [q for q in qs if str(q.get("id")) == str(question_id)] if question_id else qs[:1]
        if not matches:
            raise ToolError(f"no question with id {question_id!r} in {questions_path}")
        question = matches[0]
    if not question.get("points"):
        raise ToolError("the question needs a 'points' list (id, label, accept)")
    results = []
    for i, a in enumerate(answers or []):
        who, text = (a.get("student", f"#{i + 1}"), a.get("answer", "")) if isinstance(a, dict) else (f"#{i + 1}", a)
        r = mark(str(text), question)
        blocked = [p.blocked_by for p in r.points if p.blocked_by]
        results.append({
            "student": who, "score": r.score, "out_of": r.max_marks,
            "awarded": [{"point": p.label, "evidence": p.evidence} for p in r.got],
            "missing": [p.label for p in r.missing],
            "feedback": r.feedback(),
            "teacher_check": bool(blocked) or (0 < r.score < r.max_marks and len(str(text).split()) > 40),
        })
    if not results:
        raise ToolError("no answers given")
    scores = [r["score"] for r in results]
    missed = Counter(m for r in results for m in r["missing"])
    return {
        "question": question.get("q") or question.get("question", ""),
        "results": results,
        "class_summary": {
            "answers": len(results), "mean": round(sum(scores) / len(scores), 2), "out_of": results[0]["out_of"],
            "most_missed_points": [{"point": p, "missed_by": n} for p, n in missed.most_common(3)],
        },
        "note": "Keyword marking is a first pass. Check anything marked teacher_check, and skim the rest.",
    }


# ------------------------------------------------------------ lesson pages

TEACHER_VOICE = re.compile(
    r"\b(students (should|will|must|can)|learners (should|will)|the teacher|teacher note|ask (the )?students|"
    r"pupils (should|will)|lesson objective|success criteria for the teacher|misconception:)", re.I)
BLOCK_TYPES = {"text", "note", "mcq", "sort", "write"}


def _texts(block: dict):
    for k in ("heading", "q", "prompt", "why", "hint"):
        if isinstance(block.get(k), str):
            yield block[k]
    body = block.get("body")
    if isinstance(body, str):
        yield body
    elif isinstance(body, list):
        yield from (b for b in body if isinstance(b, str))
    for o in block.get("options", []):
        if isinstance(o, str):
            yield o
    for it in block.get("items", []):
        if isinstance(it, dict) and isinstance(it.get("text"), str):
            yield it["text"]


def validate_lesson(lesson: dict | None = None, lesson_path: str | None = None) -> dict:
    """Check a lesson-page-kit lesson before it reaches students."""
    if lesson is None:
        if not lesson_path:
            raise ToolError("give lesson or lesson_path")
        lesson = _read_json(lesson_path)
    errors, warnings = [], []
    if not lesson.get("title"):
        errors.append("lesson has no title")
    pages = lesson.get("pages")
    if not isinstance(pages, list) or not pages:
        return {"ok": False, "errors": errors + ["lesson has no pages"], "warnings": warnings, "stats": {}}
    seen: set[str] = set()
    counts = Counter()
    for pi, page in enumerate(pages, 1):
        where_p = f"page {pi}"
        if not page.get("title"):
            warnings.append(f"{where_p}: no title")
        blocks = page.get("blocks") or []
        if not blocks:
            errors.append(f"{where_p}: no blocks")
        if not any(b.get("type") in {"mcq", "sort", "write"} for b in blocks):
            warnings.append(f"{where_p}: nothing for the student to answer, so its summary will be empty")
        for bi, b in enumerate(blocks, 1):
            where = f"{where_p}, block {bi}"
            t = b.get("type")
            if t not in BLOCK_TYPES:
                errors.append(f"{where}: unknown type {t!r} (use text, note, mcq, sort or write)")
                continue
            counts[t] += 1
            if t in {"mcq", "sort", "write"}:
                bid = b.get("id")
                if not bid:
                    errors.append(f"{where}: {t} block needs an id")
                elif bid in seen:
                    errors.append(f"{where}: id {bid!r} is used twice")
                seen.add(bid)
            if t == "mcq":
                opts = b.get("options") or []
                if not b.get("q"):
                    errors.append(f"{where}: mcq has no question")
                if len(opts) < 3:
                    errors.append(f"{where}: mcq needs at least 3 options")
                if not isinstance(b.get("answer"), int) or not 0 <= b["answer"] < max(len(opts), 1):
                    errors.append(f"{where}: mcq answer must be the index of the correct option")
                if len(set(map(str, opts))) != len(opts):
                    errors.append(f"{where}: two options are identical")
                if not b.get("why"):
                    warnings.append(f"{where}: no 'why', so students get no explanation after answering")
            elif t == "sort":
                buckets, items = b.get("buckets") or [], b.get("items") or []
                if len(buckets) < 2:
                    errors.append(f"{where}: sort needs at least 2 buckets")
                if len(items) < 4:
                    warnings.append(f"{where}: fewer than 4 sort items is easy to guess")
                for it in items:
                    if it.get("bucket") not in buckets:
                        errors.append(f"{where}: item {it.get('text', '?')!r} has a bucket that isn't listed")
                used = Counter(it.get("bucket") for it in items)
                for bk in buckets:
                    if not used.get(bk):
                        warnings.append(f"{where}: bucket {bk!r} has no items")
            elif t == "write":
                if not b.get("prompt"):
                    errors.append(f"{where}: write block has no prompt")
            for text in _texts(b):
                if "—" in text:
                    warnings.append(f"{where}: em dash in student text")
                m = TEACHER_VOICE.search(text)
                if m:
                    warnings.append(f"{where}: reads like a teacher note ({m.group(0)!r}); student pages talk to the student")
    if counts["mcq"] and counts["mcq"] < 3:
        warnings.append("fewer than 3 multiple-choice questions: too few for the answer key to be mixed up well")
    return {"ok": not errors, "errors": errors, "warnings": warnings,
            "stats": {"pages": len(pages), **{k: counts[k] for k in sorted(counts)}}}


PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<div data-lesson="lesson"{endpoint}></div>
<script type="application/json" id="lesson">
{lesson}
</script>
<script>
{js}
</script>
</body>
</html>
"""


def build_lesson_page(out_path: str, lesson: dict | None = None, lesson_path: str | None = None,
                      endpoint: str | None = None, allow_warnings: bool = True) -> dict:
    """Validate a lesson and write one self-contained student page (HTML) that works offline."""
    if lesson is None:
        if not lesson_path:
            raise ToolError("give lesson or lesson_path")
        lesson = _read_json(lesson_path)
    check = validate_lesson(lesson=lesson)
    if not check["ok"] or (check["warnings"] and not allow_warnings):
        return {"built": False, **check, "note": "Fix these and build again."}
    if endpoint and not re.match(r"^https://[^\s\"'<>]+$", endpoint):
        raise ToolError("endpoint must be an https:// address")
    out = Path(out_path).expanduser()
    if out.suffix.lower() != ".html":
        raise ToolError("out_path must end in .html")
    payload = json.dumps(lesson, ensure_ascii=False, indent=1).replace("</", "<\\/")
    page = PAGE.format(
        title=html.escape(str(lesson.get("title", "Lesson"))),
        css=(VENDOR / "lesson_kit" / "lesson-kit.css").read_text(encoding="utf-8"),
        js=(VENDOR / "lesson_kit" / "lesson-kit.js").read_text(encoding="utf-8").replace("</script", "<\\/script"),
        lesson=payload,
        endpoint=f' data-endpoint="{html.escape(endpoint)}"' if endpoint else "",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return {"built": True, "out_path": str(out), "bytes": len(page.encode("utf-8")), **check,
            "note": "Open the file in a browser. Answer options are mixed up on the page so the key has no pattern."}


# ------------------------------------------------------------ writing checks

JARGON = ["AO1", "AO2", "AO3", "WTS", "EXS", "GDS", "working towards", "working at", "greater depth",
          "pleasure to teach", "a joy to teach", "needs to try harder", "lazy", "chatty", "disruptive",
          "must try harder", "could do better", "retrieval", "interleav", "metacogn", "scaffold"]
_SENT = re.compile(r"(?<=[.!?])\s+")


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT.split(text.strip()) if s.strip()]


def _norm(s: str, names: list[str]) -> str:
    s = s.lower()
    for n in names:
        s = re.sub(rf"\b{re.escape(n.lower())}\b", "<name>", s)
    s = re.sub(r"\[[^\]]+\]", "<name>", s)
    s = re.sub(r"\b(he|she|they)\b", "<p>", s)
    s = re.sub(r"\b(his|her|their)\b", "<pp>", s)
    return re.sub(r"[^a-z0-9<> ]+", "", s).strip()


def check_reports(reports: list[dict], min_words: int = 60, max_words: int = 90,
                  extra_banned: list[str] | None = None) -> dict:
    """Check a batch of student reports: length, repeated wording, jargon and shape."""
    if not reports:
        raise ToolError("no reports given")
    names = [str(r.get("student", "")) for r in reports if r.get("student")]
    first_names = [n.split()[0] for n in names if n and not n.startswith("[")]
    seen_sent: dict[str, str] = {}
    seen_open: dict[str, str] = {}
    out, issues_total = [], 0
    banned = JARGON + list(extra_banned or [])
    for r in reports:
        who, text = str(r.get("student", "?")), str(r.get("text", ""))
        issues = []
        n = len(text.split())
        if n < min_words:
            issues.append(f"{n} words: under the minimum of {min_words}")
        if n > max_words:
            issues.append(f"{n} words: over the limit of {max_words}")
        sents = _sentences(text)
        if len(sents) < 3:
            issues.append("fewer than 3 sentences: a strength, a next step and a positive close need room")
        for s in sents:
            key = _norm(s, first_names)
            if len(key.split()) >= 5 and key in seen_sent and seen_sent[key] != who:
                issues.append(f"sentence repeated from {seen_sent[key]}: {s[:70]!r}")
            seen_sent.setdefault(key, who)
        if sents:
            opening = " ".join(_norm(sents[0], first_names).split()[:4])
            if opening in seen_open and seen_open[opening] != who:
                issues.append(f"opens the same way as {seen_open[opening]}: {' '.join(sents[0].split()[:5])!r}")
            seen_open.setdefault(opening, who)
        low = text.lower()
        for j in banned:
            if re.search(rf"(?<![a-z]){re.escape(j.lower())}", low):
                issues.append(f"jargon or label to avoid: {j!r}")
        if "—" in text:
            issues.append("em dash")
        if not re.search(r"\b(next|now|will|step|practi[sc]e|to improve|focus|working on|aim)\b", low):
            issues.append("no clear next step found")
        issues_total += len(issues)
        out.append({"student": who, "words": n, "ok": not issues, "issues": issues})
    return {"ok": issues_total == 0, "reports": out,
            "summary": f"{sum(1 for o in out if o['ok'])} of {len(out)} reports pass every check."}


_VOWELS = re.compile(r"[aeiouy]+")


def _syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n = len(_VOWELS.findall(w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(1, n)


def text_stats(text: str, target_age: int | None = None, max_words: int | None = None) -> dict:
    """Word count and reading level for a text, with the sentences and words that make it hard."""
    words = re.findall(r"[A-Za-z0-9'’-]+", text)
    sents = _sentences(text) or ([text] if text.strip() else [])
    if not words:
        raise ToolError("no text given")
    syl = sum(_syllables(w) for w in words)
    wps = len(words) / max(len(sents), 1)
    grade = 0.39 * wps + 11.8 * (syl / len(words)) - 15.59
    reading_age = round(max(5.0, grade + 5), 1)
    long_sents = [s for s in sents if len(s.split()) > 25]
    hard = Counter(w.lower() for w in words if _syllables(w) >= 4 and len(w) > 8)
    out = {
        "words": len(words), "sentences": len(sents), "words_per_sentence": round(wps, 1),
        "reading_age_estimate": reading_age,
        "long_sentences": [s[:120] for s in long_sents[:5]],
        "hard_words": [w for w, _ in hard.most_common(12)],
        "note": "Reading age is a rough Flesch-Kincaid estimate. Subject words students must learn are fine to keep.",
    }
    if target_age is not None:
        out["target_age"] = target_age
        out["on_target"] = reading_age <= target_age + 1
    if max_words is not None:
        out["max_words"] = max_words
        out["within_limit"] = len(words) <= max_words
    return out


# ------------------------------------------------------------ registry

def _schema(props: dict, required: list[str] | None = None) -> dict:
    return {"type": "object", "properties": props, "required": required or [], "additionalProperties": False}


_QUESTIONS = {"description": "List of questions, or an object with a 'questions' list. Multiple choice: "
              "{q, options, answer} where answer is the option index or the option text. Sort task: "
              "{type:'sort', items:[{text, bucket}]}.", "type": ["array", "object"], "items": {"type": "object"}}
_BANK = {"description": "Path to a CSV or JSON question bank (columns: id, topic, question, answer), "
         "or the rows inline as a list.", "type": ["string", "array"], "items": {"type": "object"}}
_LOG = {"description": "Path to the attempts CSV (columns: student, question_id, date, result), "
        "or the rows inline as a list.", "type": ["string", "array"], "items": {"type": "object"}}
_SEED = {"type": "integer", "description": "Optional seed for a repeatable result."}
_TODAY = {"type": "string", "description": "Date to treat as today, YYYY-MM-DD. Defaults to the real date."}

TOOLS: dict[str, dict] = {
    "check_answer_key": {
        "fn": check_answer_key,
        "description": "Check a quiz's correct-answer positions for patterns students can guess (repeats, runs, "
                       "A-B-C-D staircases, alternation, repeating blocks, lopsided spread). Give a bare key such "
                       "as 'CADBDACB', or the questions themselves. Always run this on any multiple-choice set or "
                       "sort task before it reaches students.",
        "schema": _schema({
            "key": {"type": "string", "description": "Correct answers as letters, e.g. CADBDACB."},
            "options": {"type": "integer", "description": "Options per question, when checking a bare key."},
            "questions": _QUESTIONS,
            "quiz_path": {"type": "string", "description": "Path to a quiz JSON file."}}),
    },
    "fix_answer_key": {
        "fn": fix_answer_key,
        "description": "Reorder answer options and sort items so the key has no guessable pattern. Wording is never "
                       "changed, answers stay correct, and options like 'All of the above' stay in place. Returns "
                       "the reordered questions with before and after reports.",
        "schema": _schema({"questions": _QUESTIONS,
                           "quiz_path": {"type": "string", "description": "Path to a quiz JSON file."},
                           "seed": _SEED,
                           "write": {"type": "boolean", "description": "Write the result back to quiz_path."}}),
    },
    "plan_answer_key": {
        "fn": plan_answer_key,
        "description": "Plan a pattern-free, evenly spread answer key BEFORE writing a quiz, so each question's "
                       "correct option can be written straight into its planned position.",
        "schema": _schema({"length": {"type": "integer", "description": "Number of questions."},
                           "options": {"type": "integer", "description": "Options per question (default 4)."},
                           "seed": _SEED}, ["length"]),
    },
    "recall_starter": {
        "fn": recall_starter,
        "description": "Choose a spaced, interleaved retrieval starter for one student from a question bank and "
                       "an attempts log: recently wrong first, then due for a check, then not asked yet. Each "
                       "question comes with the reason it was chosen.",
        "schema": _schema({"bank": _BANK, "log": _LOG,
                           "student": {"type": "string", "description": "Student id or initials as used in the log."},
                           "size": {"type": "integer", "description": "Number of questions (default 8)."},
                           "today": _TODAY,
                           "covered_topics": {"type": "array", "items": {"type": "string"},
                                              "description": "Topics taught so far. Defaults to topics already attempted."},
                           "seed": _SEED,
                           "show_answers": {"type": "boolean", "description": "Include answers (default true)."}},
                          ["bank"]),
    },
    "progress_review": {
        "fn": progress_review,
        "description": "Six-week style review for one student: hit rate per topic in their first week(s) against "
                       "their last two weeks, with the biggest gain and the topics that still need attention.",
        "schema": _schema({"bank": _BANK, "log": _LOG, "student": {"type": "string"}, "today": _TODAY,
                           "baseline_weeks": {"type": "integer", "description": "Weeks in the baseline (default 1)."}},
                          ["bank", "log"]),
    },
    "log_attempts": {
        "fn": log_attempts,
        "description": "Append quiz results to the attempts log so future starters and reviews can use them. Use "
                       "initials or ids for students, not full names.",
        "schema": _schema({"log_path": {"type": "string", "description": "Path to the attempts CSV."},
                           "attempts": {"type": "array", "description": "Rows of {student, question_id, result, date?}. "
                                        "result is right or wrong.", "items": {"type": "object"}},
                           "today": _TODAY}, ["log_path", "attempts"]),
    },
    "mark_answers": {
        "fn": mark_answers,
        "description": "First-pass marking of short written answers against a mark scheme's marking points, with "
                       "the evidence for each mark, feedback per student and the points the class missed most. "
                       "No AI model is used. Borderline answers are flagged for the teacher.",
        "schema": _schema({"answers": {"type": "array", "items": {"type": ["string", "object"]},
                                       "description": "Answers as strings, or {student, answer} objects."},
                           "question": {"type": "object", "description": "{q, marks, points:[{id, label, accept:[...], "
                                        "forbid:[...]}]}. accept entries are words or phrases; a nested list means all "
                                        "parts must appear."},
                           "questions_path": {"type": "string"}, "question_id": {"type": "string"}}, ["answers"]),
    },
    "validate_lesson": {
        "fn": validate_lesson,
        "description": "Check a lesson written in lesson-page-kit format before building it: ids, answers, sort "
                       "buckets, a task on every page, and text that reads like a teacher note on a student page.",
        "schema": _schema({"lesson": {"type": "object", "description": "{title, subject, pages:[{title, blocks:[...]}]}"},
                           "lesson_path": {"type": "string"}}),
    },
    "build_lesson_page": {
        "fn": build_lesson_page,
        "description": "Build the interactive student page for a lesson as one self-contained HTML file: multi-page, "
                       "instant feedback on multiple choice and sort tasks, written answers captured for the teacher "
                       "(never self-marked), a summary to copy after every page, and answer options mixed so the key "
                       "has no pattern.",
        "schema": _schema({"out_path": {"type": "string", "description": "Where to write the page, ending .html."},
                           "lesson": {"type": "object"}, "lesson_path": {"type": "string"},
                           "endpoint": {"type": "string", "description": "Optional https address that receives each answer."},
                           "allow_warnings": {"type": "boolean", "description": "Build even with warnings (default true)."}},
                          ["out_path"]),
    },
    "check_reports": {
        "fn": check_reports,
        "description": "Check a batch of student reports before they go out: word limits, sentences or openings "
                       "repeated between students, jargon and labels, and a missing next step.",
        "schema": _schema({"reports": {"type": "array", "description": "List of {student, text}. Placeholders like [S1] are fine.",
                                       "items": {"type": "object"}},
                           "min_words": {"type": "integer"}, "max_words": {"type": "integer"},
                           "extra_banned": {"type": "array", "items": {"type": "string"},
                                            "description": "Extra words or phrases the school doesn't want."}}, ["reports"]),
    },
    "text_stats": {
        "fn": text_stats,
        "description": "Word count and estimated reading age for any text (a parent message, a levelled text, a "
                       "student page), with the long sentences and hard words to simplify.",
        "schema": _schema({"text": {"type": "string"},
                           "target_age": {"type": "integer", "description": "Reader's age, to check the level against."},
                           "max_words": {"type": "integer"}}, ["text"]),
    },
}


def call(name: str, arguments: dict | None) -> dict:
    if name not in TOOLS:
        raise ToolError(f"unknown tool: {name}")
    try:
        return TOOLS[name]["fn"](**(arguments or {}))
    except TypeError as e:
        raise ToolError(f"bad arguments for {name}: {e}") from None
