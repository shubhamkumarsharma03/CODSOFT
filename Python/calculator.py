import tkinter as tk
from tkinter import messagebox

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Serene Calculator")
        self.root.geometry("400x500")
        self.root.configure(bg="#e6ffe6")  # Light green background

        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self.root, font=('Arial', 24), bd=10, relief=tk.RIDGE, justify='right')
        self.display.pack(fill='x', padx=10, pady=20)

        button_frame = tk.Frame(self.root, bg="#e6ffe6")
        button_frame.pack()

        buttons = [
            ('7', '#ccffcc'), ('8', '#ccffcc'), ('9', '#ccffcc'), ('/', '#a3c2c2'),
            ('4', '#ccffcc'), ('5', '#ccffcc'), ('6', '#ccffcc'), ('*', '#a3c2c2'),
            ('1', '#ccffcc'), ('2', '#ccffcc'), ('3', '#ccffcc'), ('-', '#a3c2c2'),
            ('0', '#ccffcc'), ('.', '#ccffcc'), ('=', '#99ccff'), ('+', '#a3c2c2'),
            ('C', '#ffcccc')
        ]

        row = 0
        col = 0
        for (text, color) in buttons:
            button = tk.Button(button_frame, text=text, width=8, height=3, font=('Arial', 14),
                               bg=color, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_button_click(self, char):
        if char == 'C':
            self.display.delete(0, tk.END)
        elif char == '=':
            try:
                expression = self.display.get()
                result = eval(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
        else:
            self.display.insert(tk.END, char)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()
