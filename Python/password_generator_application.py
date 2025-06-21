import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("400x300")
        self.root.configure(bg="#e6f7ff")  # Light blue calm background

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Password Length:", font=('Arial', 14), bg="#e6f7ff").pack(pady=10)
        self.length_entry = tk.Entry(self.root, font=('Arial', 14), justify="center")
        self.length_entry.pack(pady=5)

        self.include_upper = tk.IntVar()
        self.include_lower = tk.IntVar()
        self.include_digits = tk.IntVar()
        self.include_symbols = tk.IntVar()

        tk.Checkbutton(self.root, text="Include Uppercase Letters", variable=self.include_upper,
                       bg="#e6f7ff", font=('Arial', 12)).pack(anchor="w", padx=40)
        tk.Checkbutton(self.root, text="Include Lowercase Letters", variable=self.include_lower,
                       bg="#e6f7ff", font=('Arial', 12)).pack(anchor="w", padx=40)
        tk.Checkbutton(self.root, text="Include Digits", variable=self.include_digits,
                       bg="#e6f7ff", font=('Arial', 12)).pack(anchor="w", padx=40)
        tk.Checkbutton(self.root, text="Include Symbols", variable=self.include_symbols,
                       bg="#e6f7ff", font=('Arial', 12)).pack(anchor="w", padx=40)

        tk.Button(self.root, text="Generate Password", font=('Arial', 14), bg="#99ccff",
                  command=self.generate_password).pack(pady=10)

        self.output_label = tk.Label(self.root, text="", font=('Arial', 14, 'bold'), bg="#e6f7ff", fg="#003366")
        self.output_label.pack(pady=5)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length <= 0:
                raise ValueError

            char_pool = ""
            if self.include_upper.get():
                char_pool += string.ascii_uppercase
            if self.include_lower.get():
                char_pool += string.ascii_lowercase
            if self.include_digits.get():
                char_pool += string.digits
            if self.include_symbols.get():
                char_pool += string.punctuation

            if not char_pool:
                messagebox.showwarning("Warning", "Select at least one character type!")
                return

            password = ''.join(random.choices(char_pool, k=length))
            self.output_label.config(text=password)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for length.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
