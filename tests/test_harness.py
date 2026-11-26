import json
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))

import checks  # noqa: E402
import score  # noqa: E402

TASKS = json.loads((ROOT / "tasks" / "tasks.json").read_text(encoding="utf-8"))


class Tasks(unittest.TestCase):
    def test_shape(self):
        ids = [t["id"] for t in TASKS]
        self.assertEqual(len(ids), len(set(ids)))
        for t in TASKS:
            self.assertEqual(len(t["criteria"]), 6, t["id"])
            for k in ("category", "phase", "subject", "task"):
                self.assertTrue(t.get(k), (t["id"], k))
            if t.get("auto"):
                self.assertIn(t["auto"], checks.NAMES, t["id"])
            self.assertNotIn("—", t["task"] + " ".join(t["criteria"]), t["id"])

    def test_balanced_categories(self):
        from collections import Counter
        counts = Counter(t["category"] for t in TASKS)
        self.assertEqual(len(counts), 8)
        self.assertEqual(len(set(counts.values())), 1, counts)


class Checks(unittest.TestCase):
    def test_key(self):
        self.assertFalse(checks.check("key", "...\nANSWER KEY: A B C D A B")["pass"])
        self.assertTrue(checks.check("key", "...\nANSWER KEY: **C A D B D A C B**")["pass"])
        self.assertIsNone(checks.check("key", "no key here")["pass"])

    def test_message(self):
        ok = "hi\n===\nShort message here.\n===\n"
        self.assertTrue(checks.check("message80", ok)["pass"])
        long = "===\n" + "word " * 120 + "\n==="
        self.assertFalse(checks.check("message100", long)["pass"])
        self.assertIsNone(checks.check("message100", "no markers")["pass"])

    def test_reading(self):
        easy = "===\nThe sun is hot. It gives us light. Plants need it to grow.\n==="
        self.assertTrue(checks.check("reading8", easy)["pass"])


class Bootstrap(unittest.TestCase):
    def test_ci_contains_mean_and_is_ordered(self):
        vals = [random.Random(i).uniform(60, 100) for i in range(72)]
        lo, hi = score.bootstrap_ci(vals)
        mean = sum(vals) / len(vals)
        self.assertLess(lo, mean)
        self.assertGreater(hi, mean)
        self.assertEqual(score.bootstrap_ci([80.0] * 10), (80.0, 80.0))


class EndToEnd(unittest.TestCase):
    """Prepare a tiny run, fake the answers and grades, and check the scores come out right."""

    def test_pipeline(self):
        with tempfile.TemporaryDirectory() as d:
            work = Path(d)
            subprocess.run([sys.executable, str(ROOT / "harness" / "prepare.py"), str(work), "--entrants",
                            "sonnet-plain,sonnet-teaching-skills", "--only", "quiz,hinge", "--per-agent", "2",
                            "--per-grader", "2"], check=True, capture_output=True)
            key = json.loads((work / "secret" / "key.json").read_text())
            self.assertEqual(len(key), 4)
            for p in (work / "agents").glob("*.md"):
                text = p.read_text()
                self.assertNotIn("sonnet", " ".join(l for l in text.splitlines() if "answers/" in l))
            for g in (work / "graders").glob("*.md"):
                self.assertNotIn("teaching-skills", g.read_text(), "graders must not see entrant names")
            graded = []
            for aid, info in key.items():
                good = info["entrant"] == "sonnet-teaching-skills"
                body = "answer\nANSWER KEY: " + ("A B A D A C D B C B D C" if good else "A B C D A B C D A B C D")
                (work / "answers" / f"{aid}.md").write_text(body)
                graded.append({"id": aid, "task": info["task"], "scores": [2] * 6 if good else [1] * 6, "note": "x"})
            for gname in ("batch01_a", "batch01_b"):
                (work / "grades" / f"{gname}.json").write_text(json.dumps({"grader": gname, "answers": graded}))
            res = score.score(work)
            board = {b["entrant"]: b for b in res["leaderboard"]}
            self.assertEqual(board["sonnet-teaching-skills"]["score"], 100.0)
            # plain: quiz has a code check (key) it fails: (6 + 0) / 14; hinge has none: 6 / 12
            self.assertAlmostEqual(board["sonnet-plain"]["score"], (600 / 14 + 50) / 2, delta=0.15)
            self.assertEqual(board["sonnet-teaching-skills"]["code_checks"], {"passed": 1, "total": 1, "format_missed": 0})
            self.assertEqual(res["head_to_head"]["sonnet-teaching-skills v sonnet-plain"]["wins"], 2)
            self.assertEqual(res["meta"]["graders_within_2_points"], 100.0)


if __name__ == "__main__":
    unittest.main()
