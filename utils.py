from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Label
from file_handling import get_base_path
import numpy as np
import pandas as pd

def display_ground_truth_image(right_frame, case_number, frequency):
    base_path = get_base_path()
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


#def display_results_in_treeview(df):
def display_results_in_treeview(tree, df, plot_polar_anomalies, root, right_frame):
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

def display_dwg_image(right_frame, case_number):
    # Construct the file path for the DWG plot (assuming it's saved as an image)
    base_path = get_base_path()
    dwg_folder = "polar_DWG"
    filename = f"case{case_number}.png"  # Adjust according to your naming convention
    #image_path = os.path.join(base_path, filename)
    image_path = os.path.join(base_path, dwg_folder, filename)

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.ANTIALIAS)  # Resize the image if necessary
        img_photo = ImageTk.PhotoImage(img)

        if hasattr(right_frame, 'dwg_image_label'):
            right_frame.dwg_image_label.configure(image=img_photo)
            right_frame.dwg_image_label.image = img_photo  # Keep a reference
        else:
            right_frame.dwg_image_label = tk.Label(right_frame, image=img_photo)
            right_frame.dwg_image_label.image = img_photo  # Keep a reference
            right_frame.dwg_image_label.grid(row=1, column=1, pady=10)  # Position it below the polar plot
    else:
        print("DWG image file does not exist:", image_path)



def plot_polar_anomalies(root, right_frame, anomaly_segments):
    print("Plotting anomalies for segments:", anomaly_segments)  # Debug print
    # Close previous figure if it exists to avoid memory issues
    if hasattr(right_frame, 'canvas'):
        plt.close('all')  # This closes all figures to manage memory usage

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(3, 3))
    num_segments = 8
    # Create theta for segment centers, but rotate by 22.5 degrees (pi/8 radians) so each segment aligns correctly
    theta = np.linspace(0.0, 2 * np.pi, num_segments, endpoint=False) + (np.pi / num_segments)
   # theta = np.linspace(0.0, 2 * np.pi, num_segments, endpoint=False)
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

#def on_tree_select(event):
def on_tree_select(event, tree, root, right_frame, plot_polar_anomalies, display_ground_truth_image, display_dwg_image):
    selected_item = tree.focus()  # Get selected item in the Treeview
    if selected_item:
        row_values = tree.item(selected_item, 'values')

        case_number = row_values[0]
        frequency = row_values[1]

       

        # Convert map object to list
        anomaly_segments = list(map(int, row_values[3].split(', ')))
        plot_polar_anomalies(root, right_frame, anomaly_segments)
        display_ground_truth_image(right_frame, case_number, frequency)

        #Update the DWG image as well
        display_dwg_image(right_frame, case_number)