import tkinter as tk
from tkinter import ttk
import psutil
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ProcessMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Monitor")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0e68c") # Set background color to light brown

        # Increase font size
        custom_font = ("Arial", 14)

        self.label = ttk.Label(root, text="Real Time Process graph", foreground="#ff0000", font=custom_font, background="#f0e68c")
        self.label.place(x=280, y=320)

        self.label_processes = ttk.Label(root, text="Number of Processes: 0", font=custom_font, background="#f0e68c")
        self.label_processes.place(x=150, y=370)

        self.tree = ttk.Treeview(root, columns=("Arrival Time", "Closing Time"), show="headings", selectmode="browse")
        self.tree.heading("Arrival Time", text="Arrival Time")
        self.tree.heading("Closing Time", text="Closing Time")
        self.tree.column("Arrival Time", width=150)
        self.tree.column("Closing Time", width=150)
        self.tree.place(x=250, y=420)

        self.figure, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=10)
        self.canvas.draw()

        self.is_running = True
        self.thread = threading.Thread(target=self.update_data)
        self.thread.start()

        self.prev_num_processes = 0
        self.processes_data = []

    def update_data(self):
        x_data = [0]
        y_data = [0]

        while self.is_running:
            processes = psutil.process_iter()
            num_processes = 0
            for _ in processes:
                num_processes += 1

            x_data.append(x_data[-1] + 1)
            y_data.append(num_processes)

            if len(x_data) > 10:  # Limit data points for better visualization
                x_data = x_data[-10:]
                y_data = y_data[-10:]

            self.label_processes.config(text=f"Number of Processes: {num_processes}")

            # Check for a decrease in the number of processes
            if num_processes < self.prev_num_processes:
                reduction = self.prev_num_processes - num_processes
                reduction_text = f"({reduction} processes closed)"
                self.label_processes.config(text=f"Number of Processes: {num_processes} {reduction_text}")

            # Check for newly arrived processes
            if num_processes > self.prev_num_processes:
                for _ in range(num_processes - self.prev_num_processes):
                    arrival_time = datetime.now().strftime("%H:%M:%S")
                    self.processes_data.append((arrival_time, "-"))

            # Check for closed processes
            if num_processes < self.prev_num_processes:
                for _ in range(self.prev_num_processes - num_processes):
                    closing_time = datetime.now().strftime("%H:%M:%S")
                    self.processes_data[-1] = (self.processes_data[-1][0], closing_time)

            # Display up to 5 processes in the table
            for i, (arrival_time, closing_time) in enumerate(self.processes_data[-5:]):
                self.tree.insert("", i, values=(arrival_time, closing_time))

            self.prev_num_processes = num_processes

            self.ax.clear()
            self.ax.plot(x_data, y_data, marker='o')
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Number of Processes")
            self.canvas.draw()

            self.root.update()
            self.root.after(1000)  # Update every second

    def stop_monitoring(self):
        self.is_running = False
        self.thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    monitor = ProcessMonitor(root)
    root.protocol("WM_DELETE_WINDOW", monitor.stop_monitoring)
    root.mainloop()
