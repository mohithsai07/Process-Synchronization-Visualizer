import tkinter as tk
from tkinter import ttk
import threading
import time
from queue import Queue
import random

class ProducerConsumerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Producer-Consumer Simulator")
        self.root.geometry("800x400")
        self.root.configure(bg="#8B4513")  # Set background color to dark brown

        # Create variables for user input
        self.num_processes_var = tk.StringVar()

        # Set up GUI components
        ttk.Label(root, text="Number of Processes:").pack(pady=10)
        entry_num_processes = ttk.Entry(root, textvariable=self.num_processes_var)
        entry_num_processes.pack(pady=10)

        start_button = ttk.Button(root, text="Start", command=self.start_simulation)
        start_button.pack(pady=20)

        # Create a treeview for displaying process information
        self.tree = ttk.Treeview(root, columns=("Process", "Arrival Time", "Waiting Time", "Burst Time", "Producer", "Consumer", "Resource Type"),
                                  show="headings", selectmode="browse")
        self.tree.heading("Process", text="Process")
        self.tree.heading("Arrival Time", text="Arrival Time (s)")
        self.tree.heading("Waiting Time", text="Waiting Time (s)")
        self.tree.heading("Burst Time", text="Burst Time (s)")
        self.tree.heading("Producer", text="Producer")
        self.tree.heading("Consumer", text="Consumer")
        self.tree.heading("Resource Type", text="Resource Type")
        self.tree.column("Process", width=80, anchor="center")
        self.tree.column("Arrival Time", width=120, anchor="center")
        self.tree.column("Waiting Time", width=120, anchor="center")
        self.tree.column("Burst Time", width=120, anchor="center")
        self.tree.column("Producer", width=80, anchor="center")
        self.tree.column("Consumer", width=80, anchor="center")
        self.tree.column("Resource Type", width=120, anchor="center")
        self.tree.pack(pady=20)

        self.is_running = False
        self.queue = Queue()

    def start_simulation(self):
        num_processes = int(self.num_processes_var.get())

        if num_processes <= 0:
            tk.messagebox.showerror("Error", "Please enter a valid number of processes.")
            return

        if self.is_running:
            tk.messagebox.showinfo("Info", "Simulation is already running.")
            return

        self.is_running = True
        self.tree.delete(*self.tree.get_children())

        # Start the simulation in a separate thread
        threading.Thread(target=self.simulate_processes, args=(num_processes,), daemon=True).start()

    def simulate_processes(self, num_processes):
        for process_id in range(1, num_processes + 1):
            arrival_time = time.time()
            producer_id = random.randint(1, 5)
            consumer_id = random.randint(1, 5)
            resource_type = random.choice(["TypeA", "TypeB", "TypeC"])

            self.queue.put((process_id, arrival_time, producer_id, consumer_id, resource_type))

            # Simulate burst time (waiting time)
            time.sleep(1)

            waiting_time = time.time() - arrival_time

            # Update the GUI in the main thread
            self.root.after(0, self.update_treeview, process_id, arrival_time, waiting_time, producer_id, consumer_id, resource_type)

        self.is_running = False

    def update_treeview(self, process_id, arrival_time, waiting_time, producer_id, consumer_id, resource_type):
        self.tree.insert("", "end", values=(process_id, f"{arrival_time:.2f} s", f"{waiting_time:.2f} s", "Simulated Burst", producer_id, consumer_id, resource_type))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProducerConsumerSimulator(root)
    root.mainloop()
