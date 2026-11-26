# Year 9 Python: while loops

**Assumptions:** one 60-minute lesson, Python 3, students already know variables, `input()`, `if` and `for`. The lesson builds a ladder: predict, run, investigate, modify, make, with a debugging task and a Parsons problem.

**Learning goal:** a `while` loop repeats while its condition is `True`. Something inside the loop must change the condition, or the loop never stops.

---

## Task 1: Predict

Students read this code and write down the output before running it.

```python
count = 1
while count <= 3:
    print("Hello", count)
    count = count + 1
print("Done")
```

**Hint 1:** Write the value of `count` on paper before each line runs.
**Hint 2:** Check the condition before every loop, including the last time.
**Hint 3:** Use the trace table in Task 2 to check your prediction.

## Task 2: Run and investigate

Students run Task 1 and complete this trace table.

| Step | `count` at start | Is `count <= 3`? | Printed |
|---|---|---|---|
| 1 | 1 | Yes | Hello 1 |
| 2 | 2 | Yes | Hello 2 |
| 3 | 3 | Yes | Hello 3 |
| 4 | 4 | No | (loop stops) |

Questions to answer in pairs:
1. Why does the loop stop after `Hello 3`?
2. What would happen if the line `count = count + 1` were removed?

## Task 3: Modify

Starter code:

```python
count = 5
while count >= 1:
    print(count)
    count = count - 1
print("Blast off!")
```

**Goal:** change this code so it counts up from 1 to 5 and then prints `Launch!`.

**Hint 1:** Which way does the number need to move, and what must the condition be?
**Hint 2:** Start `count` at 1 and use `<=`.
**Hint 3:** Only the first line, the condition and the increment need to change.

**Model solution:**
```python
count = 1
while count <= 5:
    print(count)
    count = count + 1
print("Launch!")
```

## Task 4: Predict a trap

```python
total = 0
while total < 10:
    total = total + 3
print(total)
```

Students predict the output, then run it.

**Answer:** `12` (the total goes 0, 3, 6, 9, 12, and the loop stops once it reaches 12).
**Common wrong answer:** `9`. This happens when students stop the loop as soon as they see a value near 10 and do not check the condition again.

## Task 5: Make (input with a range check)

**Task:** Keep asking the user for a number until they enter one from 1 to 10. Then print `Thanks, you picked` and the number.

**Hint 1:** You need to ask once before the loop starts.
**Hint 2:** The loop condition must be true while the number is out of range.
**Hint 3:** Ask for the number again inside the loop.

**Model solution:**
```python
number = int(input("Pick a number from 1 to 10: "))
while number < 1 or number > 10:
    print("That is not in range.")
    number = int(input("Pick a number from 1 to 10: "))
print("Thanks, you picked", number)
```

**Test cases (type these in, in order):**

| Inputs | Expected printed output (last line) |
|---|---|
| `0`, `11`, `7` | `Thanks, you picked 7` (after two "not in range" messages) |
| `1` | `Thanks, you picked 1` (boundary, no messages) |
| `10` | `Thanks, you picked 10` (boundary, no messages) |

## Task 6: Make (password check)

**Task:** Ask for a password. Keep asking until the user types `pizza`, then print `Access granted`.

**Model solution:**
```python
password = input("Password: ")
while password != "pizza":
    password = input("Wrong. Password: ")
print("Access granted")
```

**Extension:** Add a line that counts attempts and stops after three wrong guesses.

## Debugging task

This program has three planted bugs. Students find and fix all three.

```python
count = 1
while count < 5
    print(count)
    count = count - 1
print("Finished")
```

1. **Syntax:** the `while` line is missing its colon.
2. **Logic:** `count - 1` moves the wrong way, so the loop never ends.
3. **Off-by-one:** `< 5` stops at 4, but the goal is to print 1 to 5, so it needs `<= 5`.

**Fixed version:**
```python
count = 1
while count <= 5:
    print(count)
    count = count + 1
print("Finished")
```

## Parsons problem

Put these lines in the correct order. Indentation matters.

```
print("Game over")
lives = 3
lives = lives - 1
while lives > 0:
    print("Keep going")
```

**Correct order:**
```python
lives = 3
while lives > 0:
    print("Keep going")
    lives = lives - 1
print("Game over")
```

## Common errors (for the teacher)

- **Infinite loop:** the variable in the condition never changes. Ask: "Where does the condition change?"
- **Off-by-one:** `<` used where `<=` is needed, or the reverse.
- **Missing colon or wrong indentation:** the line after `while` must end in a colon, and the loop body must be indented.
- **Choosing `while` when `for` fits:** if the number of repeats is known, a `for` loop is simpler. Ask students to compare the two.

## Teacher solutions sheet

| Task | Answer |
|---|---|
| 1 (predict) | Hello 1, Hello 2, Hello 3, Done |
| 2 | Loop stops because `count` becomes 4 and `4 <= 3` is False; without the increment it prints `Hello 1` forever |
| 3 | Code in Task 3 model solution |
| 4 | `12` |
| 5 | Model solution; test table above |
| 6 | Model solution |
| Debugging | Colon added, `count + 1`, `<= 5` |
| Parsons | `lives = 3`, `while`, `print`, `lives - 1`, `print("Game over")` |
