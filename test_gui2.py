#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Hide the root window
root = tk.Tk()
root.withdraw()

# Show exactly where the app is running from
current_dir = os.getcwd()
script_dir = os.path.dirname(os.path.abspath(__file__))
sys_argv = sys.argv[0] if sys.argv else "Unknown"

messagebox.showinfo("Directory Info", 
    f"Current working directory:\n{current_dir}\n\n"
    f"Script directory:\n{script_dir}\n\n"
    f"sys.argv[0]:\n{sys_argv}")

# List files in current directory
try:
    files = os.listdir(current_dir)
    messagebox.showinfo("Files in Current Dir", f"Files found:\n" + "\n".join(files[:10]))
except Exception as e:
    messagebox.showerror("Directory Error", f"Cannot list directory:\n{str(e)}")

# List files in script directory
try:
    files = os.listdir(script_dir)
    messagebox.showinfo("Files in Script Dir", f"Files in script dir:\n" + "\n".join(files[:10]))
except Exception as e:
    messagebox.showerror("Script Dir Error", f"Cannot list script directory:\n{str(e)}") 