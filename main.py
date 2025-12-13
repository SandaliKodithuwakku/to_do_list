import tkinter as tk
from tkinter import ttk

class ToDoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List Management System")
        self.root.geometry("400x500")
        
        # Title label
        title = tk.Label(
            self.root,
            text="To-Do List Manager",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=20)
        
        # Placeholder label
        label = tk.Label(
            self.root,
            text="Coming Soon...",
            font=("Helvetica", 12)
        )
        label.pack(pady=20)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()