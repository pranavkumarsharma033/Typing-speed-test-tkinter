# ⌨️ Typing Speed Test — Python & Tkinter

A fully functional desktop typing speed test application built with Python and Tkinter.
Designed and developed as a first-year B.Tech CSE (AI & ML) project at Baddi University.

![App Screenshot](screenshot.png)

---

## Features

- 60-second countdown timer that auto-starts when you begin typing
- Real-time WPM (Words Per Minute) calculation
- Live accuracy percentage tracking
- Error counter updated with every keystroke
- Color-coded feedback — green for correct, red for incorrect characters
- Underline cursor showing your current position in the target text
- 8 built-in paragraphs selected randomly each session
- Save results to a local CSV file after each test
- View full test history in a scrollable table inside the app
- Clear all saved records with one click
- Clean and responsive UI built entirely with Tkinter

---

## Screenshots

> Add your screenshot here after running the app

![Typing Speed Test](screenshot.png)

---

## How to Run

### Requirements
- Python 3.7 or above
- Tkinter (comes built-in with standard Python installations)

### Steps

```bash
# Clone the repository
git clone https://github.com/pranavkumarsharma033/Typing-speed-test-tkinter.git

# Navigate into the folder
cd Typing-speed-test-tkinter

# Run the app
python "24UCS033 Project.py"
```

---

## How It Works

1. Click **Start (60s)** or just start typing — the timer begins automatically
2. Type the displayed paragraph as fast and accurately as you can
3. Your WPM, accuracy, and errors update in real time
4. When the timer hits zero (or you finish the paragraph), the test ends
5. Click **Save Result** to store your score
6. View all past scores in the History table at the bottom

---

## Metrics Explained

| Metric | How it is calculated |
|---|---|
| WPM | (Total characters typed / 5) / minutes elapsed |
| Accuracy | (Correct characters / Total characters typed) × 100 |
| Errors | Total characters typed minus correct characters |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| Tkinter | GUI framework for the desktop interface |
| CSV module | Saving and loading result history |
| Random module | Selecting paragraphs randomly |
| Time module | Timer and WPM calculation |

---

## What I Learned

- Building desktop GUI applications with Tkinter
- Real-time event handling using key bindings
- File I/O with Python's CSV module
- Calculating performance metrics like WPM and accuracy
- Structuring a Python project cleanly with functions and classes

---

## Author

**Pranav Kumar Sharma**
B.Tech CSE (AI & ML) — 2nd Year
Baddi University Of Emerging Sciences And Technology

- GitHub: [@pranavkumarsharma033](https://github.com/pranavkumarsharma033)
- LinkedIn: [Add your LinkedIn URL here]

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
