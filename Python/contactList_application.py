import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONTACT_FILE = "contacts.json"

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f5f5")

        self.contacts = self.load_contacts()
        self.create_widgets()
        self.display_contacts()

    def create_widgets(self):
        entry_frame = tk.LabelFrame(self.root, text="Add / Update Contact", padx=10, pady=10, bg="#f0f5f5")
        entry_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(entry_frame, text="Name:", bg="#f0f5f5").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(entry_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Phone:", bg="#f0f5f5").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(entry_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Email:", bg="#f0f5f5").grid(row=0, column=2, padx=5, pady=5)
        self.email_entry = tk.Entry(entry_frame)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(entry_frame, text="Address:", bg="#f0f5f5").grid(row=1, column=2, padx=5, pady=5)
        self.address_entry = tk.Entry(entry_frame)
        self.address_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(entry_frame, text="Add Contact", bg="#c6f6c6", command=self.add_contact).grid(row=2, column=1, pady=10)
        tk.Button(entry_frame, text="Update Contact", bg="#f6f6c6", command=self.update_contact).grid(row=2, column=2, pady=10)

        search_frame = tk.Frame(self.root, bg="#f0f5f5")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:", bg="#f0f5f5").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_contact, bg="#d9eaff").pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.display_contacts, bg="#eeeeee").pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self.root, columns=('Name', 'Phone', 'Email', 'Address'), show='headings')
        for col in ('Name', 'Phone', 'Email', 'Address'):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10, fill='both', expand=True)
        self.tree.bind('<ButtonRelease-1>', self.select_contact)

        tk.Button(self.root, text="Delete Contact", command=self.delete_contact, bg="#f6c6c6").pack(pady=5)

    def load_contacts(self):
        if os.path.exists(CONTACT_FILE):
            with open(CONTACT_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_contacts(self):
        with open(CONTACT_FILE, 'w') as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if name and phone:
            self.contacts.append({'name': name, 'phone': phone, 'email': email, 'address': address})
            self.save_contacts()
            self.display_contacts()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Name and phone are required.")

    def display_contacts(self):
        self.tree.delete(*self.tree.get_children())
        for contact in self.contacts:
            self.tree.insert('', 'end', values=(contact['name'], contact['phone'], contact['email'], contact['address']))

    def search_contact(self):
        term = self.search_entry.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for contact in self.contacts:
            if term in contact['name'].lower() or term in contact['phone']:
                self.tree.insert('', 'end', values=(contact['name'], contact['phone'], contact['email'], contact['address']))

    def select_contact(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[0])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, values[3])

    def update_contact(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "No contact selected.")
            return

        updated_name = self.name_entry.get().strip()
        updated_phone = self.phone_entry.get().strip()
        updated_email = self.email_entry.get().strip()
        updated_address = self.address_entry.get().strip()

        if updated_name and updated_phone:
            index = self.tree.index(selected)
            self.contacts[index] = {
                'name': updated_name,
                'phone': updated_phone,
                'email': updated_email,
                'address': updated_address
            }
            self.save_contacts()
            self.display_contacts()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Name and phone are required.")

    def delete_contact(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "No contact selected.")
            return
        index = self.tree.index(selected)
        del self.contacts[index]
        self.save_contacts()
        self.display_contacts()
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
