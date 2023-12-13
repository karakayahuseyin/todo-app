import json
PRIORITY_OPTIONS = ["Low", "Normal", "High"]
STATUS_OPTIONS = ["Not Started", "In Progress", "Done"]

class Task():
    def __init__(self, name) -> None:
        self.name = name
        self.description = ""
        self.deadline = ""
        self.priority = PRIORITY_OPTIONS[0]
        self.status = STATUS_OPTIONS[0]
    def __str__(self) -> str:
        return f"Name: {self.name}\nDescription: {self.description}\nDeadline: {self.deadline}\nPriority: {self.priority}\nStatus: {self.status}"
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

tasklist = []

class Tasklist():
    # create a blank list
    def __init__(self) -> None:
        self.list = []
    # create a list from json file
    def Tasklist(self, jsonfile) -> None:
        self.list = []
        with open(jsonfile) as f:
            data = json.load(f)
            for task in data:
                name = task["name"]
                description = task["description"]
                deadline = task["deadline"]
                priority = task["priority"]
                status = task["status"]
                task = Task(name)
                task.setDescription(description)
                task.setDeadline(deadline)
                task.setPriority(priority)
                task.setStatus(status)
                self.list.append(task)
    # add a task to the list
    def add(self, task):
        task_dict = {
            "name": task.getName(),
            "description": task.getDescription(),
            "deadline": task.getDeadline(),
            "priority": task.getPriority(),
            "status": task.getStatus()
        }
        self.list.append(task_dict)
    # remove a task from the list
    def remove(self, task):
        self.list.remove(task)
    # save the list to json file
    def save(self, jsonfile):
        with open(jsonfile, "w") as f:
            json.dump(self.list, f)
    # return the list
    def getList(self):
        return self.list
    # return a task
    def getTask(self, index):
        return "name: " + self.list[index]["name"] + "\ndescription: " + self.list[index]["description"] + "\ndeadline: " + self.list[index]["deadline"] + "\npriority: " + self.list[index]["priority"] + "\nstatus: " + self.list[index]["status"]
    # return the length of the list
    def getLength(self):
        return len(self.list)
    

