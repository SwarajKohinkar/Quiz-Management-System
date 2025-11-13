import tkinter as tk
from tkinter import messagebox
import json
import os

QUIZ_FILE = "quiz_data.json"

# ---------- Helper Functions ----------
def load_quiz_data():
    """Load quiz questions from JSON file."""
    if not os.path.exists(QUIZ_FILE):
        return []
    with open(QUIZ_FILE, "r") as f:
        return json.load(f)

def save_quiz_data(data):
    """Save quiz questions to JSON file."""
    with open(QUIZ_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- GUI Application ----------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Management System")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        self.root.config(bg="#F0F4F8")

        # Default users (you can later load from file)
        self.teacher_credentials = {"teacher": "1234"}
        self.student_credentials = {"student": "abcd"}

        self.logged_in_user = None
        self.user_role = None

        self.show_login()

    # ---------- LOGIN SCREEN ----------
    def show_login(self):
        self.clear_window()

        tk.Label(self.root, text="🔐 Quiz System Login", font=("Arial", 26, "bold"), bg="#F0F4F8").pack(pady=40)

        tk.Label(self.root, text="Select Role:", font=("Arial", 14), bg="#F0F4F8").pack(pady=5)

        self.role_var = tk.StringVar(value="Teacher")

        role_frame = tk.Frame(self.root, bg="#F0F4F8")
        role_frame.pack(pady=5)
        tk.Radiobutton(role_frame, text="Teacher", variable=self.role_var, value="Teacher", font=("Arial", 12),
                       bg="#F0F4F8").grid(row=0, column=0, padx=20)
        tk.Radiobutton(role_frame, text="Student", variable=self.role_var, value="Student", font=("Arial", 12),
                       bg="#F0F4F8").grid(row=0, column=1, padx=20)

        frame = tk.Frame(self.root, bg="#F0F4F8")
        frame.pack(pady=20)

        tk.Label(frame, text="Username:", font=("Arial", 12), bg="#F0F4F8").grid(row=0, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12), bg="#F0F4F8").grid(row=1, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(frame, show="*", width=25)
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.root, text="Login", bg="#2196F3", fg="white", font=("Arial", 13), width=15,
                  command=self.handle_login).pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if role == "Teacher":
            if username in self.teacher_credentials and self.teacher_credentials[username] == password:
                self.logged_in_user = username
                self.user_role = "Teacher"
                self.show_home()
            else:
                messagebox.showerror("Error", "Invalid teacher credentials!")
        else:
            if username in self.student_credentials and self.student_credentials[username] == password:
                self.logged_in_user = username
                self.user_role = "Student"
                self.show_home()
            else:
                messagebox.showerror("Error", "Invalid student credentials!")

    # ---------- HOME SCREEN ----------
    def show_home(self):
        self.clear_window()
        role = self.user_role

        tk.Label(self.root, text=f"🎓 Welcome, {self.logged_in_user} ({role})", font=("Arial", 20, "bold"),
                 bg="#F0F4F8").pack(pady=30)

        if role == "Teacher":
            tk.Button(self.root, text="Create Quiz", font=("Arial", 14), width=25, bg="#4CAF50", fg="white",
                      command=self.show_create_quiz).pack(pady=15)
        elif role == "Student":
            tk.Button(self.root, text="Take Quiz", font=("Arial", 14), width=25, bg="#2196F3", fg="white",
                      command=self.show_take_quiz).pack(pady=15)

        tk.Button(self.root, text="Logout", font=("Arial", 12), width=15, bg="#F44336", fg="white",
                  command=self.show_login).pack(pady=30)

    # ---------- TEACHER MODE ----------
    def show_create_quiz(self):
        self.clear_window()

        tk.Label(self.root, text="🧑‍🏫 Create Quiz", font=("Arial", 22, "bold"), bg="#F0F4F8").pack(pady=10)

        frame = tk.Frame(self.root, bg="#F0F4F8")
        frame.pack(pady=10)

        tk.Label(frame, text="Question:", bg="#F0F4F8", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.q_entry = tk.Entry(frame, width=60)
        self.q_entry.grid(row=0, column=1, pady=5)

        self.opt_entries = []
        for i in range(4):
            tk.Label(frame, text=f"Option {i + 1}:", bg="#F0F4F8", font=("Arial", 12)).grid(row=i + 1, column=0, sticky="w")
            e = tk.Entry(frame, width=40)
            e.grid(row=i + 1, column=1, pady=3)
            self.opt_entries.append(e)

        tk.Label(frame, text="Correct Answer:", bg="#F0F4F8", font=("Arial", 12)).grid(row=5, column=0, sticky="w")
        self.ans_entry = tk.Entry(frame, width=30)
        self.ans_entry.grid(row=5, column=1, pady=5)

        tk.Button(self.root, text="Add Question", bg="#4CAF50", fg="white", font=("Arial", 12),
                  command=self.add_question).pack(pady=10)

        tk.Button(self.root, text="Back", bg="#9E9E9E", fg="white", font=("Arial", 12),
                  command=self.show_home).pack(side="bottom", pady=20)

    def add_question(self):
        question = self.q_entry.get().strip()
        options = [e.get().strip() for e in self.opt_entries]
        answer = self.ans_entry.get().strip()

        if not question or not all(options) or not answer:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        data = load_quiz_data()
        data.append({"question": question, "options": options, "answer": answer})
        save_quiz_data(data)

        for e in self.opt_entries:
            e.delete(0, tk.END)
        self.q_entry.delete(0, tk.END)
        self.ans_entry.delete(0, tk.END)

        messagebox.showinfo("Saved", "Question added successfully!")

    # ---------- STUDENT MODE ----------
    def show_take_quiz(self):
        data = load_quiz_data()
        if not data:
            messagebox.showerror("Error", "No quiz data found!")
            return

        self.clear_window()
        self.data = data
        self.current_q = 0
        self.score = 0
        self.answers = []

        self.q_label = tk.Label(self.root, text="", font=("Arial", 16, "bold"), wraplength=600, bg="#F0F4F8")
        self.q_label.pack(pady=40)

        self.var = tk.StringVar()
        self.opts = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.var, value="", font=("Arial", 12), bg="#F0F4F8")
            rb.pack(anchor="w", padx=180, pady=5)
            self.opts.append(rb)

        tk.Button(self.root, text="Next →", font=("Arial", 13), bg="#2196F3", fg="white",
                  command=self.next_question).pack(pady=30)

        tk.Button(self.root, text="Back", bg="#9E9E9E", fg="white", font=("Arial", 11),
                  command=self.show_home).pack(side="bottom", pady=15)

        self.display_question()

    def display_question(self):
        q_data = self.data[self.current_q]
        self.q_label.config(text=f"Q{self.current_q + 1}. {q_data['question']}")
        self.var.set(None)
        for i, opt in enumerate(q_data["options"]):
            self.opts[i].config(text=opt, value=opt)

    def next_question(self):
        if not self.var.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        selected = self.var.get()
        correct = self.data[self.current_q]["answer"]
        self.answers.append((self.data[self.current_q]["question"], selected, correct))

        if selected == correct:
            self.score += 1

        self.current_q += 1
        if self.current_q < len(self.data):
            self.display_question()
        else:
            self.show_result()

    # ---------- RESULT SCREEN ----------
    def show_result(self):
        self.clear_window()

        tk.Label(self.root, text=f"🏁 Quiz Completed!", font=("Arial", 24, "bold"), bg="#F0F4F8").pack(pady=10)
        tk.Label(self.root, text=f"Your Score: {self.score}/{len(self.data)}", font=("Arial", 16),
                 bg="#F0F4F8", fg="#4CAF50").pack(pady=5)

        # Scrollable result list
        outer_frame = tk.Frame(self.root, bg="#F0F4F8")
        outer_frame.pack(fill="both", expand=True, padx=20, pady=10)

        canvas = tk.Canvas(outer_frame, bg="#F0F4F8", highlightthickness=0)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F0F4F8")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, (q, selected, correct) in enumerate(self.answers, 1):
            color = "#4CAF50" if selected == correct else "#F44336"
            tk.Label(scroll_frame, text=f"{i}. {q}", font=("Arial", 12, "bold"), bg="#F0F4F8", wraplength=680).pack(anchor="w", pady=2)
            tk.Label(scroll_frame, text=f"Your Answer: {selected}", font=("Arial", 11),
                     bg="#F0F4F8", fg=color).pack(anchor="w", padx=20)
            tk.Label(scroll_frame, text=f"Correct Answer: {correct}", font=("Arial", 11),
                     bg="#F0F4F8", fg="#4CAF50").pack(anchor="w", padx=20, pady=(0, 5))
            tk.Label(scroll_frame, text="—" * 70, bg="#F0F4F8").pack(anchor="w")

        tk.Button(self.root, text="Back to Home", font=("Arial", 12), bg="#9E9E9E", fg="white",
                  command=self.show_home).pack(pady=20)

    # ---------- Utility ----------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------- MAIN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
