"""
Tkinter GUI for the Electronics Lab Teaching Suite.
Designed for classroom projection and student self-study.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from Teaching.lessons import LESSONS
from Teaching.quiz import get_random_question
from Electronics.circuits import RCCircuit, RLCircuit
from Electronics.filters import LowPassFilter, HighPassFilter
from Electronics.utils import db


class TeachingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Undergraduate Electronics Lab Teaching Suite")
        self.root.geometry("1200x800")

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.tab_lessons = ttk.Frame(notebook)
        self.tab_rc = ttk.Frame(notebook)
        self.tab_filter = ttk.Frame(notebook)
        self.tab_rlc = ttk.Frame(notebook)
        self.tab_quiz = ttk.Frame(notebook)

        notebook.add(self.tab_lessons, text="📚 Lessons")
        notebook.add(self.tab_rc, text="⚡ RC Circuit")
        notebook.add(self.tab_filter, text="📉 Filters")
        notebook.add(self.tab_rlc, text="🎛️ RLC / Resonance")
        notebook.add(self.tab_quiz, text="🧠 Quiz")

        self._build_lessons_tab()
        self._build_rc_tab()
        self._build_filter_tab()
        self._build_rlc_tab()
        self._build_quiz_tab()

    # ---------- LESSONS TAB ----------
    def _build_lessons_tab(self):
        left = ttk.Frame(self.tab_lessons)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

        ttk.Label(left, text="Select lesson:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.lesson_list = tk.Listbox(left, width=34, height=20, font=("Courier", 10))
        for name in LESSONS.keys():
            self.lesson_list.insert(tk.END, name)
        self.lesson_list.pack(fill=tk.Y, expand=True)
        self.lesson_list.bind("<<ListboxSelect>>", self._on_lesson_select)

        right = ttk.Frame(self.tab_lessons)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.lesson_text = tk.Text(right, wrap="word", font=("Arial", 11), padx=10, pady=10)
        self.lesson_text.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(right)
        btn_frame.pack(fill=tk.X, pady=4)
        ttk.Button(btn_frame, text="▶ Run Live Demo", command=self._run_lesson_demo).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="💡 Show Exercise Answer", command=self._show_answer).pack(side=tk.LEFT, padx=8)

        self._current_lesson = None

    def _on_lesson_select(self, event):
        sel = self.lesson_list.curselection()
        if not sel:
            return
        name = self.lesson_list.get(sel[0])
        self._current_lesson = name
        L = LESSONS[name]
        self.lesson_text.delete("1.0", tk.END)
        self.lesson_text.insert(tk.END, f"📘 {name}\n\n", "header")
        self.lesson_text.insert(tk.END, L["theory"] + "\n\n", "body")
        self.lesson_text.insert(tk.END, "🎯 Exercise:\n", "header2")
        self.lesson_text.insert(tk.END, L["exercise"] + "\n\n", "body")
        self.lesson_text.tag_config("header", font=("Arial", 14, "bold"), foreground="#1a4d8f")
        self.lesson_text.tag_config("header2", font=("Arial", 11, "bold"), foreground="#a04b00")
        self.lesson_text.tag_config("body", font=("Arial", 11))

    def _run_lesson_demo(self):
        if not self._current_lesson:
            messagebox.showinfo("Select lesson", "Choose a lesson first.")
            return
        result = LESSONS[self._current_lesson]["demo"]()
        msg = "\n".join(f"{k}: {v}" for k, v in result.items())
        messagebox.showinfo(f"Live Demo — {self._current_lesson}", msg)

    def _show_answer(self):
        if not self._current_lesson:
            return
        messagebox.showinfo("Answer", LESSONS[self._current_lesson]["answer"])

    # ---------- RC TAB ----------
    def _build_rc_tab(self):
        top = ttk.Frame(self.tab_rc)
        top.pack(fill=tk.X, padx=8, pady=8)

        self.rc_R = tk.DoubleVar(value=1000)
        self.rc_C = tk.DoubleVar(value=10e-6)
        self.rc_mode = tk.StringVar(value="Charge")

        ttk.Label(top, text="R (Ω):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.rc_R, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="C (F):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.rc_C, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="Mode:").pack(side=tk.LEFT)
        ttk.Combobox(top, textvariable=self.rc_mode, values=["Charge", "Discharge"],
                     state="readonly", width=10).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Plot", command=self._plot_rc).pack(side=tk.LEFT, padx=8)

        self.rc_info = tk.StringVar(value="Enter R, C and click Plot.")
        ttk.Label(self.tab_rc, textvariable=self.rc_info, font=("Courier", 10)).pack(anchor="w", padx=8)

        self.rc_fig = Figure(figsize=(10, 4), dpi=100)
        self.rc_ax = self.rc_fig.add_subplot(111)
        self.rc_canvas = FigureCanvasTkAgg(self.rc_fig, master=self.tab_rc)
        self.rc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _plot_rc(self):
        try:
            rc = RCCircuit(R=self.rc_R.get(), C=self.rc_C.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if self.rc_mode.get() == "Charge":
            t, v = rc.step_response()
            label = "Capacitor voltage (charging)"
        else:
            t, v = rc.discharge_response()
            label = "Capacitor voltage (discharging)"

        self.rc_ax.clear()
        self.rc_ax.plot(t, v, color="steelblue", lw=2, label=label)
        self.rc_ax.axvline(rc.tau, color="red", ls="--", lw=1, label=f"τ = {rc.tau*1000:.2f} ms")
        self.rc_ax.axhline(rc.Vin * 0.632, color="green", ls=":", lw=1, label="63.2% of Vin")
        self.rc_ax.set_xlabel("Time (s)")
        self.rc_ax.set_ylabel("Voltage (V)")
        self.rc_ax.set_title("RC Circuit Step Response")
        self.rc_ax.grid(True, alpha=0.3)
        self.rc_ax.legend()
        self.rc_canvas.draw()

        self.rc_info.set(
            f"τ = {rc.tau*1000:.2f} ms   |   fc = {rc.cutoff_frequency():.1f} Hz   |   "
            f"Steady-state V = {rc.Vin:.2f} V"
        )

    # ---------- FILTER TAB ----------
    def _build_filter_tab(self):
        top = ttk.Frame(self.tab_filter)
        top.pack(fill=tk.X, padx=8, pady=8)

        self.f_R = tk.DoubleVar(value=1000)
        self.f_C = tk.DoubleVar(value=10e-6)
        self.f_type = tk.StringVar(value="Low-pass")

        ttk.Label(top, text="R (Ω):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.f_R, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="C (F):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.f_C, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="Type:").pack(side=tk.LEFT)
        ttk.Combobox(top, textvariable=self.f_type, values=["Low-pass", "High-pass"],
                     state="readonly", width=12).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Plot Bode", command=self._plot_filter).pack(side=tk.LEFT, padx=8)

        self.filter_fig = Figure(figsize=(10, 5), dpi=100)
        self.filter_ax1 = self.filter_fig.add_subplot(211)
        self.filter_ax2 = self.filter_fig.add_subplot(212)
        self.filter_canvas = FigureCanvasTkAgg(self.filter_fig, master=self.tab_filter)
        self.filter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _plot_filter(self):
        try:
            if self.f_type.get() == "Low-pass":
                flt = LowPassFilter(R=self.f_R.get(), C=self.f_C.get())
            else:
                flt = HighPassFilter(R=self.f_R.get(), C=self.f_C.get())
            freqs, H = flt.frequency_response()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        mag_db = 20 * np.log10(np.abs(H))
        phase = np.angle(H, deg=True)
        fc = flt.cutoff_frequency()

        self.filter_ax1.clear()
        self.filter_ax1.semilogx(freqs, mag_db, color="steelblue", lw=2)
        self.filter_ax1.axvline(fc, color="red", ls="--", lw=1, label=f"fc = {fc:.1f} Hz")
        self.filter_ax1.axhline(-3, color="green", ls=":", lw=1, label="-3 dB")
        self.filter_ax1.set_ylabel("Gain (dB)")
        self.filter_ax1.set_title(f"Bode Plot — {self.f_type.get()} Filter")
        self.filter_ax1.grid(True, which="both", alpha=0.3)
        self.filter_ax1.legend()

        self.filter_ax2.clear()
        self.filter_ax2.semilogx(freqs, phase, color="darkorange", lw=2)
        self.filter_ax2.axvline(fc, color="red", ls="--", lw=1)
        self.filter_ax2.set_xlabel("Frequency (Hz)")
        self.filter_ax2.set_ylabel("Phase (°)")
        self.filter_ax2.grid(True, which="both", alpha=0.3)

        self.filter_fig.tight_layout()
        self.filter_canvas.draw()

    # ---------- RLC TAB ----------
    def _build_rlc_tab(self):
        top = ttk.Frame(self.tab_rlc)
        top.pack(fill=tk.X, padx=8, pady=8)

        self.rlc_R = tk.DoubleVar(value=200)
        self.rlc_L = tk.DoubleVar(value=10e-3)
        self.rlc_C = tk.DoubleVar(value=1e-6)

        ttk.Label(top, text="R (Ω):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.rlc_R, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="L (H):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.rlc_L, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Label(top, text="C (F):").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.rlc_C, width=10).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Simulate", command=self._plot_rlc).pack(side=tk.LEFT, padx=8)

        self.rlc_info = tk.StringVar(value="Enter R, L, C and click Simulate.")
        ttk.Label(self.tab_rlc, textvariable=self.rlc_info,
                  font=("Courier", 10)).pack(anchor="w", padx=8)

        self.rlc_fig = Figure(figsize=(10, 4), dpi=100)
        self.rlc_ax = self.rlc_fig.add_subplot(111)
        self.rlc_canvas = FigureCanvasTkAgg(self.rlc_fig, master=self.tab_rlc)
        self.rlc_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    def _plot_rlc(self):
        try:
            rlc = RLCircuit(R=self.rlc_R.get(), L=self.rlc_L.get(), C=self.rlc_C.get())
            t, v = rlc.step_response()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        f0 = rlc.resonant_frequency()
        zeta = rlc.damping_factor()

        self.rlc_ax.clear()
        self.rlc_ax.plot(t * 1000, v, color="purple", lw=2, label="Capacitor voltage")
        self.rlc_ax.set_xlabel("Time (ms)")
        self.rlc_ax.set_ylabel("Voltage (V)")
        self.rlc_ax.set_title(f"RLC Step Response — {rlc.response_type()}")
        self.rlc_ax.grid(True, alpha=0.3)
        self.rlc_ax.legend()
        self.rlc_canvas.draw()

        self.rlc_info.set(
            f"f0 = {f0:.2f} Hz   |   ζ = {zeta:.3f}   |   "
            f"Q = {1 / (2 * zeta):.2f}   |   {rlc.response_type()}"
        )

    # ---------- QUIZ TAB ----------
    def _build_quiz_tab(self):
        top = ttk.Frame(self.tab_quiz)
        top.pack(fill=tk.X, padx=8, pady=8)

        ttk.Button(top, text="🎲 New Question", command=self._new_quiz).pack(side=tk.LEFT)
        self.quiz_score = tk.StringVar(value="Score: 0 / 0")
        ttk.Label(top, textvariable=self.quiz_score,
                  font=("Arial", 11, "bold")).pack(side=tk.RIGHT)

        self.quiz_q_text = tk.Text(self.tab_quiz, height=3, wrap="word",
                                   font=("Arial", 12), padx=10, pady=10)
        self.quiz_q_text.pack(fill=tk.X, padx=8, pady=(0, 8))

        self.quiz_options_frame = ttk.Frame(self.tab_quiz)
        self.quiz_options_frame.pack(fill=tk.X, padx=8)

        self.quiz_feedback = tk.StringVar(value="")
        ttk.Label(self.tab_quiz, textvariable=self.quiz_feedback,
                  font=("Arial", 11, "italic"), foreground="#1a4d8f").pack(
            anchor="w", padx=8, pady=8)

        self._quiz_correct = 0
        self._quiz_total = 0
        self._current_question = None

    def _new_quiz(self):
        for w in self.quiz_options_frame.winfo_children():
            w.destroy()

        q = get_random_question()
        self._current_question = q
        self.quiz_q_text.delete("1.0", tk.END)
        self.quiz_q_text.insert(tk.END, q["q"])
        self.quiz_feedback.set("")

        for i, opt in enumerate(q["options"]):
            ttk.Button(
                self.quiz_options_frame,
                text=f"{chr(65 + i)}. {opt}",
                command=lambda idx=i: self._check_quiz(idx),
            ).pack(anchor="w", pady=2)

    def _check_quiz(self, idx: int):
        q = self._current_question
        if q is None:
            return
        self._quiz_total += 1
        if idx == q["answer"]:
            self._quiz_correct += 1
            self.quiz_feedback.set(f"✅ Correct! {q['explain']}")
        else:
            correct = q["options"][q["answer"]]
            self.quiz_feedback.set(f"❌ Not quite. Correct: {correct}. {q['explain']}")
        self.quiz_score.set(f"Score: {self._quiz_correct} / {self._quiz_total}")

    # ---------- RUN ----------
    def run(self):
        self.root.mainloop()