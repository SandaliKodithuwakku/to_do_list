import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.storage import TaskStorage
from src.gui_components import LoginWindow, TaskManagerWindow


class ToDoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List Management System")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'white': '#ffffff'
        }
        
        self.storage = TaskStorage()
        self.current_user = None
        
        # Show login
        self.show_login()
    
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow(self.root, self.on_login_success, self.colors)
    
    def on_login_success(self, username):
        """Called when user logs in"""
        self.current_user = username
        self.login_window.destroy()
        self.show_task_manager()
    
    def show_task_manager(self):
        """Show task manager"""
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.task_manager = TaskManagerWindow(
            self.root, 
            self.current_user, 
            self.storage, 
            self.colors,
            self.on_logout
        )
    
    def on_logout(self):
        """Handle logout"""
        self.task_manager.destroy()
        self.current_user = None
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.show_login()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()