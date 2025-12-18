import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
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
    Complete CRUD operations + Mark as Completed
    """
    def __init__(self, parent, username, storage, colors, on_logout):
        self.parent = parent
        self.username = username
        self.storage = storage
        self.colors = colors
        self.on_logout = on_logout
        self.tasks = []
        self.filtered_tasks = []
        self.current_filter = "All"
        self.selected_task_index = None
        
        # Load tasks
        self.load_tasks()
        
        # Create UI
        self.create_ui()
        
        # Display tasks
        self.refresh_task_list()
    
    def create_ui(self):
        """Create the UI"""
        # Main container
        main_frame = tk.Frame(self.parent, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Task Form
        self.create_task_form(content_frame)
        
        # Right panel - Task List
        self.create_task_list(content_frame)
        
        # Bottom - Statistics
        self.create_statistics(main_frame)
    
    def create_header(self, parent):
        """Create header"""
        header = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # User info
        user_frame = tk.Frame(header, bg=self.colors['primary'])
        user_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        greeting = tk.Label(
            user_frame,
            text=f"Welcome, {self.username}! 👋",
            font=("Helvetica", 16, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        greeting.pack(anchor=tk.W)
        
        date_label = tk.Label(
            user_frame,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            font=("Helvetica", 10),
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        date_label.pack(anchor=tk.W)
        
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
    
    def create_task_form(self, parent):
        """Create task input form"""
        form_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, borderwidth=1)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        form_frame.config(width=300)
        
        # Form title
        title = tk.Label(
            form_frame,
            text="✏️ Task Details",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['dark']
        )
        title.pack(pady=(15, 20), padx=15, anchor=tk.W)
        
        # Task Name
        tk.Label(
            form_frame, 
            text="Task Name:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=15, pady=(5, 2))
        
        self.task_name_entry = tk.Entry(form_frame, font=("Helvetica", 10), relief=tk.SOLID, borderwidth=1)
        self.task_name_entry.pack(fill=tk.X, padx=15, pady=(0, 10), ipady=5)
        
        # Priority
        tk.Label(
            form_frame, 
            text="Priority:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=15, pady=(5, 2))
        
        self.priority_var = tk.StringVar(value="Low")
        priority_frame = tk.Frame(form_frame, bg=self.colors['white'])
        priority_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
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
        
        # Due Date
        tk.Label(
            form_frame, 
            text="Due Date:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=15, pady=(5, 2))
        
        self.due_date_entry = DateEntry(
            form_frame,
            font=("Helvetica", 10),
            borderwidth=1,
            date_pattern='yyyy-mm-dd',
            mindate=datetime.now()
        )
        self.due_date_entry.pack(fill=tk.X, padx=15, pady=(0, 10), ipady=5)
        
        # Category
        tk.Label(
            form_frame, 
            text="Category:", 
            font=("Helvetica", 10, "bold"),
            bg=self.colors['white']
        ).pack(anchor=tk.W, padx=15, pady=(5, 2))
        
        self.category_var = tk.StringVar(value="Personal")
        category_combo = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=["Personal", "Work", "Study", "Health", "Shopping", "Other"],
            state="readonly",
            font=("Helvetica", 10)
        )
        category_combo.pack(fill=tk.X, padx=15, pady=(0, 20), ipady=5)
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.colors['white'])
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Add button
        add_btn = tk.Button(
            button_frame,
            text="➕ Add Task",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['success'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_task
        )
        add_btn.pack(fill=tk.X, pady=(0, 5), ipady=8)
        
        # Update button
        update_btn = tk.Button(
            button_frame,
            text="💾 Update Task",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['warning'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.update_task
        )
        update_btn.pack(fill=tk.X, pady=(0, 5), ipady=8)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🔄 Clear Form",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['dark'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_form
        )
        clear_btn.pack(fill=tk.X, ipady=8)
    
    def create_task_list(self, parent):
        """Create task list panel"""
        list_frame = tk.Frame(parent, bg=self.colors['white'], relief=tk.RAISED, borderwidth=1)
        list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Header with filters
        header_frame = tk.Frame(list_frame, bg=self.colors['white'])
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            header_frame,
            text="📋 My Tasks",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['white'],
            fg=self.colors['dark']
        ).pack(side=tk.LEFT)
        
        # Filter buttons
        filter_frame = tk.Frame(header_frame, bg=self.colors['white'])
        filter_frame.pack(side=tk.RIGHT)
        
        filters = ["All", "Pending", "Completed"]
        for filter_name in filters:
            btn = tk.Button(
                filter_frame,
                text=filter_name,
                font=("Helvetica", 9),
                bg=self.colors['light'] if filter_name != "All" else self.colors['secondary'],
                fg=self.colors['dark'] if filter_name != "All" else self.colors['white'],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda f=filter_name: self.apply_filter(f)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Treeview for tasks
        tree_frame = tk.Frame(list_frame, bg=self.colors['white'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.task_tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Priority", "Due Date", "Category", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )
        
        scrollbar.config(command=self.task_tree.yview)
        
        # Define columns
        self.task_tree.heading("Name", text="Task Name")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Due Date", text="Due Date")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Status", text="Status")
        
        self.task_tree.column("Name", width=200)
        self.task_tree.column("Priority", width=80)
        self.task_tree.column("Due Date", width=100)
        self.task_tree.column("Category", width=100)
        self.task_tree.column("Status", width=100)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure row colors
        self.task_tree.tag_configure('completed', background='#d5f4e6')
        self.task_tree.tag_configure('pending', background='#ffffff')
        self.task_tree.tag_configure('high', foreground='#e74c3c')
        self.task_tree.tag_configure('medium', foreground='#f39c12')
        
        # Bind selection event
        self.task_tree.bind('<<TreeviewSelect>>', self.on_task_select)
        
        # Action buttons
        action_frame = tk.Frame(list_frame, bg=self.colors['white'])
        action_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Mark Complete button
        complete_btn = tk.Button(
            action_frame,
            text="✓ Mark Complete",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['success'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.mark_complete
        )
        complete_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=8, ipadx=10)
        
        # Delete button
        delete_btn = tk.Button(
            action_frame,
            text="🗑️ Delete Task",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['danger'],
            fg=self.colors['white'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.delete_task
        )
        delete_btn.pack(side=tk.LEFT, padx=5, ipady=8, ipadx=10)
    
    def create_statistics(self, parent):
        """Create statistics panel"""
        stats_frame = tk.Frame(parent, bg=self.colors['dark'], height=60)
        stats_frame.pack(fill=tk.X, side=tk.BOTTOM)
        stats_frame.pack_propagate(False)
        
        self.total_label = tk.Label(
            stats_frame,
            text="Total: 0",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark'],
            fg=self.colors['white']
        )
        self.total_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.pending_label = tk.Label(
            stats_frame,
            text="Pending: 0",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark'],
            fg=self.colors['warning']
        )
        self.pending_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.completed_label = tk.Label(
            stats_frame,
            text="Completed: 0",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['dark'],
            fg=self.colors['success']
        )
        self.completed_label.pack(side=tk.LEFT, padx=20, pady=15)
    
    def load_tasks(self):
        """Load tasks from storage"""
        task_dicts = self.storage.load_tasks(self.username)
        self.tasks = [Task.from_dict(task_dict) for task_dict in task_dicts]
        self.filtered_tasks = self.tasks.copy()
    
    def save_tasks(self):
        """Save tasks to storage"""
        task_dicts = [task.to_dict() for task in self.tasks]
        self.storage.save_tasks(self.username, task_dicts)
    
    def add_task(self):
        """Add a new task"""
        try:
            name = self.task_name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a task name")
                return
            
            priority = self.priority_var.get()
            due_date = str(self.due_date_entry.get_date())
            category = self.category_var.get()
            
            task = Task(name, priority, due_date, category)
            self.tasks.append(task)
            self.save_tasks()
            self.apply_filter(self.current_filter)
            self.clear_form()
            messagebox.showinfo("Success", "Task added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {str(e)}")
    
    def update_task(self):
        """Update selected task"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to update")
            return
        
        name = self.task_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a task name")
            return
        
        try:
            # Get selected task index
            item = selection[0]
            index = self.task_tree.index(item)
            
            # Find task in filtered list
            task = self.filtered_tasks[index]
            
            # Update task properties
            task.name = name
            task.priority = self.priority_var.get()
            task.due_date = str(self.due_date_entry.get_date())
            task.category = self.category_var.get()
            
            self.save_tasks()
            self.refresh_task_list()
            self.clear_form()
            messagebox.showinfo("Success", "Task updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update task: {str(e)}")
    
    def delete_task(self):
        """Delete selected task"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to delete")
            return
        
        # Confirmation dialog
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            try:
                item = selection[0]
                index = self.task_tree.index(item)
                task = self.filtered_tasks[index]
                
                # Remove from main task list
                self.tasks.remove(task)
                self.save_tasks()
                self.apply_filter(self.current_filter)
                self.clear_form()
                messagebox.showinfo("Success", "Task deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {str(e)}")
    
    def mark_complete(self):
        """Mark selected task as completed (NEW for Day 8!)"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to mark as complete")
            return
        
        try:
            item = selection[0]
            index = self.task_tree.index(item)
            task = self.filtered_tasks[index]
            
            # Check if already completed
            if task.status == "Completed":
                messagebox.showinfo("Info", "Task is already marked as completed")
                return
            
            # Update status to Completed
            task.status = "Completed"
            
            # Save to JSON
            self.save_tasks()
            
            # Refresh display
            self.refresh_task_list()
            
            messagebox.showinfo("Success", "Task marked as completed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark task as complete: {str(e)}")
    
    def on_task_select(self, event):
        """Handle task selection"""
        selection = self.task_tree.selection()
        if selection:
            item = selection[0]
            index = self.task_tree.index(item)
            task = self.filtered_tasks[index]
            
            # Populate form with selected task data
            self.task_name_entry.delete(0, tk.END)
            self.task_name_entry.insert(0, task.name)
            self.priority_var.set(task.priority)
            self.category_var.set(task.category)
            
            if task.due_date:
                try:
                    date_obj = datetime.strptime(task.due_date, '%Y-%m-%d')
                    self.due_date_entry.set_date(date_obj)
                except:
                    pass
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear tree
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Add filtered tasks
        for task in self.filtered_tasks:
            tags = []
            
            # Status tag
            if task.status == "Completed":
                tags.append('completed')
            else:
                tags.append('pending')
            
            # Priority tags
            if task.priority == "High":
                tags.append('high')
            elif task.priority == "Medium":
                tags.append('medium')
            
            self.task_tree.insert(
                "",
                tk.END,
                values=(task.name, task.priority, task.due_date, task.category, task.status),
                tags=tags
            )
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update statistics display"""
        total = len(self.tasks)
        pending = sum(1 for task in self.tasks if task.status == "Pending")
        completed = sum(1 for task in self.tasks if task.status == "Completed")
        
        self.total_label.config(text=f"Total: {total}")
        self.pending_label.config(text=f"Pending: {pending}")
        self.completed_label.config(text=f"Completed: {completed}")
    
    def apply_filter(self, filter_name):
        """Apply filter to task list"""
        self.current_filter = filter_name
        
        if filter_name == "All":
            self.filtered_tasks = self.tasks.copy()
        elif filter_name == "Pending":
            self.filtered_tasks = [task for task in self.tasks if task.status == "Pending"]
        elif filter_name == "Completed":
            self.filtered_tasks = [task for task in self.tasks if task.status == "Completed"]
        
        self.refresh_task_list()
    
    def clear_form(self):
        """Clear the form"""
        self.task_name_entry.delete(0, tk.END)
        self.priority_var.set("Low")
        self.category_var.set("Personal")
        self.due_date_entry.set_date(datetime.now())
    
    def destroy(self):
        """Destroy the task manager window"""
        for widget in self.parent.winfo_children():
            widget.destroy()