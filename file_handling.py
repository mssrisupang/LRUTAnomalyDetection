# file_handling.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Label
import pandas as pd
import os

base_path = ""  # Initial value

df_merged = None  # Global variable to store the DataFrame

def upload_excel():
    global df_merged
    file_path = get_file_path()  # Ensure the file path is retrieved properly
    if file_path:
        try:
            df_merged = pd.read_excel(file_path)
           # results_text_widget.delete('1.0', tk.END)
            #results_text_widget.insert('1.0', f"File {file_path} loaded successfully.\n")
            return df_merged
        except Exception as e:
            #results_text_widget.insert('1.0', f"Failed to load file: {e}\n")
            df_merged = None
            return None
    else:
        #results_text_widget.insert('1.0', "File loading was cancelled.\n")
        return None

def get_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data', 'Augmented_All_stats_segments_RAW.xlsx')  # Assuming it's an Excel file
    if not os.path.exists(file_path):
        file_path = filedialog.askopenfilename(title="Select the Excel file", filetypes=[("Excel files", "*.xlsx")])
    return file_path

def get_base_path() -> str:
    global base_path
    return base_path if base_path else ""

def set_base_path(new_base_path: str):
    global base_path
    base_path = new_base_path