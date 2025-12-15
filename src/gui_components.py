import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from storage import Task


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
        
        subtitle_label = tk.Label(
            main_frame,
            text="Organize your tasks efficiently",
            font=("Helvetica", 12),
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Login card
        login_card = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, borderwidth=2)
        login_card.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # Welcome text
        welcome_label = tk.Label(
            login_card,
            text="Welcome Back!",
            font=("Helvetica", 18, "bold"),
            bg=self.colors['white'],
            fg=self.colors['dark']
        )
        welcome_label.pack(pady=(30, 10))
        
        info_label = tk.Label(
            login_card,
            text="Enter your username to continue",
            font=("Helvetica", 10),
            bg=self.colors['white'],
            fg=self.colors['dark']
        )
        info_label.pack(pady=(0, 30))
        
        # Username entry
        entry_frame = tk.Frame(login_card, bg=self.colors['white'])
        entry_frame.pack(pady=10, padx=40, fill=tk.X)
        
        username_label = tk.Label(
            entry_frame,
            text="Username:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['white'],
            fg=self.colors['dark']
        )
        username_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = tk.Entry(
            entry_frame,
            font=("Helvetica", 12),
            relief=tk.SOLID,
            borderwidth=1
        )
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
            activebackground=self.colors['primary'],
            activeforeground=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.login
        )
        login_button.pack(pady=(30, 20), padx=40, fill=tk.X, ipady=10)
        
        # Footer
        footer_label = tk.Label(
            login_card,
            text="New user? Just enter a username to create an account",
            font=("Helvetica", 9),
            bg=self.colors['white'],
            fg=self.colors['dark']
        )
        footer_label.pack(pady=(0, 20))
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        if username:
            if len(username) < 3:
                messagebox.showerror("Error", "Username must be at least 3 characters long")
                return
            self.on_success(username)
        else:
            messagebox.showerror("Error", "Please enter a username")
    
    def destroy(self):
        """Clear the login window"""
        for widget in self.parent.winfo_children():
            widget.destroy()


class TaskManagerWindow:
    """
    Day 5: Basic Task Manager with Category Support
    """
    def __init__(self, parent, username, storage, colors, on_logout):
        self.parent = parent
        self.username = username
        self.storage = storage
        self.colors = colors
        self.on_logout = on_logout
        self.tasks = []
        
        # Load tasks
        self.load_tasks()
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the basic UI with categories"""
        main_frame = tk.Frame(self.parent, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        
        # User info
        user_label = tk.Label(
            header,
            text=f"Welcome, {self.username}! 👋",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        user_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Logout button
        logout_btn = tk.Button(
            header,
            text="Logout",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['danger'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.on_logout
        )
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Task form with categories
        form_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, borderwidth=1)
        form_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(
            form_frame, 
            text="✏️ Add New Task", 
            font=("Helvetica", 14, "bold"),
            bg=self.colors['white']
        ).pack(pady=10)
        
        # Task Name
        tk.Label(
            form_frame, 
            text="Task Name:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        self.task_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        self.task_entry.pack(fill=tk.X, padx=20, pady=(0, 10), ipady=5)
        
        # Category (NEW for Day 5!)
        tk.Label(
            form_frame, 
            text="Category:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        self.category_var = tk.StringVar(value="Personal")
        category_combo = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=["Personal", "Work", "Study", "Health", "Shopping", "Other"],
            state="readonly",
            font=("Helvetica", 10)
        )
        category_combo.pack(fill=tk.X, padx=20, pady=(0, 10), ipady=5)
        
        # Priority
        tk.Label(
            form_frame, 
            text="Priority:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=20, pady=(5, 2))
        
        self.priority_var = tk.StringVar(value="Low")
        priority_frame = tk.Frame(form_frame, bg=self.colors['white'])
        priority_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        for priority in ["Low", "Medium", "High"]:
            rb = tk.Radiobutton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                bg=self.colors['white'],
                font=("Helvetica", 9)
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_btn = tk.Button(
            form_frame,
            text="➕ Add Task",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['success'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task
        )
        add_btn.pack(pady=15, padx=20, fill=tk.X, ipady=8)
        
        # Task list
        list_frame = tk.Frame(main_frame, bg=self.colors['white'], relief=tk.RAISED, borderwidth=1)
        list_frame.pack(pady=(0, 20), padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            list_frame,
            text="📋 My Tasks",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['white']
        ).pack(pady=10)
        
        # Listbox to show tasks
        self.task_listbox = tk.Listbox(
            list_frame, 
            height=10,
            font=("Helvetica", 10)
        )
        self.task_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.task_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Refresh the list
        self.refresh_list()
    
    def load_tasks(self):
        """Load tasks"""
        task_dicts = self.storage.load_tasks(self.username)
        self.tasks = [Task.from_dict(td) for td in task_dicts]
    
    def save_tasks(self):
        """Save tasks"""
        task_dicts = [t.to_dict() for t in self.tasks]
        self.storage.save_tasks(self.username, task_dicts)
    
    def add_task(self):
        """Add a task with category"""
        name = self.task_entry.get().strip()
        if name:
            category = self.category_var.get()
            priority = self.priority_var.get()
            
            task = Task(name=name, priority=priority, category=category)
            self.tasks.append(task)
            self.save_tasks()
            self.refresh_list()
            self.task_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Task added to {category}!")
        else:
            messagebox.showerror("Error", "Please enter a task name")
    
    def refresh_list(self):
        """Refresh task list"""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = f"{task.name} | {task.category} | {task.priority} | {task.status}"
            self.task_listbox.insert(tk.END, display_text)
    
    def destroy(self):
        """Destroy window"""
        for widget in self.parent.winfo_children():
            widget.destroy()