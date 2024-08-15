import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Label
import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

frequencies = ['36Hz', '44Hz', '67Hz']

def display_ground_truth_image(right_frame, case_number, frequency):
    base_path = r"D:\Research\Project-Research\23. GuideWave-PPTEP\polarplot\Standardized"
    # Ensure frequency is formatted correctly, assuming it ends with 'Hz' and needs to be upper case
    frequency = frequency.replace("Hz", "").upper() + "HZ"
    # Construct the filename based on formatted inputs
    filename = f"case{case_number}_{frequency}Hz.png"
    image_path = os.path.join(base_path, filename)

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.ANTIALIAS)  # Adjust the size as needed
        img_photo = ImageTk.PhotoImage(img)
        if hasattr(right_frame, 'image_label'):
            right_frame.image_label.configure(image=img_photo)
            right_frame.image_label.image = img_photo  # Keep a reference
        else:
            right_frame.image_label = Label(right_frame, image=img_photo)
            right_frame.image_label.image = img_photo  # Keep a reference
            right_frame.image_label.grid(row=1, column=0, pady=10)
    else:
        print("Image file does not exist:", image_path)

def plot_polar_anomalies(root, right_frame, anomaly_segments):
    print("Plotting anomalies for segments:", anomaly_segments)  # Debug print
    # Close previous figure if it exists to avoid memory issues
    if hasattr(right_frame, 'canvas'):
        plt.close('all')  # This closes all figures to manage memory usage

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(4, 4))
    num_segments = 8
    theta = np.linspace(0.0, 2 * np.pi, num_segments, endpoint=False)
    radii = np.ones(num_segments)
    width = 2 * np.pi / num_segments

    bars = ax.bar(theta, radii, width=width, bottom=0.0)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)

    for i, bar in enumerate(bars):
        if i+1 in anomaly_segments:
            bar.set_facecolor('red')
        else:
            bar.set_facecolor('gray')
        bar.set_alpha(0.8)

    # Draw the figure on the canvas
    if hasattr(right_frame, 'canvas'):
        right_frame.canvas.figure.clf()
        right_frame.canvas.figure = fig
        right_frame.canvas.draw()
    else:
        right_frame.canvas = FigureCanvasTkAgg(fig, master=right_frame)
        right_frame.canvas_widget = right_frame.canvas.get_tk_widget()
        right_frame.canvas_widget.grid(row=0, column=0, sticky='nsew')
        right_frame.canvas.draw()

    # Optionally, you can close the figure after drawing to free up memory
    #plt.close(fig)

def z_score_method(df, frequencies):
    
    threshold = 2
    
    outliers_result_df = pd.DataFrame(columns=['#Case', '#Frequency', '#Defect', '#Anomaly Segments'])
    data_list = []
    for case in df['#Case'].unique():
        for freq in frequencies:
            features = [f'std_{freq.lower()}', f'area_{freq.lower()}', f'peri_{freq.lower()}', f'dist_{freq.lower()}']
            sub_df = df[df['#Case'] == case]
            z_scores = sub_df[features].apply(zscore)
            outlier_rows = z_scores[(z_scores.abs() > threshold).any(axis=1)]
            if not outlier_rows.empty:
                outlier_segments = sub_df.loc[outlier_rows.index, '#Segment'].tolist()
                defect_value = df[df['#Case'] == case]['#Defect'].iloc[0]
                data_list.append({'#Case': case, '#Frequency': freq, '#Defect': defect_value, '#Anomaly Segments': outlier_segments})
    if data_list:
        outliers_result_df = pd.DataFrame(data_list)
    return outliers_result_df


def one_class_svm_method(df, frequencies, kernel='rbf', nu=0.1):
    scaler = StandardScaler()
    anomalies_svm_result_df = pd.DataFrame(columns=['#Case', '#Frequency', '#Defect', '#Anomaly Segments'])

    for case in df['#Case'].unique():
        for freq in frequencies:
            features = [f'std_{freq.lower()}', f'area_{freq.lower()}', f'peri_{freq.lower()}', f'dist_{freq.lower()}']
            sub_df = df[df['#Case'] == case]
            if not sub_df.empty and len(sub_df) > 1:
                sub_df_scaled = scaler.fit_transform(sub_df[features])
               # print(f"Sub-DataFrame for case {case} and freq {freq} has shape {sub_df_scaled.shape}")

                one_class_svm = OneClassSVM(kernel=kernel, nu=nu)
                one_class_svm.fit(sub_df_scaled)

                pred = one_class_svm.predict(sub_df_scaled)
                anomaly_rows = sub_df.iloc[pred == -1]

                if not anomaly_rows.empty:
                    anomaly_segments = list(set(anomaly_rows['#Segment'].tolist()))  # Ensure unique segments
                    defect_value = sub_df.iloc[0]['#Defect']
                    anomalies_svm_result_df = anomalies_svm_result_df.append({
                        '#Case': case, 
                        '#Frequency': freq, 
                        '#Defect': defect_value, 
                        '#Anomaly Segments': anomaly_segments
                    }, ignore_index=True)

    return anomalies_svm_result_df

def on_tree_select(event):
    selected_item = tree.focus()  # Get selected item in the Treeview
    if selected_item:
        row_values = tree.item(selected_item, 'values')

        case_number = row_values[0]
        frequency = row_values[1]

        filename = f"case{case_number}_{frequency.replace('Hz', '').upper()}HZ"  # Reformatting here

        # Convert map object to list
        anomaly_segments = list(map(int, row_values[3].split(', ')))
        plot_polar_anomalies(root, right_frame, anomaly_segments)
        display_ground_truth_image(right_frame, case_number, frequency)

def detect_anomalies(data, method):
    # Placeholder for actual anomaly detection logic
    return pd.DataFrame()  # Returning empty DataFrame for illustration

def upload_excel():
    global df_merged  # Use a global variable to store the uploaded data
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    if file_path:
        df_merged = pd.read_excel(file_path)
        #messagebox.showinfo("File Upload", "Excel file uploaded successfully!")
        results_text.delete('1.0', tk.END)  # Clear previous results first
        results_text.insert('1.0', f"File {file_path} loaded successfully.\n")

def display_results_in_treeview(df):
    # Clear previous results from the treeview
    for item in tree.get_children():
        tree.delete(item)
    # Inserting new data into the treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=(row['#Case'], row['#Frequency'], row['#Defect'], ', '.join(map(str, row['#Anomaly Segments']))))
    if not df.empty:
        # Ensure anomaly_segments are properly converted to integers
        last_row_segments = df.iloc[-1]['#Anomaly Segments']
        if isinstance(last_row_segments, str):
            last_row_segments = list(map(int, last_row_segments.split(',')))
        plot_polar_anomalies(root, right_frame, last_row_segments)  # Include right_frame

def run_analysis():
    method = method_var.get()
    if 'df_merged' in globals():
        results_text.delete('1.0', tk.END)  # Clear previous results
        results_text.insert('1.0', f"Running analysis using {method}...\n")
        if method == 'Z-Score Method':
            results_df = z_score_method(df_merged, frequencies)
        elif method == 'OneClass SVM':
            results_df = one_class_svm_method(df_merged, frequencies, kernel='rbf', nu=0.1)
            
        else:
            results_df = detect_anomalies(df_merged, method)
        #results_text.insert(tk.END, str(results_df))
        if not results_df.empty:
            display_results_in_treeview(results_df)
            results_text.insert(tk.END, f"Analysis complete. Displaying results for {method}.\n")
        else:
            results_text.insert(tk.END, "No anomalies detected or empty dataset.\n")
    else:
        messagebox.showerror("Error", "Please upload an Excel file first.")

def main():
    global root, tree, results_text, method_var, right_frame
    root = tk.Tk()
    root.title('Anomaly Detection GUI')

    left_frame = tk.Frame(root)
    right_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky='nsew')
    right_frame.grid(row=0, column=1, sticky='nsew')

    root.grid_columnconfigure(0, weight=1)  # Give weight for expansion
    root.grid_columnconfigure(1, weight=3)  # More weight for right_frame

    upload_btn = tk.Button(left_frame, text="Upload Excel File", command=upload_excel)
    upload_btn.grid(row=0, column=0, padx=10, pady=10)

    method_var = tk.StringVar()
    method_var.set("Select Method")
    methods = ['Z-Score Method', 'Modified Z-Score Method', 'Local Outlier Factor', 'OneClass SVM']
    method_menu = ttk.Combobox(left_frame, textvariable=method_var, values=methods)
    method_menu.grid(row=1, column=0, padx=10, pady=10)

    run_btn = tk.Button(left_frame, text="Run Analysis", command=run_analysis)
    run_btn.grid(row=2, column=0, padx=10, pady=10)

    results_text = tk.Text(left_frame, height=10, width=50)
    results_text.grid(row=3, column=0, padx=10, pady=10)

    tree = ttk.Treeview(left_frame, columns=('Case', 'Frequency', 'Defect', 'Anomaly Segments'), show='headings')
    tree.heading('Case', text='#Case')
    tree.heading('Frequency', text='#Frequency')
    tree.heading('Defect', text='#Defect')
    tree.heading('Anomaly Segments', text='Anomaly Segments')
    tree.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')  # Using grid instead of pack
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    left_frame.grid_rowconfigure(4, weight=1)  # Make the treeview expandable
    left_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
