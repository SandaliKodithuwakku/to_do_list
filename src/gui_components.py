import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow:
    def __init__(self, parent, on_success, colors):
        self.parent = parent
        self.on_success = on_success
        self.colors = colors
        
        # Clear parent window
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Create login UI
        self.create_login_ui()
    
    def create_login_ui(self):
        """Create the login interface"""
        # Main container
        main_frame = tk.Frame(self.parent, bg=self.colors['primary'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📝 To-Do List Manager",
            font=("Helvetica", 24, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=(50, 10))
        
        # Login card
        login_card = tk.Frame(main_frame, bg=self.colors['white'])
        login_card.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Welcome text
        welcome_label = tk.Label(
            login_card,
            text="Welcome!",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['white']
        )
        welcome_label.pack(pady=(30, 10))
        
        # Username entry
        entry_frame = tk.Frame(login_card, bg=self.colors['white'])
        entry_frame.pack(pady=10, padx=40, fill=tk.X)
        
        username_label = tk.Label(
            entry_frame,
            text="Username:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['white']
        )
        username_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = tk.Entry(entry_frame, font=("Helvetica", 12))
        self.username_entry.pack(fill=tk.X, ipady=8)
        self.username_entry.focus()
        self.username_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_button = tk.Button(
            login_card,
            text="Login",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            command=self.login
        )
        login_button.pack(pady=(30, 20), padx=40, fill=tk.X, ipady=10)
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        if username:
            if len(username) < 3:
                messagebox.showerror("Error", "Username must be at least 3 characters")
                return
            self.on_success(username)
        else:
            messagebox.showerror("Error", "Please enter a username")
    
    def destroy(self):
        """Clear the login window"""
        for widget in self.parent.winfo_children():
            widget.destroy()