from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Label
from file_handling import get_base_path
import numpy as np
import pandas as pd

def display_ground_truth_image(ground_frame, case_number, frequency):
    base_path = get_base_path()
    # Ensure frequency is formatted correctly, assuming it ends with 'Hz' and needs to be upper case
    #frequency = frequency.replace("Hz", "").upper() + "HZ"
    # Construct the filename based on formatted inputs
    
    filename = f"case{case_number}_{frequency}.png"
       
    image_path = f"{base_path}/{filename}"  # Use base path from 

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.ANTIALIAS)  # Adjust the size as needed
        # Clear any previous figure
        for widget in ground_frame.winfo_children():
            widget.destroy()

        # Create a matplotlib figure
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.imshow(img)
        ax.set_title(f"Polar Plot Case {case_number} - {frequency}", fontsize=9)
        ax.axis('off')  # Turn off axes

        # Embed the matplotlib plot in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=ground_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=2,padx=2, pady=2)
    else:
        print(f"Image file does not exist: {image_path}")


#def display_results_in_treeview(df):
def display_results_in_treeview(tree, df, plot_polar_anomalies, root, polar_plot):
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
        plot_polar_anomalies(polar_plot, last_row_segments)  # Include right_frame


def display_dwg_image(dwg_frame, case_number):
    base_path = get_base_path()
    for widget in dwg_frame.winfo_children():
        widget.destroy()

    dwg_folder = "polar_DWG"
    filename = f"case{case_number}.png"
    image_path = f"{base_path}/{dwg_folder}/{filename}"  # Use base path from user input

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.ANTIALIAS)  # Adjust the size as needed
        for widget in dwg_frame.winfo_children():
            widget.destroy()

         # Create a matplotlib figure
        fig1, ax1 = plt.subplots(figsize=(3, 2))
        ax1.imshow(img)
        ax1.set_title(f"DWG Case {case_number}", fontsize=9)
        ax1.axis('off')  # Turn off axes
       
        # Embed the matplotlib plot in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig1, master=dwg_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=1, padx=2,pady=2)
        
    else:
        print(f"Image file does not exist: {image_path}")
        

      
def plot_polar_anomalies(polar_plot, anomaly_segments):
    print("Plotting anomalies for segments:", anomaly_segments)  # Debug print
    # Close previous figure if it exists to avoid memory issues
    if hasattr(polar_plot, 'canvas'):
        plt.close('all')  

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
    if hasattr(polar_plot, 'canvas'):
        polar_plot.canvas.figure.clf()
        polar_plot.canvas.figure = fig
        polar_plot.canvas.draw()
    else:
        polar_plot.canvas = FigureCanvasTkAgg(fig, master=polar_plot)
        polar_plot.canvas_widget = polar_plot.canvas.get_tk_widget()
        polar_plot.canvas.draw()
        polar_plot.canvas_widget.grid(row=0, column=1, sticky='nsew')
       


def on_tree_select(event, tree, root, polar_plot,right_frame, dwg_frame,plot_polar_anomalies, ground_frame,display_ground_truth_image, display_dwg_image):


    selected_item = tree.focus()  # Get selected item in the Treeview
    if selected_item:
        row_values = tree.item(selected_item, 'values')

        case_number = row_values[0]
        frequency = row_values[1]
  
        # Convert map object to list
        anomaly_segments = list(map(int, row_values[3].split(', ')))
        plot_polar_anomalies(polar_plot, anomaly_segments)
        
        display_ground_truth_image(ground_frame, case_number, frequency)

        #Update the DWG image as well
        display_dwg_image(dwg_frame, case_number)
        