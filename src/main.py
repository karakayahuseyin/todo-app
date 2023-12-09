import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import *

# TASK OPTIONS
PRIORITY_OPTIONS = ["Low", "Normal", "High"]
STATUS_OPTIONS = ["Not Started", "In Progress", "Done"]

class Root(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("To-Do App")
        self.geometry("1200x800")
        self.menu = MenuFrame(self)
        self.main = TaskList(self)
        self.buttons = ButtonFrame(self)
        self.mainloop()

tasklist = []
class MenuFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH)
        # Menu
        self.menu = ttk.Menu(self)
        self.file_menu = ttk.Menu(self.menu)
        self.file_menu.add_command(label="New", command=self.new)
        self.file_menu.add_command(label="Open", command=self.open)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.tasklist = tasklist
        # Bind menu to root
        parent.config(menu=self.menu)
    def new(self):
        #create a new tasklist jsonfile
        self.tasklist = []
    def open(self):
        pass
    def save(self):
        pass

class TaskList(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        # Treeview
        self.treeview = ttk.Treeview(self, columns=("Name","Description", "Deadline", "Priority", "Status"), show="headings",height=35)
        self.treeview.heading("#1", text="Name")
        self.treeview.heading("#2", text="Description")
        self.treeview.heading("#3", text="Deadline")
        self.treeview.heading("#4", text="Priority")
        self.treeview.heading("#5", text="Status")
        self.treeview.pack(padx=1, pady=1, expand=True)

class Task():
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.deadline = ""
        self.priority = PRIORITY_OPTIONS[0]
        self.status = STATUS_OPTIONS[0]
    def setName(self, name):
        self.name = name
    def setDescription(self, description):
        self.description = description
    def setDeadline(self, deadline):
        self.deadline = deadline
    def setPriority(self, priority):
        self.priority = priority
    def setStatus(self, status):
        self.status = status
    def getName(self):
        return self.name
    def getDescription(self):
        return self.description
    def getDeadline(self):
        return self.deadline
    def getPriority(self):
        return self.priority
    def getStatus(self):
        return self.status
    
class Button(ttk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent)
        self.configure(text=text, command=command)
class ButtonFrame(ttk.Frame):
    # Add Task
    # Edit Task
    # Delete Task
    # Sort Task
    # Filter Task
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.add_task = Button(self, text="Add Task", command=self.add_task)
        self.add_task.pack(side=tk.LEFT, padx=10)
        self.edit_task = Button(self, text="Edit Task", command=self.edit_task)
        self.edit_task.pack(side=tk.LEFT, padx=10)
        self.delete_task = Button(self, text="Delete Task", command=self.delete_task)
        self.delete_task.pack(side=tk.LEFT, padx=10)
        self.sort_task = Button(self, text="Sort Task", command=self.sort_task)
        self.sort_task.pack(side=tk.LEFT, padx=10)
        self.filter_task = Button(self, text="Filter Task", command=self.filter_task)
        self.filter_task.pack(side=tk.LEFT, padx=10)
    def add_task(self):
        AddTaskWindow(self)
    def edit_task(self):
        EditTaskWindow(self)
    def delete_task(self):
        pass
    def sort_task(self):
        pass
    def filter_task(self):
        pass

class AddTaskWindow(ttk.Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Task")
        self.geometry("500x250")
        self.name_frame = ttk.Frame(self)
        self.name_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.name_label = ttk.Label(self.name_frame, text="Name", width=10) 
        self.name_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.name_frame, width=50)
        self.name_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.description_frame = ttk.Frame(self)
        self.description_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.description_label = ttk.Label(self.description_frame, text="Description", width=10)
        self.description_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.description_frame, width=50)
        self.description_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_frame = ttk.Frame(self)
        self.deadline_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.deadline_label = ttk.Label(self.deadline_frame, text="Deadline", width=10)
        self.deadline_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_entry = ttk.Entry(self.deadline_frame, width=50)
        self.deadline_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_frame = ttk.Frame(self)
        self.priority_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.priority_label = ttk.Label(self.priority_frame, text="Priority", width=10)
        self.priority_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(self.priority_frame, values=PRIORITY_OPTIONS, width=50)
        self.priority_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.status_label = ttk.Label(self.status_frame, text="Status", width=10)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.status_combobox = ttk.Combobox(self.status_frame, values=STATUS_OPTIONS, width=50)
        self.status_combobox.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = ttk.Button(self, text="Add", command=self.add)
        self.add_button.pack(side=tk.TOP, padx=10, pady=10)
        self.mainloop()
    def add(self):
        pass

class EditTaskWindow():
    def __init__(self):
        pass

if __name__ == "__main__":
    Root()
