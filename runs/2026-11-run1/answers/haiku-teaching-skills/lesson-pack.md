# Lesson pack: How data travels across the internet (packets and packet switching)

**Year 9 computing, 50 minutes, live on Zoom.** Assumptions: the class knows routers, switches and NICs from last lesson. No prior knowledge of packets is assumed. Students have a device and can open a shared HTML file, either from a link you send in the Zoom chat or from your screen share.

## 1. Teacher plan (teacher only)

**Objectives**
- Describe how data is split into packets, and what a packet's header and payload contain.
- Explain how packet switching sends packets separately and reassembles them at the destination.

**Timeline (50 minutes)**

| Time | Stage | What happens |
|---|---|---|
| 0 to 6 min | Starter | Students answer the recall questions from memory, with a confidence rating. Ask them to type answers in the Zoom chat as well as the page. |
| 6 to 18 min | Learn | Students read the packet and packet switching pages. Pause at the worked example and ask: "How many packets would a 1,000 packet photo need, and what number is on packet 500?" |
| 18 to 23 min | Check | Launch a Zoom poll with the three hinge questions on page 2. Read out the most common wrong answer and ask who chose it and why. |
| 23 to 38 min | Apply | Students match the four terms to definitions, then write the exam-style answer. Stop after 10 minutes and ask two students to read their answer aloud. |
| 38 to 42 min | Exit | Students write one thing they now know that they didn't know this morning, and paste their page summary into the chat. |
| 42 to 50 min | Buffer | Use for questions, the summary check, or any stage that ran long. |

**Misconceptions to listen for**
1. "Packets all take the same route." Ask: "If the first road is blocked, what could the packets do?"
2. "The packets arrive in order, so the sequence number isn't needed." Ask: "What would happen if the packets were on different routes?"
3. "A router is the same as a switch." Ask: "What does the router read on the packet? Which device joins networks together?"

**Differentiation**
- Support: give a sentence starter for the written answer, such as "Packet switching helps because…".
- Stretch: ask "What happens if one packet never arrives? Why does the receiver need the sequence numbers to spot this?"

**Remote notes**
- Use the Zoom poll for the MCQs. Students can answer in the chat for the short-answer questions.
- Camera is optional. Ask for a thumbs up, or a word in the chat, to check everyone is there.
- Backup: if the page won't load, put the MCQs in a Zoom poll and paste the match task into the chat as a numbered list.

**Next lesson's starter:** ask about packets, headers and routers, and include one question on what happens when a packet is lost.

---

## 2. Student page (students)

Save this as `packets.html`, or open it from the link you send.

```html
<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>How Data Travels: Packets</title>
<style>
body{font-family:system-ui,Arial,sans-serif;max-width:760px;margin:0 auto;padding:20px;line-height:1.5;color:#1b2a3a;background:#f7f9fb}
h1{font-size:1.6em}
h2{margin-top:1.6em;border-bottom:2px solid #0f766e;padding-bottom:4px}
.card{background:#fff;border:1px solid #d9e2ec;border-radius:10px;padding:16px;margin:14px 0}
.opt{display:block;margin:6px 0;padding:8px 10px;border:1px solid #cbd5e1;border-radius:8px;cursor:pointer;background:#fff}
.opt input{margin-right:8px}
button{background:#0f766e;color:#fff;border:0;border-radius:8px;padding:8px 14px;cursor:pointer;font-size:0.95em;margin-top:8px}
.feedback{margin-top:8px;font-weight:bold}
.good{color:#15803d}
.bad{color:#b91c1c}
.summary{background:#ecfdf5;border-left:4px solid #0f766e;padding:12px;border-radius:8px}
textarea{width:100%;min-height:80px;font:inherit;padding:8px;border-radius:8px;border:1px solid #cbd5e1;box-sizing:border-box}
select{padding:6px;border-radius:6px}
.conf label{margin-right:12px}
</style>
</head>
<body>

<h1>How Data Travels Across the Internet</h1>
<p>Last lesson you met routers, switches and NICs. Today you find out what those devices actually carry: data, cut into pieces.</p>

<h2>Page 1: Warm-up and learn</h2>

<div class="card">
  <p><strong>Warm-up.</strong> Answer from memory. No notes, no searching, no AI.</p>
  <p><strong>Q1.</strong> Which device joins your home network to other networks, such as the internet?</p>
  <label class="opt"><input type="radio" name="q1" value="A">A. A switch</label>
  <label class="opt"><input type="radio" name="q1" value="B">B. A NIC</label>
  <label class="opt"><input type="radio" name="q1" value="C">C. A router</label>
  <label class="opt"><input type="radio" name="q1" value="D">D. A cable</label>
  <button onclick="check('q1','C','fb1','A router reads the destination address and passes data on towards it.')">Check my answer</button>
  <div id="fb1" class="feedback"></div>
  <p class="conf"><strong>How sure are you?</strong>
    <label><input type="radio" name="c1" value="g">Guessing</label>
    <label><input type="radio" name="c1" value="t">Think so</label>
    <label><input type="radio" name="c1" value="c">Certain</label></p>
  <p><strong>Q2.</strong> In your own words, what does a NIC do?</p>
  <textarea id="starterShort" placeholder="Type your answer here."></textarea>
</div>

<div class="card">
  <h3>Packets</h3>
  <p>A photo, a song or a video file is far too big to travel across the internet as one piece. The data is cut into small chunks called <strong>packets</strong>.</p>
  <p>Each packet has two parts:</p>
  <ul>
    <li>The <strong>header</strong> is the label at the front. It holds the destination address and a sequence number.</li>
    <li>The <strong>payload</strong> is the actual piece of your data.</li>
  </ul>
  <p><strong>Worked example.</strong> Imagine a 1,000 piece photo. Each piece is numbered in its header: the first packet is number 1, the second is number 2, and so on. Packet number 500 holds the 500th piece of the photo.</p>
  <p>Think of it like a jigsaw sent in the post, where every piece has a label saying where it fits. Unlike a jigsaw in a box, these pieces can arrive in any order and can travel by different roads.</p>
</div>

<div class="card">
  <h3>Packet switching</h3>
  <p>Each packet is sent on its own. Routers read the destination address on each packet and pass it on towards that address. Two packets from the same file can take different routes.</p>
  <p>When the packets reach the destination, they are joined back together using their sequence numbers.</p>
</div>

<div class="summary">
  <p><strong>Summarise page 1</strong> in two or three sentences, in your own words.</p>
  <textarea id="sum1" placeholder="Type your summary here."></textarea>
  <button onclick="copySummary('sum1')">Copy my summary</button>
</div>

<h2>Page 2: Check</h2>

<div class="card">
  <p><strong>Q3.</strong> What is in the header of a packet?</p>
  <label class="opt"><input type="radio" name="q2" value="A">A. The destination address and the sequence number</label>
  <label class="opt"><input type="radio" name="q2" value="B">B. The whole file</label>
  <label class="opt"><input type="radio" name="q2" value="C">C. A picture of the sender</label>
  <label class="opt"><input type="radio" name="q2" value="D">D. Only the payload</label>
  <button onclick="check('q2','A','fb2','The header holds the destination address and the sequence number. The payload is the data.')">Check my answer</button>
  <div id="fb2" class="feedback"></div>
</div>

<div class="card">
  <p><strong>Q4.</strong> Why does each packet carry a sequence number?</p>
  <label class="opt"><input type="radio" name="q3" value="A">A. To make the packet travel faster</label>
  <label class="opt"><input type="radio" name="q3" value="B">B. To show which router it used</label>
  <label class="opt"><input type="radio" name="q3" value="C">C. To count how many routers there are</label>
  <label class="opt"><input type="radio" name="q3" value="D">D. To let the receiver put the packets back in the right order</label>
  <button onclick="check('q3','D','fb3','The sequence number tells the receiving device where each packet fits.')">Check my answer</button>
  <div id="fb3" class="feedback"></div>
</div>

<div class="card">
  <p><strong>Q5.</strong> One packet gets lost on the way. What happens?</p>
  <label class="opt"><input type="radio" name="q4" value="A">A. The whole file is sent again from the start</label>
  <label class="opt"><input type="radio" name="q4" value="B">B. The missing packet is sent again</label>
  <label class="opt"><input type="radio" name="q4" value="C">C. The file is deleted</label>
  <label class="opt"><input type="radio" name="q4" value="D">D. The other packets get bigger</label>
  <button onclick="check('q4','B','fb4','Only the missing packet needs to be sent again, because the others have arrived.')">Check my answer</button>
  <div id="fb4" class="feedback"></div>
</div>

<div class="card">
  <p><strong>Q6.</strong> Which statement about routers is correct?</p>
  <label class="opt"><input type="radio" name="q5" value="A">A. A router decides the next step for each packet by reading its destination address</label>
  <label class="opt"><input type="radio" name="q5" value="B">B. A router stores the whole file in one place</label>
  <label class="opt"><input type="radio" name="q5" value="C">C. A router always sends every packet by the same route</label>
  <label class="opt"><input type="radio" name="q5" value="D">D. A router can only connect two computers in the same room</label>
  <button onclick="check('q5','A','fb5','Each router reads the destination address and passes the packet on.')">Check my answer</button>
  <div id="fb5" class="feedback"></div>
</div>

<div class="card">
  <p><strong>Q7.</strong> Why is it useful that packets can take different routes?</p>
  <label class="opt"><input type="radio" name="q6" value="A">A. It makes the packets bigger</label>
  <label class="opt"><input type="radio" name="q6" value="B">B. Packets can never get lost on the internet</label>
  <label class="opt"><input type="radio" name="q6" value="C">C. The sender doesn't need an address</label>
  <label class="opt"><input type="radio" name="q6" value="D">D. If one route is busy or broken, the packets can go another way</label>
  <button onclick="check('q6','D','fb6','Different routes mean the data can still get through when one route is busy or broken.')">Check my answer</button>
  <div id="fb6" class="feedback"></div>
</div>

<div class="summary">
  <p><strong>Summarise page 2</strong> in two or three sentences, in your own words.</p>
  <textarea id="sum2" placeholder="Type your summary here."></textarea>
  <button onclick="copySummary('sum2')">Copy my summary</button>
</div>

<h2>Page 3: Apply and exit</h2>

<div class="card">
  <p><strong>Match each term to its meaning.</strong> Choose one letter for each term.</p>
  <ol>
    <li>Packet
      <select id="t1"><option value="">Choose</option><option>A</option><option>B</option><option>C</option><option>D</option></select></li>
    <li>Header
      <select id="t2"><option value="">Choose</option><option>A</option><option>B</option><option>C</option><option>D</option></select></li>
    <li>Sequence number
      <select id="t3"><option value="">Choose</option><option>A</option><option>B</option><option>C</option><option>D</option></select></li>
    <li>Packet switching
      <select id="t4"><option value="">Choose</option><option>A</option><option>B</option><option>C</option><option>D</option></select></li>
  </ol>
  <p><strong>Meanings:</strong></p>
  <ul style="list-style:none;padding-left:0">
    <li><strong>A.</strong> A number that shows where each piece fits in the original data.</li>
    <li><strong>B.</strong> A small chunk of data that is sent across a network.</li>
    <li><strong>C.</strong> A way of sending data where each piece can take its own route and is joined back together at the destination.</li>
    <li><strong>D.</strong> The part at the front of a packet that holds the addresses and other information about it.</li>
  </ul>
  <button onclick="checkMatch()">Check my matches</button>
  <div id="matchFb" class="feedback"></div>
</div>

<div class="card">
  <p><strong>Exam-style question (4 marks).</strong> Explain how packet switching helps a large video file travel across the internet.</p>
  <textarea id="examAns" placeholder="Write your answer here. Use full sentences."></textarea>
</div>

<div class="card">
  <p><strong>Exit question.</strong> Name one thing you now know about packets that you didn't know this morning.</p>
  <textarea id="exitAns" placeholder="Type one thing here."></textarea>
</div>

<div class="summary">
  <p><strong>Summarise page 3</strong> in two or three sentences, in your own words.</p>
  <textarea id="sum3" placeholder="Type your summary here."></textarea>
  <button onclick="copySummary('sum3')">Copy my summary</button>
</div>

<script>
function check(name, correct, fbId, why) {
  var chosen = document.querySelector('input[name="' + name + '"]:checked');
  var fb = document.getElementById(fbId);
  if (!chosen) { fb.textContent = 'Pick an answer first.'; fb.className = 'feedback'; return; }
  if (chosen.value === correct) { fb.textContent = 'Correct. ' + why; fb.className = 'feedback good'; }
  else { fb.textContent = 'Not quite. ' + why; fb.className = 'feedback bad'; }
}

function checkMatch() {
  var want = { t1: 'B', t2: 'D', t3: 'A', t4: 'C' };
  var right = 0;
  for (var k in want) {
    if (document.getElementById(k).value === want[k]) { right++; }
  }
  var fb = document.getElementById('matchFb');
  fb.textContent = right + ' of 4 correct. ' + (right === 4 ? 'Well done.' : 'Look again at the ones you are unsure of, then check again.');
  fb.className = 'feedback ' + (right === 4 ? 'good' : 'bad');
}

function copySummary(id) {
  var box = document.getElementById(id);
  if (!box.value.trim()) { alert('Write your summary first.'); return; }
  box.select();
  var ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  if (navigator.clipboard && !ok) {
    navigator.clipboard.writeText(box.value).then(function () { alert('Copied. Paste it into the class chat.'); });
  } else {
    alert(ok ? 'Copied. Paste it into the class chat.' : 'Select the text and copy it by hand.');
  }
}
</script>
</body>
</html>
```

---

## 3. Homework (students, about 20 minutes)

**Retrieval (no notes)**
1. What is a packet?
2. Name the two parts of a packet and say what each one holds.
3. What does a router do with a packet it receives?
4. Why do packets need sequence numbers?

**Stretch (about 8 minutes)**
A friend says that packet switching is the same as sending the whole file down one cable. Explain why they are wrong. Use the words "header" and "router" in your answer.

Paste your answers to questions 1 to 4 and the stretch answer into the class chat.

---

## 4. Mark scheme (teacher only)

**Starter**
- Q1: C (a router). Credit only C.
- Q2 (NIC): credit "connects a device to a network" or "gives the device an address so it can join a network". Do not credit "stores data" alone.

**Page 2 MCQs:** Q3 A, Q4 D, Q5 B, Q6 A, Q7 D. Credit only these letters.

**Match task:** credit each correct term: Packet B, Header D, Sequence number A, Packet switching C. Award 1 mark per term.

**Exam-style question (4 marks).** Credit one mark for each marking point:
1. The video is split into packets.
2. Each packet has a header with the destination address (and a sequence number).
3. Packets travel separately and can take different routes. Routers pass each one on towards the destination.
4. The packets are joined back together at the destination using the sequence numbers.

*Model answer:* "Packet switching splits the video file into packets. Each packet has a header with the destination address and a sequence number. The packets can travel separately and take different routes, with routers passing each one on. When they arrive, the sequence numbers are used to join the packets back together in the right order."

*Not credited on their own:* "The file is sent in packets" with no further detail (1 point at most); "packets are sent quickly" (no mark).

**Homework**
- Q1: a small chunk of data sent across a network. Accept "a piece of data with a header and payload".
- Q2: header (addresses, sequence number) and payload (the data).
- Q3: reads the destination address and forwards the packet towards it.
- Q4: so the receiver can put the packets back in order.
- Stretch: credit an explanation that packets can take different routes and are not all sent down the same cable, with "header" and "router" used correctly.

---

## 5. Solutions sheet (teacher only, for approving answers live)

- **Starter Q1:** C (router).
- **Starter Q2:** NIC connects a device to a network; accept any clear version.
- **Q3 (page 2):** A (destination address and sequence number).
- **Q4:** D (put packets back in order).
- **Q5:** B (missing packet is resent).
- **Q6:** A (router reads destination address and decides the next step).
- **Q7:** D (another route if one is busy or broken).
- **Match:** Packet = B, Header = D, Sequence number = A, Packet switching = C.
- **Exam question (4 marks):** award marking points 1 to 4 from the mark scheme.
- **Exit question:** accept any accurate fact about packets, headers, routers or sequence numbers.

---

ANSWER KEY: C A D B A D
