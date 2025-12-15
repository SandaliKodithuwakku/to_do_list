import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.storage import TaskStorage
from src.gui_components import LoginWindow


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
        print(f"User logged in: {username}")
        # TODO: Show main window
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()