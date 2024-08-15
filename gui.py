import tkinter as tk
from tkinter import filedialog, ttk
from file_handling import upload_excel, set_base_path, get_base_path
from run_analysis import run_analysis_
from utils import on_tree_select, display_ground_truth_image, plot_polar_anomalies


def set_image_path(results_text_widget: tk.Text):
    folder_path = filedialog.askdirectory()
    if folder_path:
        set_base_path(folder_path)
        results_text_widget.insert('1.0', f"Image base path set to {folder_path}\n")
    else:
        results_text_widget.insert('1.0', "Setting image base path was cancelled.\n")


def setup_gui():
    global root, tree, results_text, method_var, right_frame
    root = tk.Tk()
    root.title('Anomaly Detection GUI')

    left_frame = tk.Frame(root)
    right_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky='nsew')
    right_frame.grid(row=0, column=1, sticky='nsew')

    root.grid_columnconfigure(0, weight=1)  # Give weight for expansion
    root.grid_columnconfigure(1, weight=3)  # More weight for right_frame

    
    df_merged = None  # Local variable to store the DataFrame

    def handle_upload():
        nonlocal df_merged
        df_merged = upload_excel(results_text)    

    def handle_run_analysis():
            if df_merged is not None:
                run_analysis_(df_merged, method_var.get(), results_text,tree,root, right_frame)
            else:
                results_text.insert('1.0', "Please upload a file before running analysis.\n")

    
    
    upload_btn = tk.Button(left_frame, text="Upload Excel File", command=handle_upload)
    upload_btn.grid(row=0, column=0, padx=10, pady=10)
    
    path_btn = tk.Button(left_frame, text="Set Image Base Path", command=lambda: set_image_path(results_text))
    path_btn.grid(row=0, column=1, padx=10, pady=10)   

    method_var = tk.StringVar()
    method_var.set("Select Method")
    methods = ['Z-Score Method', 'Modified Z-Score Method', 'Local Outlier Factor', 'OneClass SVM']
    method_menu = ttk.Combobox(left_frame, textvariable=method_var, values=methods)
    method_menu.grid(row=1, column=0, padx=10, pady=10)

    run_btn = tk.Button(left_frame, text="Run Analysis", command=handle_run_analysis)
    run_btn.grid(row=2, column=0, padx=10, pady=10)

    results_text = tk.Text(left_frame, height=10, width=50)
    results_text.grid(row=3, column=0, padx=10, pady=10)

    tree = ttk.Treeview(left_frame, columns=('Case', 'Frequency', 'Defect', 'Anomaly Segments'), show='headings')
    tree.heading('Case', text='#Case')
    tree.column('Case', width=20)  # Set width for 'Case' column

    tree.heading('Frequency', text='#Frequency')
    tree.column('Frequency', width=20)

    tree.heading('Defect', text='#Defect')
    tree.column('Defect', width=20)

    tree.heading('Anomaly Segments', text='Anomaly Segments')
    tree.column('Anomaly Segments', width=50)
    tree.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')  # Using grid instead of pack
    #tree.bind('<<TreeviewSelect>>', on_tree_select)
    tree.bind('<<TreeviewSelect>>', lambda event: on_tree_select(event, tree, root, right_frame,plot_polar_anomalies, display_ground_truth_image))


    left_frame.grid_rowconfigure(4, weight=1)  # Make the treeview expandable
    left_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()