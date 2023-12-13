import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from task import *
from tkcalendar import Calendar, DateEntry
from datetime import date
from config import *

class Application(ttk.Window):
    def __init__(self, config:Config):
        super().__init__(themename = config.getTheme())
        self.title("To-Do List")
        self.geometry("1000x750")
        self.resizable(True, True)
        self.menu = MenuFrame(self, config)
        self.buttons = ButtonFrame(self, config)
        self.treeview = TaskListView(self, config)
        self.mainloop()
    def refresh(self):
        self.treeview.update_data(tasklist)

class MenuFrame(ttk.Frame):
    def __init__(self, parent, config:Config):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, padx=5, pady=5)
        # Menu
        self.menu = ttk.Menu(self)
        self.file_menu = ttk.Menu(self.menu)
        self.file_menu.add_command(label="New", font=config.getFont(), command=self.new)
        self.file_menu.add_command(label="Open", font=config.getFont(), command=self.open)
        self.file_menu.add_command(label="Save", font=config.getFont(), command=self.save)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Preferences", font=config.getFont(), command=self.preferences)
        self.file_menu.add_command(label="Exit", font=config.getFont(), command=self.quit)
        self.menu.add_cascade(label="Menu", menu=self.file_menu)
        # Bind menu to root
        parent.config(menu=self.menu)
    def new(self):
        pass
    def open(self):
        pass
    def save(self):
        pass
    def preferences(self):
        PreferencesWindow()

class TaskListView(ttk.Frame):
    def __init__(self, parent, config:Config):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        # Treeview
        self.treeview = ttk.Treeview(self,selectmode= "extended", columns=("Name","Description", "Deadline", "Priority", "Status"), show="headings",height=35)
        # TREEVIEW STYLES
        # Treeview scrollbar
        self.treeview_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar.set)
        # Columns heading
        self.treeview.heading("#1", text="Name")
        self.treeview.heading("#2", text="Description")
        self.treeview.heading("#3", text="Deadline")
        self.treeview.heading("#4", text="Priority")
        self.treeview.heading("#5", text="Status")
        # Columns config
        self.treeview.column("#1", width=200, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#2", width=400, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#3", width=100, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#4", width=100, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#5", width=100, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.pack(padx=1, pady=1, expand=True)
        # Row selection
    # Add data to treeview
    def update_data(self, tasklist):
        self.treeview.delete(*self.treeview.get_children())
        for task in tasklist:
            self.treeview.insert("", tk.END, values=(task.getName(), task.getDescription(), task.getDeadline(), task.getPriority(), task.getStatus()))

class Button(ttk.Button):
    def __init__(self, parent, config:Config, text, command, image_path = None, style = "default.TButton"):
        super().__init__(parent)
        if style != None:
            self.configure(text=text, command=command, style=style)
        if image_path != None:
            self.image = tk.PhotoImage(file=image_path)
            self.configure(image=self.image, compound=tk.LEFT)
        self.pack(side=tk.LEFT, padx=10, pady=10)

class ButtonFrame(ttk.Frame):
    def __init__(self, parent, config:Config):
        super().__init__(parent)
        self.config = config
        self.pack(pady=5)
        self.add_task = Button(self, text=" Add Task", config=config, image_path="icons/add-task-button.png", command=self.add)
        self.add_task.pack(side=tk.LEFT, padx=10)
        self.sort_tasks = Button(self, text="Sort Tasks", config=config, image_path="icons/sort-tasks-button.png", command=self.sort)
        self.sort_tasks.pack(side=tk.LEFT, padx=10)
        self.filter_task = Button(self, text="Filter Tasks", config=config, image_path="icons/filter-tasks-button.png", command=self.filter)
        self.filter_task.pack(side=tk.LEFT, padx=10)
    def add(self) -> None:
        AddTaskWindow(self, config=self.config)
    def sort(self) -> None:
        pass
    def filter(self) -> None:
        pass

class AddTaskWindow(ttk.Window):
    def __init__(self, parent, config:Config):
        super().__init__(parent, themename=config.getTheme())
        self.title("Add Task")
        self.geometry("500x250")
        self.resizable(False, False)
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
        self.cal = Calendar(self, selectmode="day", year=date.today().year, month=date.today().month, day=date.today().day)
        self.deadline_frame = ttk.Frame(self)
        self.deadline_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.deadline_label = ttk.Label(self.deadline_frame, text="Deadline", width=10)
        self.deadline_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_entry = Entry(self.deadline_frame, width=50)
        self.deadline_entry.insert(0, "dd/mm/yyyy")
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
        name = self.name_entry.get()
        print(self.name_entry.get())
        description = self.description_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_combobox.get()
        status = self.status_combobox.get()
        task = Task(name)
        task.setDescription(description)
        task.setDeadline(deadline)
        task.setPriority(priority)
        task.setStatus(status)
        tasklist.append(task)
        # update Tasklist treeview
        self.parent.main.update_data()
        self.destroy()


class PreferencesWindow(ttk.Window):
    def __init__(self):
        super().__init__(self, themename="darkly")
        self.title("Preferences")
        self.geometry("500x250")
        self.resizable(False, False)
        self.theme_frame = ttk.Frame(self)
        self.theme_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.theme_label = ttk.Label(self.theme_frame, text="Theme", width=10)
        self.theme_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.theme_combobox = ttk.Combobox(self.theme_frame, values=THEME_OPTIONS, width=50)
        self.theme_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.font_frame = ttk.Frame(self)
        self.font_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.font_label = ttk.Label(self.font_frame, text="Font", width=10)
        self.font_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.font_combobox = ttk.Combobox(self.font_frame, values=FONT_OPTIONS, width=50)
        self.font_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.font_size_frame = ttk.Frame(self)
        self.font_size_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.font_size_label = ttk.Label(self.font_size_frame, text="Font Size", width=10)
        self.font_size_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.font_size_combobox = ttk.Combobox(self.font_size_frame, values=FONT_SIZE_OPTIONS, width=50)
        self.font_size_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.mainloop()
    def save(self):
            theme = self.theme_combobox.get()
            font = self.font_combobox.get()
            font_size = self.font_size_combobox.get()
            config = Config(theme, font, font_size)
            config.save()
            self.destroy()