# main.py

from gui import setup_gui
from file_handling import upload_excel
from run_analysis import run_analysis_
from utils import on_tree_select, display_ground_truth_image, plot_polar_anomalies, display_dwg_image

def main():
    # Setup the GUI
    setup_gui()

if __name__ == "__main__":
    main()
