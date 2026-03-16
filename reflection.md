# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, it looked functional on the surface but almost nothing worked correctly under the hood. The difficulty ranges were swapped — Hard showed 1–50 while Normal showed 1–100, which made no sense. The hints were completely backwards: when my guess was too high, the app told me to go higher, actively steering me in the wrong direction. On top of that, the "New Game" button did nothing after a game ended because the game status was never reset, and the attempt counter started at 1 instead of 0, so I was losing an attempt before I even made a guess. After exhausting all attempts, the app revealed a secret number that was completely outside the difficulty range — the actual number generation logic was broken too.

---

## 2. How did you use AI as a teammate?

I used Claude Code throughout this project. I first ran the app myself and made a list of all the bugs I could find, then brought that list to Claude to map each bug to the exact lines responsible — that process was really useful for getting precise file and line references quickly. One suggestion that was clearly correct: Claude identified that the `attempts` counter starting at `1` instead of `0` was the shared root cause of both the off-by-one display bug and the "Out of attempts!" message firing on the last valid attempt — I verified this by tracing through the attempt count manually and confirming both issues disappeared after changing the initial value to `0`.

---

## 3. Debugging and testing your fixes

For most bugs I verified the fix by reading through the relevant code path and tracing the logic manually before running anything — if the fix made sense to me, I then ran the app to confirm that the behavior changed. For the scoring bug specifically, I actually played a full game in Hard mode and got a final score of 0 after winning on attempt 7, which told me the wrong-guess deductions were silently canceling out the win bonus; that manual test exposed the problem clearly. I also ran the full pytest suite after completing the refactor to `logic_utils.py`, and it immediately caught that the original 3 test cases had wrong assertions — they were comparing `check_guess()` output against a plain string, but the function returns a tuple. Claude helped design the broader test suite by systematically covering boundary values (like guessing exactly `low` and exactly `high`) and edge cases (None input, decimal input, unknown difficulty), which I wouldn't have covered as thoroughly on my own.

---

## 4. What did you learn about Streamlit and state?

The secret number appeared to change because on every even-numbered attempt, the code was converting the secret to a string and passing it into `check_guess()` — this caused Python to do string comparison instead of numeric comparison, so the "Too High" / "Too Low" hints were based on alphabetical ordering rather than actual value. That made the hints feel random and inconsistent, as if the target was shifting. The way I'd explain Streamlit reruns to someone: every time a user interacts with the app — clicks a button, types something — Streamlit reruns the entire Python script from top to bottom, like hitting refresh. Session state is a dictionary that persists across those reruns, so values you store there survive the restart instead of being reset to their defaults each time. The key fix for stabilizing the secret was wrapping its generation in `if "secret" not in st.session_state` — that guard means a new random number is only picked on the very first run, and every subsequent rerun just reads the already-stored value.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is playing the app myself before touching any code — having a concrete list of observed failures made every conversation with Claude much more focused and productive, rather than asking it to review the code blindly. Next time I work with AI on a debugging task, I'd push it harder on root cause analysis upfront rather than fixing bugs one by one; some of the bugs here shared the same underlying issue (like the `attempts` counter), and catching that earlier would have saved steps. This project changed how I think about AI-generated code: I used to assume that if code ran without errors it was probably correct, but this app ran fine and still had logic that was fundamentally broken in multiple places — AI code needs the same skeptical, test-first review that any code does.
