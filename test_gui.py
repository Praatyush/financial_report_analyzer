#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import os

# Hide the root window
root = tk.Tk()
root.withdraw()

# Test if we can show a popup
messagebox.showinfo("Test", f"GUI Test Successful!\nCurrent directory: {os.getcwd()}")

# Test if we can find our files
try:
    with open('.env', 'r') as f:
        content = f.read()
    messagebox.showinfo("File Test", f"Found .env file:\n{content[:50]}...")
except Exception as e:
    messagebox.showerror("File Error", f"Cannot find .env file:\n{str(e)}") 