#!/usr/bin/env python3
"""Build the TeachBench leaderboard site into _site/ from runs/*/results.json (newest run first)."""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
REPO = "https://github.com/kal-eficia/teachbench"
CATS = {"planning": "Planning", "retrieval": "Retrieval", "assessment": "Assessment", "explaining": "Explaining",
        "inclusion": "Inclusion", "pastoral": "Pastoral and parents", "tutoring": "Tutoring and progress",
        "leadership-ai": "Leadership and AI"}


def e(s):
    return html.escape(str(s))


CSS = """
@font-face{font-family:"Cinzel";src:url(fonts/cinzel-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Inter Tight";src:url(fonts/inter-tight-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Inter Tight";src:url(fonts/inter-tight-latin-500-normal.woff2) format("woff2");font-weight:500;font-display:swap}
@font-face{font-family:"Inter Tight";src:url(fonts/inter-tight-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
:root{--ink:#16140F;--ink-2:#4A453C;--ink-3:#6B6357;--paper:#F4EFE4;--paper-2:#EBE4D6;--rule:#CFC5B3;--brass:#7A5C23;--brass-light:#C9A45C;--on-dark-2:#BDB4A3;
--display:"Cinzel",Georgia,serif;--body:"Inter Tight","Helvetica Neue",Arial,system-ui,sans-serif;--gutter:40px;--section:96px}
@media (max-width:720px){:root{--gutter:20px;--section:64px}}
*{box-sizing:border-box;border-radius:0}
html{background:var(--ink)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--brass);text-decoration-thickness:2px;text-underline-offset:3px}
:focus-visible{outline:2px solid var(--brass);outline-offset:3px}
.wrap{max-width:1200px;margin-inline:auto;padding-inline:var(--gutter)}
.kicker{display:flex;align-items:center;gap:12px;font-weight:600;font-size:14px;letter-spacing:.32em;text-transform:uppercase;color:var(--brass);margin:0 0 20px}
.kicker::before{content:"";width:7px;height:7px;background:currentColor;flex:none}
.on-ink .kicker{color:var(--brass-light)}
h1,h2,h3{font-family:var(--display);font-weight:600;text-transform:uppercase;letter-spacing:.02em;margin:0}
h1{font-size:clamp(44px,30px + 3vw,76px);line-height:1.04}
h2{font-size:clamp(30px,24px + 1.6vw,46px);line-height:1.12;margin-bottom:16px}
h3{font-size:22px}
.lead{font-size:clamp(19px,17.3px + .45vw,23px);line-height:1.55;color:var(--ink-2);max-width:66ch;margin:22px 0 0}
section{padding-block:var(--section);border-top:1px solid var(--rule)}
.on-ink{background:var(--ink);color:var(--paper);border-top:none}.on-ink p,.on-ink li{color:var(--on-dark-2)}.on-ink a{color:var(--paper);text-decoration-color:var(--brass-light)}
header.site{border-bottom:1px solid var(--rule)}header.site .wrap{display:flex;align-items:center;justify-content:space-between;padding-block:20px;gap:24px}
header.site img{height:50px;margin-inline-start:-8px;display:block}
nav{display:flex;gap:28px;font-weight:500;font-size:16px}nav a{text-decoration:none}
.hero{border-top:none;padding-block:80px var(--section)}
table{border-collapse:collapse;width:100%}
th{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);font-weight:600;text-align:start;padding:0 12px 12px 0;border-bottom:1.5px solid var(--ink)}
td{padding:18px 12px 18px 0;border-bottom:1px solid var(--rule);vertical-align:middle}
.board td.rank{font-family:var(--display);font-size:28px;color:var(--brass);width:56px}
.board .name{font-weight:600;font-size:19px}.board .sub{font-size:14px;color:var(--ink-3)}
.score{font-family:var(--display);font-size:34px;line-height:1}
.ci{position:relative;height:14px;background:var(--paper-2);min-width:180px}
.ci span{position:absolute;top:0;bottom:0;background:var(--ink-2)}.ci i{position:absolute;top:-4px;bottom:-4px;width:3px;background:var(--ink)}
.cats td{text-align:center;font-variant-numeric:tabular-nums;font-size:16px}.cats td:first-child{text-align:start;font-weight:600}
.cats th{text-align:center}.cats th:first-child{text-align:start}
.best{font-weight:700;box-shadow:inset 0 -3px var(--brass)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);border-top:1.5px solid var(--ink);margin-top:40px}
.stat{padding:26px 24px 8px 0}.stat+.stat{padding-inline-start:24px;border-inline-start:1px solid var(--rule)}
.stat b{font-family:var(--display);font-weight:600;font-size:clamp(32px,4vw,48px);display:block;line-height:1}.stat span{display:block;color:var(--ink-2);font-size:16px;margin-top:10px}
@media (max-width:860px){.stats{grid-template-columns:1fr}.stat+.stat{padding-inline-start:0;border-inline-start:none;border-top:1px solid var(--rule)}.hide-sm{display:none}}
.steps{display:grid;grid-template-columns:repeat(4,1fr);border-top:1.5px solid var(--ink);margin-top:32px}
.step{padding:24px 24px 8px 0}.step+.step{padding-inline-start:24px;border-inline-start:1px solid var(--rule)}
.step .n{font-family:var(--display);color:var(--brass);font-size:20px}.step h3{font-size:19px;margin:10px 0 8px}.step p{margin:0;color:var(--ink-2);font-size:16px}
@media (max-width:860px){.steps{grid-template-columns:1fr 1fr}.step:nth-child(3){padding-inline-start:0;border-inline-start:none}}
.scroll{overflow-x:auto}
.tasks td{font-size:15px;padding:10px 12px 10px 0}.tasks td.num{text-align:center;font-variant-numeric:tabular-nums}
details{border-top:1px solid var(--rule);padding:14px 0}summary{cursor:pointer;font-weight:600}
.limits li{margin:8px 0;max-width:72ch}
footer.site{background:var(--ink);color:var(--on-dark-2);padding-block:56px;font-size:15px}
footer.site .wrap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:32px}footer.site img{height:58px;margin-inline-start:-10px}
footer.site a{color:var(--paper);text-decoration-color:var(--brass-light)}footer.site p{margin:0;max-width:56ch}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:15px;background:#2a261e;color:var(--paper);padding:2px 7px}
"""


def build():
    runs = sorted((ROOT / "runs").glob("*/results.json"), reverse=True)
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "site", OUT)
    if not runs:
        (OUT / "index.html").write_text("<p>No runs yet.</p>")
        return
    res = json.loads(runs[0].read_text(encoding="utf-8"))
    run_name = res["run"]["name"]
    board, meta = res["leaderboard"], res["meta"]
    tasks = {t["id"]: t for t in json.loads((ROOT / "tasks" / "tasks.json").read_text(encoding="utf-8"))}
    lo_all = min(b["ci95"][0] for b in board) - 5
    hi_all = 100
    span = hi_all - lo_all

    def pos(v):
        return max(0, min(100, 100 * (v - lo_all) / span))

    rows = []
    for i, b in enumerate(board, 1):
        lo, hi = b["ci95"]
        cc = b["code_checks"]
        rows.append(f"""<tr><td class="rank">{i:02d}</td>
<td><div class="name">{e(b['name'])}</div><div class="sub">{e(b['tasks'])} tasks · median {b['median_words']:,} words</div></td>
<td><span class="score">{b['score']:g}</span></td>
<td class="hide-sm"><div class="ci" role="img" aria-label="95% interval {lo} to {hi}"><span style="left:{pos(lo):.1f}%;right:{100 - pos(hi):.1f}%"></span><i style="left:calc({pos(b['score']):.1f}% - 1px)"></i></div><div class="sub" style="margin-top:6px">{lo} to {hi}</div></td>
<td>{cc['passed']}/{cc['total']}</td></tr>""")

    cat_rows = []
    for c, label in CATS.items():
        vals = [b["categories"].get(c) for b in board]
        top = max(v for v in vals if v is not None)
        cells = "".join(f'<td class="{"best" if v == top else ""}">{v:g}</td>' if v is not None else "<td>-</td>" for v in vals)
        cat_rows.append(f"<tr><td>{e(label)}</td>{cells}</tr>")
    cat_head = "".join(f"<th>{e(b['name'].replace('Claude ', ''))}</th>" for b in board)

    by_task = {}
    for a in res["answers"]:
        by_task.setdefault(a["task"], {})[a["entrant"]] = a
    trs = []
    for tid in sorted(by_task, key=lambda t: (tasks[t]["category"], t)):
        t = tasks[tid]
        cells = ""
        for b in board:
            a = by_task[tid].get(b["entrant"])
            cells += (f'<td class="num"><a href="{REPO}/blob/main/runs/{run_name}/answers/{b["entrant"]}/{tid}.md">{a["pct"]:g}</a></td>'
                      if a else '<td class="num">-</td>')
        trs.append(f"<tr><td>{e(tid)}</td><td>{e(CATS[t['category']])}</td><td>{e(t['phase'])}</td>{cells}</tr>")

    h2h = "".join(f"<li><b>{e(k.replace(' v ', ' against '))}:</b> {v['wins']} tasks higher, {v['losses']} lower, {v['level']} level</li>"
                  for k, v in res["head_to_head"].items())
    names = {b["entrant"]: b["name"] for b in board}
    for k in names:
        h2h = h2h.replace(k, e(names[k]))

    n_tasks = len(tasks)
    page = f"""<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TeachBench: an open benchmark for AI on real teaching tasks</title>
<meta name="description" content="{n_tasks} real teaching tasks, blind graded and checked by code. A public leaderboard for AI models, skills and prompts used by teachers.">
<meta property="og:title" content="TeachBench"><meta property="og:description" content="An open benchmark for AI on real teaching tasks.">
<link rel="icon" href="brand/favicon.svg" type="image/svg+xml">
<style>{CSS}</style></head><body>
<header class="site"><div class="wrap"><a href="./" aria-label="TeachBench home"><img src="brand/kalid-nur-logo-no-tagline.svg" alt="Kalid Nur logo: نور (light) in square Kufic" width="155" height="50"></a>
<nav aria-label="Main"><a href="#leaderboard">Leaderboard</a><a href="#method" class="hide-sm">Method</a><a href="#submit">Submit</a><a href="{REPO}">GitHub</a></nav></div></header>
<main>
<section class="hero"><div class="wrap">
<p class="kicker">TeachBench · {e(res["run"].get("label") or run_name)}</p>
<h1>How good is AI<br>at teaching work?</h1>
<p class="lead">{n_tasks} real requests a teacher might send, from Reception phonics to A level psychology, from lesson plans to difficult parent meetings. Every answer is graded blind by two separate graders against criteria fixed in advance, and checked by code wherever code can check.</p>
<div class="stats">
<div class="stat"><b>{n_tasks}</b><span>tasks in 8 categories, early years to sixth form</span></div>
<div class="stat"><b>{meta['answers_scored']}</b><span>answers graded blind, twice each</span></div>
<div class="stat"><b>{meta['graders_within_2_points']:g}%</b><span>of answers where the two graders agreed within 2 points of 12</span></div>
</div></div></section>

<section id="leaderboard"><div class="wrap">
<p class="kicker">Leaderboard</p><h2>Scores out of 100</h2>
<p class="lead" style="margin-bottom:32px">Score is the share of criteria met across all tasks, with code checks counted in. The bar shows the 95% confidence interval from resampling the tasks: where two bars overlap a lot, the gap could be luck.</p>
<div class="scroll"><table class="board"><tr><th></th><th>Entrant</th><th>Score</th><th class="hide-sm">95% interval</th><th>Code checks</th></tr>{''.join(rows)}</table></div>
<h3 style="margin-top:48px">Head to head</h3><ul>{h2h}</ul>
</div></section>

<section><div class="wrap">
<p class="kicker">By category</p><h2>Where each one is strong</h2>
<div class="scroll" style="margin-top:28px"><table class="cats"><tr><th>Category</th>{cat_head}</tr>{''.join(cat_rows)}</table></div>
</div></section>

<section id="method"><div class="wrap">
<p class="kicker">Method</p><h2>How it works</h2>
<div class="steps">
<div class="step"><span class="n">01</span><h3>Real tasks</h3><p>Each task is a message a teacher might send, with six criteria written before any answers existed.</p></div>
<div class="step"><span class="n">02</span><h3>Separate answers</h3><p>Each entrant answers in its own sessions, with no way to ask questions. Skill libraries choose their own skill, as in real use.</p></div>
<div class="step"><span class="n">03</span><h3>Blind grading</h3><p>Answers get random ids. Two graders score every answer 0 to 2 per criterion, seeing all entrants' answers to a task side by side, names hidden.</p></div>
<div class="step"><span class="n">04</span><h3>Code checks</h3><p>Answer keys are checked for guessable patterns, reports for repeated wording, messages for length and texts for reading age.</p></div>
</div>
<details style="margin-top:40px"><summary>All {n_tasks} tasks and every answer</summary><div class="scroll"><table class="tasks"><tr><th>Task</th><th>Category</th><th>Phase</th>{''.join(f"<th>{e(b['name'].replace('Claude ', ''))}</th>" for b in board)}</tr>{''.join(trs)}</table></div></details>
</div></section>

<section class="on-ink"><div class="wrap">
<p class="kicker">Read this too</p><h2>Limits</h2>
<ul class="limits">
<li>The graders are AI models (Claude Opus), not teachers. A teacher-graded round is the next step.</li>
<li>One answer per task per entrant. Single tasks vary; the overall pattern and the confidence intervals are what matter.</li>
<li>The tasks and criteria were written by Kalid Nur, who also wrote one of the entrants (ai-teaching-skills). The criteria describe widely shared good practice, but they are not neutral. Submissions of tasks from other teachers are welcome.</li>
<li>Each answering agent handled six tasks in one session, told to treat each as a new conversation.</li>
<li>Mostly UK curricula and secondary school. Primary, early years and sixth form are represented but smaller.</li>
</ul></div></section>

<section id="submit"><div class="wrap">
<p class="kicker">Get on the board</p><h2>Submit an entrant</h2>
<p class="lead">An entrant is a model plus whatever you give it: a skill library, a system prompt, or nothing. Open a pull request adding a file to <code>entrants/</code> (and your skills or prompt), and it will be run on the next round. Tasks from teachers in other subjects and countries are just as welcome.</p>
<p style="margin-top:24px;font-weight:600"><a href="{REPO}#submit-an-entrant">How to submit</a> &nbsp; <a href="{REPO}/tree/main/runs/{run_name}">Every answer and grade from this run</a></p>
</div></section>
</main>
<footer class="site"><div class="wrap"><img src="brand/kalid-nur-logo-reversed.svg" alt="Kalid Nur logo: نور (light) in square Kufic" width="180" height="58">
<p>TeachBench is built and run by Kalid Nur, who teaches Computer Science, ICT and AI and trains schools on adopting AI. Open source under the MIT licence. <a href="{REPO}">GitHub</a></p></div></footer>
</body></html>
"""
    assert "—" not in page
    (OUT / "index.html").write_text(page, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print("built", OUT)


if __name__ == "__main__":
    build()
