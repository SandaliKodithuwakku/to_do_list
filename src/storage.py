import json
import os
from datetime import datetime

class Task:
    """Task class to represent a single task"""
    def __init__(self, name, priority="Low", due_date="", category="Personal", 
                 status="Pending", task_id=None, created_at=None):
        self.id = task_id if task_id else self._generate_id()
        self.name = name
        self.priority = priority
        self.due_date = str(due_date) if due_date else ""
        self.category = category
        self.status = status
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _generate_id(self):
        """Generate a unique task ID"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'priority': self.priority,
            'due_date': self.due_date,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create task from dictionary"""
        return Task(
            name=data.get('name', ''),
            priority=data.get('priority', 'Low'),
            due_date=data.get('due_date', ''),
            category=data.get('category', 'Personal'),
            status=data.get('status', 'Pending'),
            task_id=data.get('id'),
            created_at=data.get('created_at')
        )


class TaskStorage:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def get_user_file(self, username):
        """Get the file path for a specific user's tasks"""
        return os.path.join(self.data_dir, f"{username}_tasks.json")
    
    def load_tasks(self, username):
        """Load tasks for a specific user"""
        file_path = self.get_user_file(username)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading tasks: {e}")
                return []
        return []
    
    def save_tasks(self, username, tasks):
        """Save tasks for a specific user"""
        file_path = self.get_user_file(username)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False