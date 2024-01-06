import tkinter as tk
from datetime import datetime
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import *
from tkinter import messagebox
import json


THEME_OPTIONS = ["cosmo", "flatly", "journal", "litera",
                 "lumen", "minty", "pulse", "sandstone",
                 "united", "yeti", "morph", "simplex",
                 "cerculean", "solar", "superhero",
                 "darkly", "cyborg", "vapor"]

PRIORITY_OPTIONS = ["Yüksek", "Orta", "Düşük"]

theme = "superhero"
tasklist = []

class App(ttk.Window):
    def __init__(self, master=None):
        super().__init__(master, themename=theme)
        self.title("To-Do List")
        self.geometry("980x670")
        self.resizable(False, False)
        self.buttons = ButtonFrame(self)
        self.treeview = TaskListView(self)
        self.mainloop()
    def guncelle(self):
        self.treeview.update()

class Button(ttk.Button):
    def __init__(self, parent, text, command, image_path = None, bootstyle=None):
        super().__init__(parent)
        if bootstyle != None:
            self.configure(text=text, command=command, bootstyle=bootstyle)
        if image_path != None:
            self.image = tk.PhotoImage(file=image_path)
            self.configure(image=self.image, compound=tk.LEFT)
        else:
            self.configure(text=text, command=command)
        self.pack(side=tk.LEFT, padx=2, pady=2)

class ButtonFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(pady=10)
        self.add_task_button = Button(self, text="Görev Ekle", image_path="icons/add-task-button.png", command=self.add, bootstyle="default")
        self.add_task_button.pack(side=tk.LEFT, padx=2)
        self.edit_task_button = Button(self, text="Görev Düzenle", image_path="icons/edit-task-button.png", command=self.edit, bootstyle="warning")
        self.edit_task_button.pack(side=tk.LEFT, padx=2)
        self.complete_task_button = Button(self, text="Görev Tamamla", image_path="icons/complete-task-button.png", command=self.complete, bootstyle="success")
        self.complete_task_button.pack(side=tk.LEFT, padx=2)
        self.delete_task_button = Button(self, text="Görev Sil", image_path="icons/delete-task-button.png", command=self.delete, bootstyle="danger")
        self.delete_task_button.pack(side=tk.LEFT, padx=2)
        self.sort_combobox = ttk.Combobox(self, values=["Başlık", "Bitiş Tarihi", "Öncelik", "Durum"], width=12)
        self.sort_combobox.pack(side=tk.LEFT, padx=2)
        self.sort_tasks_button = Button(self, text="Sırala", image_path="icons/sort-tasks-button.png", command=self.sort, bootstyle="info")
        self.sort_tasks_button.pack(side=tk.LEFT, padx=2)
        self.set_theme_combobox = ttk.Combobox(self, values=THEME_OPTIONS, width=12)
        self.set_theme_combobox.pack(side=tk.LEFT, padx=2)
        self.set_theme_button = Button(self, text="Tema Değiştir", image_path="icons/theme.png", command=self.set_theme, bootstyle="warning")
        self.set_theme_button.pack(side=tk.LEFT, padx=2)
    def set_theme(self) -> None:
        theme = self.set_theme_combobox.get()
        self.master.style.theme_use(theme)
    def add(self) -> None:
        window = AddTaskWindow(self.master)
    def complete(self) -> None:
        selected_item = self.master.treeview.treeview.selection()
        if not selected_item:
             messagebox.showinfo("Görev Tamamlama", "Lütfen tamamlanacak bir görev seçin.")
        else:
            selected_task_values = self.master.treeview.treeview.item(selected_item, 'values')
            title, description, deadline, priority, status = selected_task_values
        if status != "Tamamlandı":
            Task(title=title, description=description, deadline=deadline, priority=priority,status="Tamamlandı")
            index = self.master.treeview.treeview.index(selected_item)
            tasklist.pop(index)
            # Update the Treeview
            self.master.treeview.update()
        else:
             messagebox.showinfo("Görev Tamamlama", "Seçili görev zaten tamamlanmış.")
    def delete(self) -> None:
        selected_item = self.master.treeview.treeview.selection()
        if not selected_item:
            messagebox.showinfo("Görev Silme", "Lütfen silinecek bir görev seçin.")
        else:
            index = self.master.treeview.treeview.index(selected_item)
            tasklist.pop(index)
            self.master.treeview.update()
    def sort(self) -> None:
        selected_option = self.sort_combobox.get()
        if selected_option == "Durum":
            tasklist.sort(key=lambda task: task["status"] == "Tamamlandı")
            self.master.treeview.update()
        elif selected_option == "Bitiş Tarihi":
            tasklist.sort(key=lambda task: task["deadline"])
            self.master.treeview.update()
        elif selected_option == "Öncelik":
            tasklist.sort(key=lambda task: task["priority"], reverse=True)
            self.master.treeview.update()
        else:
            tasklist.sort(key=lambda task: task["title"])
            self.master.treeview.update()
    # Görev düzenleme ekranını açar
    def edit(self) -> None:
        selected_item = self.master.treeview.treeview.selection()

        if not selected_item:
            messagebox.showinfo("Görev Düzenleme", "Lütfen düzenlenecek bir görev seçin.")
        else:
            selected_task_values = self.master.treeview.treeview.item(selected_item, 'values')
            title, description, deadline, priority, status = selected_task_values
            index = self.master.treeview.treeview.index(selected_item)
            window = EditTaskWindow(self.master, title, description, deadline, priority, index)

# Görev sınıfını json'a dönüştürmek için
class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return obj.__dict__  # Convert Task object to a dictionary
        return super().default(obj)

# Görev sınıfı
class Task():
    def __init__(self, title, description, deadline, priority, status=None):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        if status == None:
            self.status = "Tamamlanmadı"
        else:
            self.status = "Tamamlandı"
        task = {"title":self. title, "description": self.description, "deadline": self.deadline, "priority": self.priority, "status": self.status}
        tasklist.append(task)
# Görev listesi Frame'i
class TaskListView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.Y)
        # Treeview
        self.treeview = ttk.Treeview(self,selectmode= "extended", columns=("Başlık","Açıklama", "Bitiş Tarihi", "Öncelik", "Durum"), show="headings",height=40)
        self.treeview_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.configure(yscrollcommand=self.treeview_scrollbar.set)
        # Sütunların ayarlanması
        self.treeview.heading("#1", text="Başlık")
        self.treeview.heading("#2", text="Açıklama")
        self.treeview.heading("#3", text="Bitiş Tarihi")
        self.treeview.heading("#4", text="Öncelik")
        self.treeview.heading("#5", text="Durum")
        self.treeview.column("#1", width=150, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#2", width=300, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#3", width=150, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#4", width=150, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("#5", width=150, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.pack(fill=tk.Y,padx=2, pady=2, expand=True)
        # Treeview'a json dosyasından veri ekleme
        self.load_tasks_from_json("tasklist.json")
        for task in tasklist:
            self.treeview.insert("", tk.END, values=(task["title"], task["description"], task["deadline"], task["priority"], task["status"]))
    def update(self):
        self.save_tasks_to_json("tasklist.json")
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.load_tasks_from_json("tasklist.json")
        for task in tasklist:
            self.treeview.insert("", tk.END, values=(task["title"], task["description"], task["deadline"], task["priority"], task["status"]))
    def save_tasks_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(tasklist, file, cls=TaskEncoder, indent=2)
        file.close()
    def load_tasks_from_json(self, filename):
        global tasklist
        try:
            with open(filename, 'r') as file:
                data = file.read()
                if data:
                    tasklist = json.loads(data)
                else:
                    tasklist = []
        except FileNotFoundError:
            tasklist = []

class AddTaskWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.title("Add Task")
        self.geometry("500x350")
        self.resizable(False, False)
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.title_label = ttk.Label(self.title_frame, text="Başlık", width=10)
        self.title_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.title_frame, width=50)
        self.title_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.description_frame = ttk.Frame(self)
        self.description_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.description_label = ttk.Label(self.description_frame, text="Açıklama", width=10)
        self.description_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.description_frame, width=50)
        self.description_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_frame = ttk.Frame(self)
        self.deadline_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.deadline_label = ttk.Label(self.deadline_frame, text="Bitiş Tarihi", width=10)
        self.deadline_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_entry = ttk.DateEntry(self.deadline_frame, dateformat="%d/%m/%Y")
        self.deadline_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_frame = ttk.Frame(self)
        self.priority_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.priority_label = ttk.Label(self.priority_frame, text="Öncelik", width=10)
        self.priority_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(self.priority_frame, values=PRIORITY_OPTIONS, width=50)
        self.priority_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.add_button = Button(self, text="Görev Ekle", image_path="icons/add-task-button.png", command=self.add, bootstyle="success")
        self.add_button.pack(side=tk.TOP, padx=10, pady=10)
        self.mainloop()
    def add(self):
        if self.title_entry.get() == "" or self.description_entry.get() == "" or self.deadline_entry.entry.get() == "" or self.priority_combobox.get() == "":
            messagebox.showinfo("Görev Ekleme", "Lütfen tüm alanları doldurun.")
            return
        else :
            title = self.title_entry.get()
            description = self.description_entry.get()
            deadline = self.deadline_entry.entry.get()
            priority = self.priority_combobox.get()
            # Görev oluştur
            task = Task(title=title, description=description, deadline=deadline, priority=priority)
            self.master.guncelle()
            self.destroy()

class EditTaskWindow(ttk.Toplevel):
    def __init__(self, parent, title, description, deadline, priority, index):
        super().__init__(master=parent)
        self.index = index
        self.title("Edit Task")
        self.geometry("500x350")
        self.resizable(False, False)
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.title_label = ttk.Label(self.title_frame, text="Başlık", width=10)
        self.title_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.title_frame, width=50)
        self.title_entry.insert(0, title)
        self.title_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.description_frame = ttk.Frame(self)
        self.description_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.description_label = ttk.Label(self.description_frame, text="Açıklama", width=10)
        self.description_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.description_frame, width=50)
        self.description_entry.insert(0, description)
        self.description_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_frame = ttk.Frame(self)
        self.deadline_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.deadline_label = ttk.Label(self.deadline_frame, text="Bitiş Tarihi", width=10)
        self.deadline_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.deadline_entry = ttk.DateEntry(self.deadline_frame, startdate=datetime.strptime(deadline, '%d/%m/%Y').date(), dateformat="%d/%m/%Y")
        self.deadline_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_frame = ttk.Frame(self)
        self.priority_frame.pack(fill=tk.BOTH, pady=5, padx=5)
        self.priority_label = ttk.Label(self.priority_frame, text="Öncelik", width=10)
        self.priority_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.priority_combobox = ttk.Combobox(self.priority_frame, values=PRIORITY_OPTIONS, width=50)
        self.priority_combobox.insert(0, priority)
        self.priority_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.edit_button = Button(self, text="Görev Düzenle", image_path="icons/edit-task-button.png", command=self.edit, bootstyle="warning")
        self.edit_button.pack(side=tk.TOP, padx=10, pady=10)
        self.mainloop()
    def edit(self):
        if self.title_entry.get() == "" or self.description_entry.get() == "" or self.deadline_entry.entry.get() == "" or self.priority_combobox.get() == "":
            messagebox.showinfo("Görev Ekleme", "Lütfen tüm alanları doldurun.")
            return
        else :
            title = self.title_entry.get()
            description = self.description_entry.get()
            deadline = self.deadline_entry.entry.get()
            priority = self.priority_combobox.get()
            # Görev oluştur
            task = Task(title=title, description=description, deadline=deadline, priority=priority)
            tasklist.pop(self.index)
            self.master.guncelle()
            self.destroy()

if __name__ == "__main__":
    app = App()