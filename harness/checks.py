"""Objective checks done by code, so part of every score does not depend on a model's judgement."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))
from classroom import tools  # noqa: E402

NAMES = {
    "key": "No guessable answer pattern",
    "reports": "Reports pass length, repetition and jargon checks",
    "message100": "Message under 100 words",
    "message80": "Message under 80 words",
    "reading10": "Reading age 10.5 or below",
    "reading8": "Reading age 9 or below",
}


def between(text: str) -> str | None:
    parts = re.split(r"^\s*={3,}\s*$", text, flags=re.M)
    return parts[1].strip() if len(parts) >= 3 else None


def check(kind: str, text: str) -> dict:
    """Return {"name", "pass": True/False/None, "detail"}. None means the answer ignored the required format."""
    name = NAMES[kind]
    if kind == "key":
        found = re.findall(r"ANSWER KEY:\s*\**\s*([A-Da-d][A-Da-d\s,;/.-]*)", text)
        if not found:
            return {"name": name, "pass": None, "detail": "no ANSWER KEY line found"}
        key = "".join(re.findall(r"[A-Da-d]", found[-1])).upper()
        if len(key) < 4:
            return {"name": name, "pass": None, "detail": f"key too short: {key}"}
        rep = tools.check_answer_key(key=key, options=4)
        fails = [f"{f['rule']} at {f['where']}" for r in rep["reports"] for f in r["findings"] if f["severity"] == "fail"]
        return {"name": name, "pass": rep["ok"], "detail": f"key {key}: " + ("clean" if rep["ok"] else "; ".join(fails))}
    if kind == "reports":
        latest = {}
        for code, body in re.findall(r"^\W*\[(S\d)\]\W*:\s*(.+)$", text, flags=re.M):
            latest[code] = re.sub(r"[*_`]", "", body).strip()
        if len(latest) < 6:
            return {"name": name, "pass": None, "detail": f"only {len(latest)} reports in the requested format"}
        rep = tools.check_reports(reports=[{"student": f"[{k}]", "text": v} for k, v in sorted(latest.items())])
        bad = [f"{r['student']}: {'; '.join(r['issues'])}" for r in rep["reports"] if not r["ok"]]
        return {"name": name, "pass": rep["ok"], "detail": rep["summary"] + (" " + " | ".join(bad) if bad else "")}
    if kind.startswith("message"):
        limit = int(kind[len("message"):])
        msg = between(text)
        if not msg:
            return {"name": name, "pass": None, "detail": "no === markers found"}
        n = len(msg.split())
        return {"name": name, "pass": n <= limit, "detail": f"{n} words"}
    if kind.startswith("reading"):
        target = {"reading10": 10.5, "reading8": 9.0}[kind]
        body = between(text)
        if not body:
            return {"name": name, "pass": None, "detail": "no === markers found"}
        s = tools.text_stats(text=re.sub(r"[*_#`>]", "", body))
        return {"name": name, "pass": s["reading_age_estimate"] <= target,
                "detail": f"estimated reading age {s['reading_age_estimate']}"}
    raise ValueError(f"unknown check {kind}")
