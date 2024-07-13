import tkinter as tk
from tkinter import messagebox
import subprocess

def collect_data():
    try:
        subprocess.run(['python', 'scripts/collect_memory_data.py'], check=True)
        messagebox.showinfo("Success", "Data collection complete.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Data collection failed: {e}")

def analyze_data():
    try:
        subprocess.run(['python', 'scripts/analyze_memory_data.py'], check=True)
        messagebox.showinfo("Success", "Data analysis complete.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Data analysis failed: {e}")

def optimize_memory():
    try:
        subprocess.run(['python', 'scripts/optimize_memory.py'], check=True)
        messagebox.showinfo("Success", "Memory optimization complete.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Memory optimization failed: {e}")

def create_ui():
    root = tk.Tk()
    root.title("Memory Utilization Tool")

    collect_button = tk.Button(root, text="Collect Data", command=collect_data)
    collect_button.pack(pady=10)

    analyze_button = tk.Button(root, text="Analyze Data", command=analyze_data)
    analyze_button.pack(pady=10)

    optimize_button = tk.Button(root, text="Optimize Memory", command=optimize_memory)
    optimize_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_ui()
