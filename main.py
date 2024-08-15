# main.py

from gui import setup_gui
from file_handling import upload_excel
from run_analysis import run_analysis_
from utils import display_ground_truth_image, display_results_in_treeview, plot_polar_anomalies, on_tree_select

def main():
    # Setup the GUI
    setup_gui()

if __name__ == "__main__":
    main()
