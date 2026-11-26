# Year 9 Computing (Zoom, 50 minutes): How data travels across the internet (packets and packet switching)

**Assumptions:** students can see your screen, use Zoom chat and (ideally) a whiteboard or annotation tool, and can open a shared slide deck. You may need breakout rooms for the activity; there is a whole-class alternative if you prefer not to use them. Students have a pen and paper.

## Learning objectives

By the end of the lesson students can:

1. Explain why data is split into packets.
2. Describe what is in a packet (header and payload).
3. Explain how packet switching sends packets along different routes and how they are reassembled.
4. Link routers (last lesson) to this lesson's content.

## Lesson timeline (50 minutes)

| Time | Stage | Zoom tool |
|---|---|---|
| 0 to 5 | Retrieval starter on last lesson (routers, switches, NICs) | Chat |
| 5 to 12 | Hook and the big question | Screen share |
| 12 to 22 | Teach: packets, header and payload | Slides, annotation |
| 22 to 32 | Teach: packet switching and reassembly | Slides, annotation |
| 32 to 42 | Activity: "Post the message" simulation | Breakout rooms or chat |
| 42 to 48 | Quiz (six multiple-choice questions) | Poll or chat |
| 48 to 50 | Exit ticket and homework | Chat |

## Starter (0 to 5 minutes): retrieval from last lesson

Type answers in chat but do not press Enter until you say "go".

1. What does a NIC do? (Connects a device to a network.)
2. What is the difference between a switch and a router? (A switch connects devices within one network; a router connects networks together and directs data between them.)
3. What does a router use to decide where to send data? (The destination address and its routing table.)

Say: "Today we find out what actually travels through those routers."

## Hook (5 to 12 minutes)

Show a photo (say 5 MB) and ask: "If I email you this picture, does it travel as one big lump?" Take a few answers in chat.

Analogy to say aloud: "Imagine posting a 500-page book to a friend. You could try to send it in one giant parcel, but if the parcel gets lost, you lose everything. Instead you tear it into 50 envelopes of 10 pages each, number each envelope, write the address on every one and post them separately. They might take different routes. Your friend puts them back in order. That is how the internet sends data."

## Teaching input

### Part 1: Packets (12 to 22 minutes)

Key points for slides:

- Data (an email, a web page, a video) is broken into small chunks called **packets**.
- Each packet has two parts:
  - **Header:** destination IP address, source IP address, packet number (sequence number), and information to check for errors.
  - **Payload:** the actual piece of data being sent.
- Some models add a **trailer** or checksum at the end. Mention this only if your exam board requires it.

Draw a packet on the annotation board:

```
| HEADER: To: 203.0.113.5 | From: 198.51.100.7 | Packet 3 of 8 | Checksum |  PAYLOAD (part of the file)  |
```

Ask: "Why does each packet need a number?" (So they can be put back in order.) "Why does each need the destination address?" (Each packet travels on its own, so each must be able to find its way.)

Why use packets?

- If one packet is lost or corrupted, only that packet is re-sent.
- Many people can share the same lines, because small packets take turns.
- Packets can use any available route.

### Part 2: Packet switching (22 to 32 minutes)

Key points:

1. The sender's device splits the data into packets.
2. Each packet is sent to a **router**.
3. Each router reads the packet's header and decides the best next hop, based on the destination address and how busy the network is.
4. Packets may take **different routes** and may arrive **out of order**.
5. The receiving device uses the packet numbers to **reassemble** the data in the right order.
6. If a packet is missing or damaged, the receiver asks for it to be sent again.

Annotate a map: sender on the left, receiver on the right, five routers in between, drawing three different coloured paths.

Contrast with **circuit switching** (an old landline phone call): a dedicated connection is held for the whole call, so nobody else can use it. Packet switching is more efficient and more robust: if a router fails, packets go round it.

Key vocabulary: packet, header, payload, packet switching, router, hop, reassemble, IP address, sequence number.

## Activity (32 to 42 minutes): "Post the message"

**Setup:** give each group a short sentence (for example "THE CAT SAT ON THE MAT TODAY") and tell them to split it into packets of two or three words each.

**Version A (breakout rooms, groups of four):**

- Student 1 (sender) splits the sentence into numbered packets and writes the header: To, From, Packet number.
- Students 2 and 3 are routers. They receive packets and choose which route to pass them on (Route A or Route B).
- Student 4 (receiver) reassembles the sentence in the right order and reports back.

**Version B (whole class, if no breakouts):** you post packets one at a time into chat in jumbled order (for example 3, 1, 4, 2). Students type the reassembled sentence. Then remove one packet and ask what the receiver should do. (Request it again.)

**Extension:** "What if a packet's number is wrong?" "Why is it harder to read a message with a missing packet?"

## Quiz (42 to 48 minutes)

Use a Zoom poll or ask students to type the letter in chat.

**Q1.** What is a packet?
A. A whole file sent in one go
B. A small chunk of data with an address and number attached
C. A type of cable
D. A program that protects a computer

**Q2.** Which part of a packet contains the destination IP address?
A. The payload
B. The router
C. The header
D. The NIC

**Q3.** Why do packets often arrive out of order?
A. They take different routes through the network
B. The sender types them wrongly
C. The NIC reorders them
D. The payload is encrypted

**Q4.** What does the receiving device use to put packets back in the right order?
A. The size of each packet
B. The colour of each packet
C. The router's name
D. The packet number in the header

**Q5.** What happens if one packet goes missing?
A. The whole file must be re-sent from the start
B. Only the missing packet is requested again
C. The receiver ignores it
D. The router deletes the other packets

**Q6.** What does a router do with a packet?
A. Converts it into a signal for a cable
B. Splits the data into more packets
C. Stores it permanently
D. Reads the header and forwards it towards its destination

## Exit ticket (48 to 50 minutes)

In chat: "Explain in one sentence why the internet uses packets instead of sending a whole file at once."

Model answer: Splitting data into packets means that if one is lost only that part needs re-sending, and many users can share the network, because packets can take different routes.

## Homework (about 20 minutes)

1. Draw and label a packet with a header and payload.
2. A 12 MB file is split into packets of 1 MB. How many packets? What is the payload in packet 7?
3. Write a short paragraph (4 to 6 sentences) explaining packet switching to a younger student, using an analogy of your own.
4. Challenge: find out what the command `tracert` (Windows) or `traceroute` (Mac) does and describe what you see.

## Mark scheme and teacher notes

**Common misconceptions:**

- "Packets always take the same route." They do not.
- "Routers store the whole file." They only pass packets on.
- "Payload is the address." The payload is the data; the address is in the header.

**Differentiation:** support students with the analogy and sentence frames ("A packet is split into ... because ..."). Stretch students with TCP/IP, packet loss, latency, or why streaming video sometimes buffers.

**Homework answers:** Q2: 12 packets; packet 7 carries the seventh megabyte of the file. Q3: look for header, payload, numbering, different routes, reassembly.

ANSWER KEY: B C A D B D
