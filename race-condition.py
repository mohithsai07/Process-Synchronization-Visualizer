import tkinter as tk
from tkinter import ttk
from threading import Thread, Semaphore
import time
import random

class RaceConditionDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Race Condition Demo with Semaphore")
        self.root.geometry("600x400")

        self.shared_resource = 0
        self.semaphore = Semaphore()

        self.label = ttk.Label(root, text="Shared Resource: 0", font=("Arial", 14))
        self.label.pack(pady=10)

        # Create buttons for incrementing the shared resource
        self.increment_button = ttk.Button(root, text="Increment", command=self.increment_shared_resource)
        self.increment_button.pack(pady=5)

        # Create buttons for decrementing the shared resource
        self.decrement_button = ttk.Button(root, text="Decrement", command=self.decrement_shared_resource)
        self.decrement_button.pack(pady=5)

        # Create a table to display relative timings and sample processes
        columns = ("Relative Time", "Process ID", "Number of Processes", "Operation", "Result")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        self.process_counts = {"Increment": 0, "Decrement": 0}

    def increment_shared_resource(self):
        with self.semaphore:
            current_value = self.shared_resource
            time.sleep(1)
            self.shared_resource = current_value + 1
            self.update_label("Increment", current_value, "+1")

    def decrement_shared_resource(self):
        with self.semaphore:
            current_value = self.shared_resource
            time.sleep(1)
            self.shared_resource = current_value - 1
            self.update_label("Decrement", current_value, "-1")

    def update_label(self, operation, current_value, result):
        timestamp = time.strftime("%H:%M:%S")
        process_id = random.randint(1000, 9999)
        relative_time = time.time()  # Get relative time

        process_type = "Increment" if operation == "Increment" else "Decrement"
        self.process_counts[process_type] += 1
        num_processes = self.process_counts[process_type]

        self.tree.insert("", "end", values=(f"{timestamp}", f"{process_id}", num_processes, operation, result))
        self.tree.yview(tk.END)  # Automatically scroll to the bottom of the table
        self.label.config(text=f"Shared Resource: {self.shared_resource}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceConditionDemo(root)
    root.mainloop()
