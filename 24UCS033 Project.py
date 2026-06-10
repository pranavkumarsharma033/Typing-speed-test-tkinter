import tkinter as tk
from tkinter import ttk, messagebox
import time
import random
import csv
import os
from datetime import datetime


TEST_DURATION = 60  


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(BASE_DIR, "typing_results.csv")

PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile language that you can use on the backend, frontend, or full stack.",
    "Typing tests help improve your accuracy and speed by encouraging proper finger placement and rhythm.",
    "Consistency beats intensidxty. Practicing for a few minutes every day often produces better results than long sessions.",
    "Baddi University students love building creative projects with Tkinter and Python in their first year.",
    "If you want to go fast, practice slowly. Precision first, then speed will follow naturally.",
    "Clean code is simple, direct, and easy to read. Add comments when necessary and name things well.",
    "In software development, small improvements every day lead to significant progress over time.",
]


def ensure_results_file():
    """Create CSV file if missing."""
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["DateTime", "Duration(s)", "WPM", "Accuracy(%)", "Errors", "CharsTyped"])  # header


def load_results_into_tree(tree: ttk.Treeview):
    """Load CSV results into the Treeview."""
    ensure_results_file()
    for item in tree.get_children():
        tree.delete(item)
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row:
                tree.insert("", tk.END, values=row)


def clear_results_file():
    """Clear CSV contents but keep the header."""
    ensure_results_file()
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["DateTime", "Duration(s)", "WPM", "Accuracy(%)", "Errors", "CharsTyped"])



class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Speed Test – Tkinter")
        self.geometry("950x600")
        self.minsize(900, 560)

        
        self.target_text = tk.StringVar()
        self.time_left = TEST_DURATION
        self.test_running = False
        self.start_time = None
        self.timer_job = None

        
        self.typed_chars = 0
        self.correct_chars = 0
        self.errors = 0

        self._build_ui()
        self._new_paragraph()
        ensure_results_file()
        load_results_into_tree(self.history_tree)

    
    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        
        top = ttk.Frame(container)
        top.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(top, text="New Text", command=self._new_paragraph).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Start (60s)", command=self.start_test).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Reset", command=self.reset_test).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Save Result", command=self.save_result).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Clear Records", command=self.clear_records).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Exit App", command=self.exit_app).pack(side=tk.RIGHT)

        
        metrics = ttk.Frame(container)
        metrics.pack(fill=tk.X, pady=(0, 8))

        self.timer_lbl = ttk.Label(metrics, text=f"Time: {TEST_DURATION}s", font=("Segoe UI", 12, "bold"))
        self.timer_lbl.pack(side=tk.LEFT)

        self.wpm_lbl = ttk.Label(metrics, text="WPM: 0.0")
        self.wpm_lbl.pack(side=tk.LEFT, padx=15)

        self.acc_lbl = ttk.Label(metrics, text="Accuracy: 100.0%")
        self.acc_lbl.pack(side=tk.LEFT, padx=15)

        self.err_lbl = ttk.Label(metrics, text="Errors: 0")
        self.err_lbl.pack(side=tk.LEFT, padx=15)

        
        target_frame = ttk.LabelFrame(container, text="Target Text")
        target_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 8))

        self.target_box = tk.Text(target_frame, height=6, wrap=tk.WORD, padx=8, pady=8, state=tk.DISABLED)
        self.target_box.pack(fill=tk.BOTH, expand=True)

        
        input_frame = ttk.LabelFrame(container, text="Type Here")
        input_frame.pack(fill=tk.BOTH, expand=True)

        self.input_box = tk.Text(input_frame, height=8, wrap=tk.WORD, padx=8, pady=8)
        self.input_box.pack(fill=tk.BOTH, expand=True)
        self.input_box.bind("<KeyRelease>", self.on_key_release)
        self.input_box.bind("<Control-BackSpace>", lambda e: "break")

        
        history_frame = ttk.LabelFrame(container, text="History (Saved Results)")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        cols = ("DateTime", "Duration(s)", "WPM", "Accuracy(%)", "Errors", "CharsTyped")
        self.history_tree = ttk.Treeview(history_frame, columns=cols, show="headings", height=6)
        for c in cols:
            self.history_tree.heading(c, text=c)
            self.history_tree.column(c, width=120, anchor=tk.CENTER)
        self.history_tree.pack(fill=tk.BOTH, expand=True)

        
        style = ttk.Style(self)
        try:
            self.call("source", "azure.tcl")
            style.theme_use("azure")
        except Exception:
            pass

        
        self.target_box.tag_configure("correct", background="#c8facc")
        self.target_box.tag_configure("wrong", background="#ffd6d6")
        self.target_box.tag_configure("next", underline=True)

    
    def _new_paragraph(self):  
        text = random.choice(PARAGRAPHS)
        self.target_text.set(text)
        self._render_target()
        self.reset_test(clear_input=True)

    def _render_target(self, typed: str = ""):
        target = self.target_text.get()
        self.target_box.config(state=tk.NORMAL)
        self.target_box.delete("1.0", tk.END)
        self.target_box.insert("1.0", target)
        self.target_box.tag_remove("correct", "1.0", tk.END)
        self.target_box.tag_remove("wrong", "1.0", tk.END)
        self.target_box.tag_remove("next", "1.0", tk.END)

        if typed:
            for i, ch in enumerate(typed):
                if i >= len(target):
                    break
                start = f"1.0+{i}c"
                end = f"1.0+{i+1}c"
                if ch == target[i]:
                    self.target_box.tag_add("correct", start, end)
                else:
                    self.target_box.tag_add("wrong", start, end)

        next_index = min(len(typed), len(target))
        self.target_box.tag_add("next", f"1.0+{next_index}c", f"1.0+{next_index+1}c")
        self.target_box.config(state=tk.DISABLED)

    def start_test(self):
        if self.test_running:
            return
        self.reset_test(clear_input=False)
        self.test_running = True
        self.start_time = time.time()
        self.time_left = TEST_DURATION
        self._tick()
        self.input_box.focus_set()

    def _tick(self):
        self.timer_lbl.config(text=f"Time: {self.time_left}s")
        if self.time_left <= 0:
            self.end_test()
            return
        self.time_left -= 1
        self.timer_job = self.after(1000, self._tick)

    def end_test(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.test_running = False
        self.input_box.config(state=tk.DISABLED)
        messagebox.showinfo("Time's up", "The test has ended. You can Save Result or Start again.")

    def reset_test(self, clear_input=True):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.test_running = False
        self.time_left = TEST_DURATION
        self.start_time = None
        self.timer_lbl.config(text=f"Time: {TEST_DURATION}s")
        self.typed_chars = 0
        self.correct_chars = 0
        self.errors = 0
        if clear_input:
            self.input_box.config(state=tk.NORMAL)
            self.input_box.delete("1.0", tk.END)
        else:
            self.input_box.config(state=tk.NORMAL)
        self._update_metrics_labels(0.0, 100.0, 0)
        self._render_target(self.input_box.get("1.0", tk.END).rstrip("\n"))

    def on_key_release(self, event):
        typed = self.input_box.get("1.0", tk.END).rstrip("\n")
        target = self.target_text.get()
        if not self.test_running and typed:
            self.start_test()

        self.typed_chars = len(typed)
        match_len = sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])
        self.correct_chars = match_len
        self.errors = max(self.typed_chars - self.correct_chars, 0)

        elapsed = (time.time() - self.start_time) if self.start_time else 0.000001
        minutes = max(elapsed / 60.0, 1e-6)
        gross_wpm = (self.typed_chars / 5.0) / minutes
        accuracy = (self.correct_chars / self.typed_chars * 100.0) if self.typed_chars > 0 else 100.0

        self._update_metrics_labels(gross_wpm, accuracy, self.errors)
        self._render_target(typed)

        if self.typed_chars >= len(target):
            self.end_test()

    def _update_metrics_labels(self, wpm, accuracy, errors):
        self.wpm_lbl.config(text=f"WPM: {wpm:.1f}")
        self.acc_lbl.config(text=f"Accuracy: {accuracy:.1f}%")
        self.err_lbl.config(text=f"Errors: {errors}")

    def save_result(self):
        if self.start_time is None and self.typed_chars == 0:
            messagebox.showwarning("Nothing to save", "Please take a test before saving.")
            return

        elapsed = (time.time() - self.start_time) if self.start_time else TEST_DURATION
        duration = min(int(elapsed), TEST_DURATION)
        minutes = max(elapsed / 60.0, 1e-6)
        gross_wpm = (self.typed_chars / 5.0) / minutes
        accuracy = (self.correct_chars / self.typed_chars * 100.0) if self.typed_chars > 0 else 100.0

        ensure_results_file()
        with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                duration,
                f"{gross_wpm:.1f}",
                f"{accuracy:.1f}",
                self.errors,
                self.typed_chars,
            ])
        load_results_into_tree(self.history_tree)
        messagebox.showinfo("Saved", "Result saved to typing_results.csv")

    
    def clear_records(self):
        """Clear all saved records."""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all saved records?"):
            clear_results_file()
            load_results_into_tree(self.history_tree)
            messagebox.showinfo("Cleared", "All records have been deleted.")

    def exit_app(self):
        """Exit the program."""
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.destroy()



if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()
