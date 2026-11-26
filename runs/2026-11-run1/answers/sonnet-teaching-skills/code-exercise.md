# Year 9 Python: first lesson on `while` loops

*Assumptions: Python 3, about 55 minutes, students have a place to run code (IDLE, Thonny, an online editor). They know variables, `input()`, `if` and `for`. Tasks climb from predict to make. Everyone starts at Task 1; stronger students can skip to the debugging and make tasks once their predictions are right.*

**Big idea for students:** a `for` loop repeats a set number of times. A `while` loop repeats **for as long as a condition is true**, even when you don't know how many times that will be.

**Suggested timing:** Tasks 1-2 (12 min), Task 3 (5), Task 4 (8), Tasks 5-7 (15), Task 8 debugging (7), Task 9 Parsons (as a quick alternative or extension), Challenge (rest).

---

## Student tasks

### Task 1: Predict, then run

```python
count = 1
while count <= 5:
    print(count)
    count = count + 1
print("Done")
```

a) Write down what you think it prints. Then run it.
b) How many times did the loop run?
c) What is the value of `count` after the loop ends?

### Task 2: Trace it

```python
total = 0
number = 1
while total < 10:
    total = total + number
    number = number + 1
print(total)
```

Complete a trace table (columns: `total`, `number`, `total < 10?`) by hand. Then run the code and check. What does it print, and why did the loop stop?

### Task 3: Investigate

a) Which of these could you do with a `for` loop, and which needs a `while` loop? Explain why.
   1. Print "Hello" 10 times.
   2. Keep asking for a password until it's right.
   3. Keep adding numbers until the total goes over 100.
   4. Print the 7 times table up to 7 x 12.
b) In Task 1, what would happen if you deleted the line `count = count + 1`? Predict first, then test it. (Press **Ctrl+C** in the console to stop a runaway program.)

### Task 4: Modify

Start from the Task 1 code.

a) Make it **count down from 10 to 1**, then print "Lift off!"
b) Make it print the **5 times table** (5, 10, 15 ... 60).
c) Make it print only the **even** numbers from 2 to 20.

### Task 5: Make, "Password"

Write a program that asks the user for a password. If it's wrong, say "Wrong, try again" and ask again. When it's right, print "Access granted". The password is `python`.

### Task 6: Make, "Check the input"

Write a program that asks for a number from 1 to 10. Keep asking until the user gives a number in that range. Then print "You chose" and the number.

### Task 7: Make, "Running total"

Write a program that keeps asking the user for numbers and adds them up. When the user types `0`, stop and print the total.

### Task 8: Debug

Each program has bugs. Find them and fix them.

**Program A** (should print 1 to 5):
```python
number = 1
while number <= 5
    print(number)
```

**Program B** (should print 1 to 5, but only prints 1 to 4):
```python
number = 1
while number < 5:
    print(number)
    number = number + 1
```

**Program C** (should count down from 10 to 1):
```python
number = 10
while number > 0:
    print(number)
    number = number + 1
```

### Task 9: Put the lines in order (Parsons)

These lines make a program that asks the user to guess a secret word until they get it right. Put them in the right order and add the indentation.

```
print("You got it!")
guess = input("Guess the word: ")
while guess != secret:
    guess = input("Guess again: ")
secret = "banana"
    print("Not quite.")
```

### Challenge A: Guess the number

Use `import random` and `random.randint(1, 20)` to pick a secret number. Let the player guess. After each guess, say "Too low" or "Too high". When they get it, say how many guesses it took.

### Challenge B: Doubling

You start with 1p, and the amount doubles every day. Use a `while` loop to work out **how many days** it takes to pass £1,000,000 (100,000,000p). Print the answer. (Hint: work in pence.)

---

## Hints (reveal one at a time)

- **Task 4a:** Start `count` at 10. Change the condition so the loop runs while `count` is at least 1. Subtract instead of add.
- **Task 5:** Ask for the password *before* the loop. The loop condition should be "the guess is **not** the password". Ask again *inside* the loop.
- **Task 6:** The condition needs to be true when the number is *wrong*. Think: smaller than 1 *or* bigger than 10.
- **Task 7:** Ask for the first number before the loop. Inside, add it to `total`, then ask again. Don't add the 0.
- **Challenge A:** You need a variable for the number of guesses. Add 1 each time round the loop.
- **Challenge B:** Start `amount = 1` and `days = 0`. Each time round, double the amount and add 1 to days.

---

## Test cases

| Task | Input | Expected output |
|---|---|---|
| 4a | none | 10 down to 1, then "Lift off!" |
| 4b | none | 5, 10, 15 ... 60 |
| 4c | none | 2, 4, 6 ... 20 |
| 5 | python | Access granted |
| 5 | pyhton, python | Wrong, try again, then Access granted |
| 6 | 5 | You chose 5 |
| 6 | 0, 11, 7 | two rejections, then You chose 7 |
| 6 | 1 (boundary) | You chose 1 |
| 6 | 10 (boundary) | You chose 10 |
| 7 | 5, 10, 0 | total is 15 |
| 7 | 0 | total is 0 |
| 7 | -3, 3, 0 | total is 0 |
| Challenge B | none | 27 |

---

## Teacher solutions sheet

**Task 1:** a) 1 2 3 4 5 Done (each on its own line). b) 5 times. c) 6.

**Task 2:** Trace:

| total | number | total < 10? |
|---|---|---|
| 0 | 1 | yes |
| 1 | 2 | yes |
| 3 | 3 | yes |
| 6 | 4 | yes |
| 10 | 5 | no, stop |

Prints 10. The loop stops when `total` reaches 10 because `10 < 10` is false.

**Task 3:** a) 1: `for` (known count). 2: `while` (unknown count). 3: `while`. 4: `for` is neater (known range), but `while` also works. b) Infinite loop: `count` stays 1, so the condition is always true and it prints 1 forever.

**Task 4:**
```python
# a
count = 10
while count >= 1:
    print(count)
    count = count - 1
print("Lift off!")

# b
count = 5
while count <= 60:
    print(count)
    count = count + 5

# c
count = 2
while count <= 20:
    print(count)
    count = count + 2
```

**Task 5:**
```python
password = "python"
guess = input("Enter the password: ")
while guess != password:
    print("Wrong, try again")
    guess = input("Enter the password: ")
print("Access granted")
```

**Task 6:**
```python
choice = int(input("Enter a number from 1 to 10: "))
while choice < 1 or choice > 10:
    print("That is not between 1 and 10")
    choice = int(input("Enter a number from 1 to 10: "))
print("You chose", choice)
```

**Task 7:**
```python
total = 0
number = int(input("Enter a number (0 to stop): "))
while number != 0:
    total = total + number
    number = int(input("Enter a number (0 to stop): "))
print("The total is", total)
```

**Task 8:**
- A: missing colon after the condition (syntax); no `number = number + 1`, so it would loop forever (logic).
- B: should be `number <= 5` (off by one).
- C: `number = number + 1` should be `number = number - 1` (it counts the wrong way and never ends).

**Task 9:**
```python
secret = "banana"
guess = input("Guess the word: ")
while guess != secret:
    print("Not quite.")
    guess = input("Guess again: ")
print("You got it!")
```

**Challenge A:**
```python
import random
secret = random.randint(1, 20)
guesses = 0
guess = 0
while guess != secret:
    guess = int(input("Guess the number (1-20): "))
    guesses = guesses + 1
    if guess < secret:
        print("Too low")
    elif guess > secret:
        print("Too high")
print("Correct! It took you", guesses, "guesses")
```

**Challenge B:**
```python
amount = 1
days = 0
while amount <= 100000000:
    amount = amount * 2
    days = days + 1
print(days)
```
Prints 27. (After 26 days the amount is 2^26 = 67,108,864p, still under 100,000,000p. After 27 days it is 134,217,728p, which is over.)

---

## Common mistakes and why they fail

1. **Forgetting to change the variable inside the loop** (e.g. no `count = count + 1`): the condition never becomes false, so the loop runs forever. Teach Ctrl+C early.
2. **Using `=` instead of `==` or `!=` in the condition:** `while guess = password:` is a syntax error. `=` assigns; `==` compares.
3. **Asking for input only once (before the loop, or only inside it):** the first, or the repeat, is missing. Pattern: ask once before the loop, ask again at the end of the loop body.
4. **Wrong condition direction:** `while guess == password:` runs only when it's *right*. Say it aloud: "keep going while it's wrong."
5. **Off by one:** `<` vs `<=`. Use the trace table to check the last value.
6. **Forgetting `int()` around `input()`** for numbers, so `choice < 1` compares text with a number and crashes.
7. **Adding the sentinel (0) to the total** in Task 7 because the check is done after the addition.

Look out for students copying a task's pattern without understanding it. A quick check: ask them what happens on a wrong guess, line by line.
