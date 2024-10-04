import tkinter as tk
from tkinter import filedialog, ttk
from file_handling import upload_excel, set_base_path, get_base_path
from run_analysis import run_analysis_
from utils import on_tree_select, display_ground_truth_image, plot_polar_anomalies, display_dwg_image


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
    root.title('LRUT Anomaly Detection GUI')

    width = root.winfo_screenwidth() 
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.protocol("WM_DELETE_WINDOW", root.quit)

    left_frame = tk.Frame(root, width=100, height=200, bg='grey')
    left_frame.grid(row=0, column=0, padx=2, pady=2,sticky='nsew')

    tool_bar = tk.Frame(left_frame, width=100, height=40, bg='grey')
    tool_bar.grid(row=0, column=0, padx=2, pady=2,sticky='nsew')

    tree_frame = tk.Frame(left_frame, width=100, height=200, bg='grey')
    tree_frame.grid(row=1, column=0, padx=2, pady=2,sticky='nsew')

    
    right_frame = tk.Frame(root, width=100, height=100, bg='grey')
    right_frame.grid(row=0, column=1, padx=2, pady=2,sticky='nsew')
    
    polar_plot = tk.Frame(right_frame, width=100, height=30)
    tk.Label(right_frame, text="Anomaly Detection").grid(row=0, column=2, padx=2, pady=2)
    polar_plot.grid(row=0, column=1, padx=2, pady=2)

    ground_frame = tk.Frame(right_frame, width=100, height=100, bg='grey')
    ground_frame .grid(row=1, column=2, padx=2, pady=2,sticky='nsew')  # Place next 
    
    dwg_frame = tk.Frame(right_frame, width=100, height=100, bg='grey')
    #tk.Label(right_frame, text="DWG Image").grid(row=1, column=1, padx=2, pady=2)
    #tk.Label(right_frame, text="Polar Plot").grid(row=1, column=2, padx=2, pady=2)
    dwg_frame.grid(row=1, column=1, padx=2, pady=2,sticky='nsew')  # Place next to the right_frame
   
   
    
    df_merged = None  # Local variable to store the DataFrame
    df_merged = upload_excel()    
    
    def handle_run_analysis():
            if df_merged is not None:
                run_analysis_(df_merged, method_var.get(), results_text,tree,root, polar_plot)
            else:
                results_text.insert('1.0', "Please upload a file before running analysis.\n")

    path_btn = tk.Button(tool_bar, text="Set Image Base Path", command=lambda: set_image_path(results_text))
    path_btn.grid(row=0, column=1, padx=2, pady=2)   

    # Create radio buttons for method selection
    method_var = tk.StringVar()
    method_var.set("Z-Score Method")  # Default selection

    methods = ['Z-Score Method', 'Modified Z-Score Method', 'Local Outlier Factor', 'OneClass SVM']
    method_label = tk.Label(tool_bar, text="Select Method:")
    method_label.grid(row=1, column=0, padx=2, pady=2)

    for i, method in enumerate(methods):
        radio_button = tk.Radiobutton(tool_bar, text=method, variable=method_var, value=method)
        radio_button.grid(row=2+i, column=0, padx=2, pady=2, sticky='nsew')

    
    run_btn = tk.Button(tool_bar, text="Run Analysis", font=('tahoma 13') ,bg='RED',command=handle_run_analysis)
    run_btn.grid(row=2, column=1, padx=3, pady=3)

    results_text = tk.Text(tool_bar, height=10, width=40)
    results_text.grid(row=0, column=0, padx=2, pady=2)

    tree = ttk.Treeview(tree_frame, columns=('Case', 'Frequency', 'Defect', 'Anomaly Segments'), show='headings')
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

    tree.bind('<<TreeviewSelect>>', lambda event: on_tree_select(
        event, tree, root, polar_plot, right_frame, dwg_frame, 
        plot_polar_anomalies, ground_frame, display_ground_truth_image, display_dwg_image
    ))
    


    tree_frame.grid_rowconfigure(4, weight=1)  # Make the treeview expandable
    tree_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()