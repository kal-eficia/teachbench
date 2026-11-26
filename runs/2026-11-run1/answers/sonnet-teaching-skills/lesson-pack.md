# Year 9 Computing: How data travels across the internet (packets and packet switching)

**Length:** 50 minutes, live on Zoom. **Follows:** network hardware (routers, switches, NICs).

**Assumptions:** mixed-ability Year 9 class, 20 to 30 students, cameras optional, everyone can use Zoom chat and polls. I've assumed no specific exam board, so the content is pitched at KS3 going into GCSE (it fits OCR J277, AQA 8525 and Edexcel 1CP2 networks content). The teacher plan comes first, then the student pages, homework, mark scheme and a one-screen solutions sheet.

**What's in this pack**
1. Teacher plan (timings, scripts, misconceptions, backup plan)
2. Student pages (share these on screen or send the text; each page ends with a summary to paste into chat)
3. Homework
4. Mark scheme
5. Solutions sheet (quick check while teaching)

---

# 1. TEACHER PLAN

## Objectives
By the end of the lesson students can:
- **Describe** what a packet is and name what is in its header and payload.
- **Explain** why data is split into packets and sent by different routes (packet switching).
- **Explain** how packets are put back in the right order and what happens if one goes missing.
- **Apply** this by tracing a message sent from one computer to another through routers.

## Before the lesson (10 minutes)
- Open a command window and run `tracert bbc.co.uk` (Windows) or `traceroute bbc.co.uk` (Mac/Linux). Take a screenshot as a backup. Do not rely on the live run; some school networks block it.
- Create three Zoom polls: Starter Q1, Starter Q2, Hinge (Q4). Or just have students type the letter in chat.
- Paste the six scrambled packets from Page 4 into a shared slide or doc.
- Have a "Hold up a hand/type 1, 2 or 3" confidence routine ready: 1 = guessing, 2 = think so, 3 = certain.

## Timeline

| Time | Stage | What happens |
|---|---|---|
| 0:00 to 0:06 | **Starter: recall from last lesson** | Q1, Q2 (MCQ polls) and one short-answer question typed into chat. No notes. Ask for confidence rating. |
| 0:06 to 0:09 | **Hook** | "I want to send you a 3,000 word essay by post, but the envelope only holds one page. What do I do?" Take 3 answers in chat. |
| 0:09 to 0:20 | **Learn** (Pages 1 to 3) | Packets, anatomy of a packet, packet switching. One worked example. |
| 0:20 to 0:25 | **Check** | Hinge question Q4 (poll). Act on the result (see below). |
| 0:25 to 0:38 | **Apply** | Page 4: put the packets back in order and find the lost packet. Page 5: traceroute demo and "be the router" route-tracing. |
| 0:38 to 0:46 | **Written answer** | Page 6: 4-mark explain question, typed in chat or on paper held to the camera at the end. |
| 0:46 to 0:50 | **Exit and summary** | Q6 (poll), then copy the final summary into chat. Set homework. |

## Script and moves, stage by stage

**Starter (0:00).** "Cameras optional, notes closed. Answer from memory. After each question, type 1, 2 or 3 for how sure you are."
- Look for students who put "3" and get it wrong. They hold a firm misconception, usually that a switch and a router do the same job. Name no one; re-teach it in 30 seconds.
- Short answer for chat: "In one sentence, what is the difference between a switch and a router?" Model answer: a switch connects devices inside one network; a router connects different networks and forwards data between them.

**Hook (0:06).** Draw out: split it into pages, number the pages, put each in its own envelope with the address, post them separately, put them in order at the other end. "That is exactly what the internet does. The envelopes are called packets."

**Learn (0:09).** Show each page on screen for 3 to 4 minutes. After each page, students paste the page summary into chat. This lets you see their thinking without needing cameras.
- Page 1: Why packets? Say the three reasons aloud: any packet can take any route; a lost packet only means re-sending that one; no one big message blocks the line for everyone else.
- Page 2: Anatomy of a packet. Point at header, payload, trailer. Stress that the **router reads the header**, not the payload.
- Page 3: Packet switching. Pause on "each router decides **independently** where to send the next packet". This is the idea students find hardest.
- Think-aloud for the worked example (Page 3): "Packet 3 gets there before packet 2. Does that matter? No. I check the numbers, put them in order, and only then rebuild the message."

**Check (0:20).** Ask Q4 as a poll. Read the results:
- 80% or more correct: move on.
- 50 to 80% correct: re-explain with the post analogy, then re-poll the two most popular wrong answers.
- Under 50%: stop, redo Page 1 in a different way (draw the jigsaw), then move on.

**Apply (0:25).**
- Page 4 (about 6 minutes): students put the six packets in order in chat ("my order is 3, 1, 4..."), then say which packet is missing. Reveal the answer; ask what the receiver does next (asks for that packet again).
- Page 5 (about 7 minutes): show the traceroute screenshot or live run. "Each line is a router the packet visited. Each visit is called a hop." Then "Be the router": use the network map on Page 5. Pick three students by name to say, in chat, which router they would send packet 1 to next and why (shortest, or avoiding a busy or broken link).

**Written answer (0:38).** Students type their answer in chat but do not send until you say "send". Then read out two good ones and one that is nearly there. Use the mark scheme to show how marks are awarded.

**Exit (0:46).** Poll Q6. Everyone pastes the final summary into chat. Set homework.

## Misconceptions to listen for

| Students say or think | Fix |
|---|---|
| "The packets all go the same way, like a train." | They *can* go different ways. Each router chooses the next hop for each packet separately. |
| "The router reads my message." | Routers read the **header** (the address), not the payload. |
| "If a packet is lost, the whole thing has to be sent again." | Only the missing packet is requested again. Packet numbers make this possible. |
| "Packets are encrypted because they are split up." | Splitting up is not encryption. Anyone who collects all the packets can rebuild the message. |
| "A switch and a router are the same." | Switch: inside one network, using MAC addresses. Router: between networks, using IP addresses. |

## Differentiation
- **Support:** give a half-finished packet diagram (header, payload and trailer labelled, parts blank). Provide sentence starters for the written answer: "Data is split into packets so that... Each packet has a header which contains... At the destination, the packets are..."
- **Stretch:** ask "Why might a very large number of tiny packets be a problem?" (more headers means more overhead) and "What does TTL (time to live) do and why is it needed?" (stops a packet bouncing around the network forever; it goes down by 1 at each hop and the packet is discarded at 0).

## Remote and backup plan
- If polls fail, students type their letter in chat instead.
- If screen share fails, send the student pages as text (below) in the chat or by email and talk through them.
- If traceroute is blocked, use the screenshot. If you have no screenshot, describe: "a typical result shows 8 to 15 hops".
- Students without a quiet space can type answers rather than speak.

## For next lesson's starter
Note which of Q3 to Q6 were missed most. Open next time with: header contents, why packets, how order is restored.

---

# 2. STUDENT PAGES

*(Share each page on screen. At the end of each page, students copy their summary into the chat.)*

## Before we start: quick recall (no notes!)

After each question, type the letter and then 1, 2 or 3 (1 = guessing, 2 = think so, 3 = certain).

**Q1.** Which device forwards data between different networks?
- A. Switch
- B. Network interface card (NIC)
- C. Router
- D. Server

**Q2.** What does a network interface card (NIC) do?
- A. Connects a device to a network
- B. Chooses the best route between two networks
- C. Sends every message to every device on the network
- D. Stores copies of web pages

**Q-chat.** In one sentence: what is the difference between a switch and a router?

---

## Page 1: Why is data split up?

Imagine you want to send a photo to a friend in Australia. A photo is a lot of data. If it was sent in one huge lump, it would block the line for everyone else.

So your computer **chops the data into small pieces called packets**. Think of it like posting a jigsaw puzzle one piece at a time, each piece in its own envelope.

Why do this?
- Different packets can travel by **different routes**, so no single road gets jammed.
- If one packet is lost, only that packet needs to be sent again.
- Lots of people can share the same cables at the same time.

**Try it:** A 6,000 byte file is split into packets that can each carry 1,000 bytes. How many packets? Type your answer in chat.

**My summary (copy this into chat):**
> Data is split into small pieces called ______. This is done so that ______ and ______. My answer to the try-it: ______ packets.

[Copy my summary]

---

## Page 2: What is inside a packet?

Every packet has three parts:

| Part | What it holds |
|---|---|
| **Header** | Where it is going (the destination IP address), where it came from (the source IP address), the packet number (for example "3 of 6") and a time-to-live count |
| **Payload** | The actual piece of your data (a bit of your photo) |
| **Trailer** | A check code, so the receiver can tell if the packet was damaged on the way |

Routers read the **header** to decide where to send the packet. They do not need to read the payload.

**Spot the part:** Which part would tell the receiver this is packet 4 of 6? Which part holds the piece of your photo?

**My summary:**
> A packet has a header, a payload and a trailer. The header contains ______. The payload is ______. The trailer is used for ______.

[Copy my summary]

---

## Page 3: Packet switching

**Packet switching** is how the internet sends data. Each packet is sent separately, and **each router along the way decides where to send it next**, using the destination IP address in the header.

Packets can take different routes. One might go London, Paris, Frankfurt. Another might go London, Amsterdam, Frankfurt, because Paris was busy.

At the other end, the packets can arrive **out of order**. That is fine. The receiving computer uses the **packet numbers** to put them in order and rebuild your file.

**Worked example:** A message is split into 4 packets. They arrive in the order 2, 4, 1, 3. The receiver sorts them by number to get 1, 2, 3, 4 and rebuilds the message. Nothing needs to be sent again.

**What if one is missing?** The receiver notices packet 3 never arrived, so it asks the sender to send packet 3 again. Only packet 3.

**My summary:**
> In packet switching, each ______ chooses the next step for each packet. Packets can arrive out of order, so the receiver uses ______ to put them back together. If a packet is lost, ______.

[Copy my summary]

---

## Page 4: Fix the message

A message was split into 6 packets. They arrived in this order:

**4, 1, 6, 3, 2**

1. Which packet is missing?
2. Put the packets that did arrive into the right order.
3. What will the receiving computer do next?

Type your answers in chat.

**My summary:**
> The missing packet is ______. The correct order is ______. The receiver will ______.

[Copy my summary]

---

## Page 5: Follow the packets

When you run a **traceroute**, you can see every router a packet visited on its way. Each stop is a **hop**.

Look at the traceroute on screen. How many hops did it take?

**Be the router.** Look at this small network:

```
Sender -- R1 -- R2 -- R4 -- Receiver
           \          /
            R3 ------
```

R1 has received a packet. Router R2 is busy. Which router would you send the packet to next, R2 or R3? Explain in one sentence.

Then: if R3 stops working halfway through, what happens to the other packets in the message?

**My summary:**
> A hop is ______. Routers can send packets round a busy or broken router because ______.

[Copy my summary]

---

## Page 6: Show what you know

**Q3.** What does the header of a packet contain?
- A. The wi-fi password
- B. The colour of the cable
- C. The size of the computer's screen
- D. The destination IP address and the packet number

**Q4.** Why is data split into packets before it is sent across the internet?
- A. So that it becomes encrypted
- B. So packets can take different routes and a lost packet can be sent again without re-sending everything
- C. So that the file is bigger
- D. So that routers can read the message

**Q5.** Packets arrive at the destination in the order 3, 1, 2. What happens?
- A. The message is shown scrambled
- B. The sender has to send everything again
- C. The router fixes the order before it arrives
- D. The receiver uses the packet numbers to put them in order

**Written question (4 marks).** Explain how a large file is sent across the internet from one computer to another using packets. Type your answer, but do not send it until your teacher says.

**Exit Q6.** A router receives a packet. What does it read to decide where to send it next?
- A. The destination IP address in the header
- B. The contents of the payload
- C. The packet number only
- D. The sender's password

**My final summary:**
> Today I learned that ______. The thing I am least sure about is ______.

[Copy my summary]

---

# 3. HOMEWORK (15 to 20 minutes)

**Part A: Remember (from last lesson and this lesson)**
1. Name two things a NIC is used for. (2 marks)
2. State one difference between a switch and a router. (1 mark)
3. What are the three parts of a packet? (3 marks)
4. Which part of a packet does a router read to decide where to send it? (1 mark)

**Part B: Apply**
5. A file is split into 8 packets. They arrive in the order 5, 2, 8, 1, 3, 7, 4. Which packet is missing, and what happens next? (2 marks)
6. Mia says "All the packets from my video call take exactly the same route." Is she right? Explain. (2 marks)

**Part C: Stretch (optional)**
7. Packets have a time-to-live (TTL) value that goes down by 1 at each router. Explain why this is useful. (2 marks)

---

# 4. MARK SCHEME

## Lesson questions

| Q | Answer | Marks | Notes |
|---|---|---|---|
| Q-chat | A switch connects devices within one network; a router connects different networks / forwards packets between networks | 1 | Do not accept "a router is bigger" or "a switch sends to everything" |
| Written (4 marks) | Any 4 from: data is split into packets (1); each packet has a header with destination address and packet number (1); packets are sent separately / can take different routes (1); routers read the header and forward each packet (1); packets may arrive out of order (1); the receiver uses the packet numbers to put them in order (1); missing or damaged packets are requested again (1) | 4 | Award marks for explanation, not a list of terms. Do not credit "packets are encrypted" |
| Page 1 try-it | 6 packets | n/a | |
| Page 4 | Missing: packet 5. Order: 1, 2, 3, 4, 6. Receiver asks the sender to resend packet 5 | n/a | |
| Page 5 | Either R2 or R3 with a reason; best answer: R3 because R2 is busy. If R3 fails, other packets are sent by a different route | n/a | |

## Homework

| Q | Answer | Marks |
|---|---|---|
| 1 | Any two: connects a computer/device to a network; allows it to send and receive data; has a unique MAC address | 2 |
| 2 | Switch connects devices within a network; router connects networks (or uses IP addresses) | 1 |
| 3 | Header, payload, trailer | 3 |
| 4 | The header (destination IP address) | 1 |
| 5 | Packet 6 is missing (1); receiver asks sender to send packet 6 again (1) | 2 |
| 6 | No (1); each packet can take a different route chosen by routers depending on traffic or failures (1) | 2 |
| 7 | Stops packets going round in circles forever (1); packet is discarded when TTL reaches 0, so it does not clog the network (1) | 2 |

---

# 5. SOLUTIONS SHEET (quick check in class)

| Item | Answer |
|---|---|
| Q1 | C (router) |
| Q2 | A (connects a device to a network) |
| Q-chat | switch = inside one network; router = between networks |
| Page 1 try-it | 6 packets |
| Page 2 spot the part | Header (packet 4 of 6); payload (piece of photo) |
| Page 3 worked example | Sorted by number 1, 2, 3, 4; resend only packet 3 if missing |
| Page 4 | Missing packet 5; order 1, 2, 3, 4, 6; ask for packet 5 again |
| Page 5 | R3 (busy R2); if R3 fails, use another route |
| Q3 | D |
| Q4 | B |
| Q5 | D |
| Q6 | A |
| Written | Split into packets / headers with address and number / separate routes / routers read header / reorder at end / resend if lost |

ANSWER KEY: C A D B D A
