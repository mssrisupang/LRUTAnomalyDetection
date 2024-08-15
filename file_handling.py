# file_handling.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Label
import pandas as pd

df_merged = None  # Global variable to store the DataFrame

def upload_excel(results_text_widget: tk.Text):
    global df_merged

    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

    if file_path:
        df_merged = pd.read_excel(file_path)
        results_text_widget.delete('1.0', tk.END)
        results_text_widget.insert('1.0', f"File {file_path} loaded successfully.\n")
        return df_merged
    else:
        df_merged = None
        results_text_widget.insert('1.0', "File loading was cancelled.\n")

def set_base_path(new_base_path: str):
    global base_path
    base_path = new_base_path

def get_base_path() -> str:
    return base_path if base_path else ""

'''
def get_base_path():
    """
    Set the base path for saving or loading additional resources like images.
    """
    return r"D:\Research\Project-Research\23. GuideWave-PPTEP\polarplot\Standardized"

'''