# Year 9 Python: while loops, programming tasks

**Assumptions:** one lesson of about 50-60 minutes, pupils use IDLE, Thonny or an online editor, and they know variables, `input()`, `if/elif/else` and `for` loops. Tasks are in order of difficulty. Tasks 1-5 are core, 6-7 are stretch, 8 is extension. Solutions are at the end.

## Key idea to establish first
A `for` loop repeats a set number of times. A `while` loop repeats **as long as a condition is True**. We use `while` when we do not know in advance how many repetitions are needed.

```python
count = 1
while count <= 3:
    print("Hello")
    count = count + 1
```

Three things every `while` loop needs: a starting value, a condition, and something inside the loop that changes the value (or the loop never ends).

Tell pupils how to stop a runaway program (Ctrl + C in the shell, or the Stop button) before they start.

---

## Task 1: Predict, run, explain
Do **not** run the code first. Write down what you think it prints, then run it.

```python
number = 10
while number > 0:
    print(number)
    number = number - 3
print("Finished")
```
a) What does it print? How many times does the loop run?
b) Change `number - 3` to `number - 2`. Predict the new output, then check.
c) Change the condition to `number >= 0`. What changes?

## Task 2: Countdown
Write a program that counts down from 10 to 1 and then prints "Blast off!". Then change it so the **user** types in the number to count down from.

## Task 3: Times table
Ask the user for a number. Use a `while` loop to print its times table from 1 x to 12 x, for example `3 x 4 = 12`.

## Task 4: Password checker
The password is `"python"`. Keep asking the user to enter the password until they get it right. Then print "Access granted".
*Hint:* start with a variable set to an empty string, and loop while the entered password is not equal to the correct one.

Extension: count how many attempts it took and print this at the end ("You took 3 attempts").

## Task 5: Running total
Ask the user to keep entering numbers. Add them up. Stop when the user enters `0`. At the end print the total.

Then extend it so it also prints **how many** numbers were entered (not counting the 0) and the **average**. Think about what happens if they enter 0 straight away.

## Task 6: Guess the number
Set a secret number (for example 7, or use `import random` and `random.randint(1, 20)`). Keep asking the user to guess. After each guess tell them "Too high" or "Too low". When they get it, tell them how many guesses they used.

## Task 7: Input validation
Ask the user for their age. Keep asking while the age is less than 0 or greater than 120, and print a helpful message each time. Once valid, print "Thank you".
*Think:* which is better here, `and` or `or` in your condition?

## Task 8: Extension challenges (choose one or more)
a) **Menu program.** Show a menu: 1) Say hello, 2) Tell a joke, 3) Quit. Keep showing the menu until the user chooses 3.

b) **Doubling game.** Start with a value of 1p. Keep doubling it. How many days until the value is over £1,000,000 (100,000,000p)? Print the day number and the amount each day.

c) **Digit counter.** Ask for a whole number and use a `while` loop with `// 10` to count how many digits it has, without converting to a string.

d) **Find the bug (debugging).** These two programs have problems. Fix them.

```python
# Program A
x = 1
while x < 5:
    print(x)

# Program B
total = 0
while total < 10
    total = total + 2
print(total)
```

---

## Solutions

**Task 1.** Output: 10, 7, 4, 1, then "Finished". Loop runs 4 times. (b) `-2`: 10, 8, 6, 4, 2 (5 times). (c) With `>= 0` and `-2`, it also prints 0 (loop runs 6 times). With `-3` and `>= 0`, it still stops after 1 (next value is -2), so output is unchanged.

**Task 2.**
```python
start = int(input("Count down from: "))
while start >= 1:
    print(start)
    start = start - 1
print("Blast off!")
```

**Task 3.**
```python
n = int(input("Which times table? "))
i = 1
while i <= 12:
    print(n, "x", i, "=", n * i)
    i = i + 1
```

**Task 4.**
```python
guess = ""
attempts = 0
while guess != "python":
    guess = input("Enter the password: ")
    attempts = attempts + 1
print("Access granted")
print("You took", attempts, "attempts")
```

**Task 5.**
```python
total = 0
count = 0
number = int(input("Enter a number (0 to stop): "))
while number != 0:
    total = total + number
    count = count + 1
    number = int(input("Enter a number (0 to stop): "))
print("Total:", total)
if count > 0:
    print("Numbers entered:", count)
    print("Average:", total / count)
else:
    print("No numbers were entered")
```
Teaching point: the input appears twice (before the loop and at the end of it). This is the standard "read ahead" pattern.

**Task 6.**
```python
import random
secret = random.randint(1, 20)
guess = 0
tries = 0
while guess != secret:
    guess = int(input("Guess the number (1-20): "))
    tries = tries + 1
    if guess < secret:
        print("Too low")
    elif guess > secret:
        print("Too high")
print("Correct! It took you", tries, "guesses")
```

**Task 7.**
```python
age = int(input("Enter your age: "))
while age < 0 or age > 120:
    print("That age is not valid. Try again.")
    age = int(input("Enter your age: "))
print("Thank you")
```
Use `or` because the age is invalid if **either** condition is true. Using `and` would never be True.

**Task 8a.**
```python
choice = ""
while choice != "3":
    print("1) Say hello  2) Tell a joke  3) Quit")
    choice = input("Choose: ")
    if choice == "1":
        print("Hello!")
    elif choice == "2":
        print("Why do programmers prefer dark mode? Because light attracts bugs.")
    elif choice != "3":
        print("Please choose 1, 2 or 3")
print("Goodbye")
```

**Task 8b.**
```python
amount = 1
day = 1
while amount <= 100000000:
    print("Day", day, ":", amount, "p")
    amount = amount * 2
    day = day + 1
```
(The value first exceeds 100,000,000p on day 28, when it is 134,217,728p.)

**Task 8c.**
```python
n = int(input("Enter a whole number: "))
digits = 0
if n == 0:
    digits = 1
while n > 0:
    n = n // 10
    digits = digits + 1
print("Digits:", digits)
```

**Task 8d.**
- Program A: infinite loop because `x` never changes. Add `x = x + 1` inside the loop.
- Program B: missing colon after the `while` condition. Also the output is 10 once fixed.

---

## Common errors to watch for
- Forgetting to update the variable (infinite loop).
- Using `=` instead of `==` in conditions.
- Comparing a string with a number (forgetting `int()` on input).
- Condition off by one (`<` vs `<=`).
- Indentation errors: the update line sitting outside the loop.
- Putting the `input()` only before the loop in validation tasks, so the user is never asked again.

## Quick plenary questions
1. When would you choose `while` over `for`?
2. What three things does every `while` loop need?
3. How can you stop a program stuck in an infinite loop?
