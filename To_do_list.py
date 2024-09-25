import pickle
from datetime import datetime, timedelta

class Task:
    def __init__(self, title, description="", due_date=None, priority="light"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        due_str = f" (Due: {self.due_date.strftime('%Y-%m-%d %H:%M')})" if self.due_date else ""
        return f"{self.title} - {self.description} [Status: {status}] [Priority: {self.priority.capitalize()}]{due_str}"

class ToDoApp:
    def __init__(self):
        self.tasks = []
        self.streak = 0
        self.load_tasks()

    def add_task(self, title, description="", due_date=None, priority="light"):
        task = Task(title, description, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        if not self.tasks:
            print("\nNo tasks found!")
        # Sort tasks based on priority
        priority_order = {"serious": 1, "medium": 2, "light": 3}
        sorted_tasks = sorted(self.tasks, key=lambda t: priority_order[t.priority])
        for i, task in enumerate(sorted_tasks, 1):
            print(f"{i}. {task}")

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.streak += 1
            print(f"Streak: {self.streak} day(s)!")
            self.save_tasks()
        else:
            print("Invalid task number.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
        else:
            print("Invalid task number.")

    def save_tasks(self):
        with open('tasks.pkl', 'wb') as f:
            pickle.dump((self.tasks, self.streak), f)

    def load_tasks(self):
        try:
            with open('tasks.pkl', 'rb') as f:
                self.tasks, self.streak = pickle.load(f)
        except FileNotFoundError:
            self.tasks = []
            self.streak = 0

def main_menu():
    app = ToDoApp()
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Mark task as completed")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            due_date_input = input("Enter due date (YYYY-MM-DD HH:MM) or press enter for no due date: ")
            due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M") if due_date_input else None
            priority = input("Set task priority (serious/medium/light): ").lower()
            if priority not in ["serious", "medium", "light"]:
                print("Invalid priority! Setting to 'light'.")
                priority = "light"
            app.add_task(title, description, due_date, priority)
            print("Task added successfully!")

        elif choice == "2":
            app.list_tasks()

        elif choice == "3":
            app.list_tasks()
            index = int(input("Enter task number to mark as completed: ")) - 1
            app.mark_task_completed(index)

        elif choice == "4":
            app.list_tasks()
            index = int(input("Enter task number to delete: ")) - 1
            app.delete_task(index)
            print("Task deleted successfully!")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    main_menu()
