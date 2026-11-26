---
name: flashcard-deck-builder
description: Build a flashcard deck for a topic with one fact per card, the question on the front and a precise answer on the back, ordered for spaced practice and exportable to Anki, Quizlet, CSV or a printable sheet. Use when a teacher or student asks for flashcards, revision cards, an Anki deck, a Quizlet set or cards to test themselves.
---

# Flashcard Deck Builder

> If `teaching-context.md` exists, read it first, follow its house rules, and don't ask for anything it already answers.

Good flashcards are small. One card, one fact, one clear answer. A card with a paragraph on the back gets read, not recalled.

## Rules for each card

1. **One atomic fact per card.** Split "RAM is volatile and stores running programs" into two cards.
2. **The front is a question, not a word.** "What happens to RAM's contents when the power goes off?" beats "RAM".
3. **The back is short and exact**: the answer an examiner credits, in under 15 words where possible.
4. **Both directions for key terms**: term to definition, and definition to term.
5. **Cloze cards for lists and processes**: "The fetch stage copies the address from the PC to the {{MAR}}".
6. **Examples beat abstractions**: add one concrete example card for every abstract definition.
7. **No trick wording, no ambiguity.** If two answers could be right, rewrite the front.

## Steps

1. Take the topic from the specification, knowledge organiser or lesson notes.
2. List the facts students must recall. Cut nice-to-know.
3. Write 20 to 40 cards, tagged by sub-topic.
4. Order them so related cards aren't back to back (interleaving), but foundational cards come before the ones that depend on them.
5. Add 3 to 5 "mix-up" cards for the pairs students confuse.

## Output

- A table: front, back, tag
- An export in the format asked for: Anki-ready CSV (front;back;tags), Quizlet (term tab definition), or a printable cut-out sheet
- Three lines for students on how to use them: say the answer out loud before flipping, sort into know / not yet, revisit "not yet" tomorrow
