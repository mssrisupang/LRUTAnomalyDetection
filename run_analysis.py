import pandas as pd
import tkinter as tk
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import zscore
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from file_handling import upload_excel
from utils import display_results_in_treeview, plot_polar_anomalies
from typing import List  # Import List from typing module
from file_handling import df_merged 


def detect_anomalies(data: pd.DataFrame, method: str) -> pd.DataFrame:
    # Placeholder for actual anomaly detection logic
    return pd.DataFrame()  # Returning empty DataFrame for illustration


def z_score_method(df: pd.DataFrame, frequencies: List[str]) -> pd.DataFrame:
    """
    Detects outliers using Z-score method for specified frequencies.
    
    :param df: Input DataFrame containing the data to analyze
    :param frequencies: List of frequency columns to analyze
    :return: DataFrame with detected anomalies
    """
    
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

#def one_class_svm_method(df, frequencies, kernel='rbf', nu=0.1):
def one_class_svm_method(df: pd.DataFrame, frequencies: List[str], kernel: str = 'rbf', nu: float = 0.1) -> pd.DataFrame:
    """
    Detects outliers using OneClass SVM for specified frequencies.
    
    :param df: Input DataFrame containing the data to analyze
    :param frequencies: List of frequency columns to analyze
    :param kernel: Kernel type for the SVM algorithm
    :param nu: An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors
    :return: DataFrame with detected anomalies
    """
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

def modified_z_score_method(df: pd.DataFrame, frequencies: List[str]):

    # Assuming df_merged is your DataFrame
    threshold = 2
   
    # Create an empty DataFrame to store the results
    outliers_result_df = pd.DataFrame(columns=['#Case', '#Frequency', '#Defect', '#Anomaly Segments'])

    # Loop through each unique case
    for case in df['#Case'].unique():
        # Loop through each frequency
        for freq in frequencies:
            # Create features list based on frequency
            features = [f'std_{freq.lower()}', f'area_{freq.lower()}', f'peri_{freq.lower()}', f'dist_{freq.lower()}']

            # Create a sub-dataframe for each case
            sub_df = df[df['#Case'] == case]

            # Calculate the Modified Z-scores
            mad = sub_df[features].mad()
            median = sub_df[features].median()
            modified_z_scores = 0.6745 * (sub_df[features] - median).abs() / mad

            # Find rows where any feature has a Modified Z-score > threshold
            outlier_rows = modified_z_scores[(modified_z_scores[features[0]] > threshold) |
                                            (modified_z_scores[features[1]] > threshold) |
                                            (modified_z_scores[features[2]] > threshold) |
                                            (modified_z_scores[features[3]] > threshold)]

            # If there are any outlier rows, add them to the DataFrame
            if not outlier_rows.empty:
                outlier_segments = sub_df.loc[outlier_rows.index, '#Segment'].tolist()
                defect_value = df[df['#Case'] == case]['#Defect'].iloc[0]  # Assuming all rows for a case have the same #Defect value
                outliers_result_df = outliers_result_df.append({'#Case': case, '#Frequency': freq, '#Defect': defect_value, '#Anomaly Segments': outlier_segments}, ignore_index=True)

       
    return outliers_result_df

def local_outlier_factor_method(df: pd.DataFrame, frequencies: List[str]):

    # LOF parameters
    n_neighbors = 10
    contamination = 0.2  # Proportion of outliers in the data set

        # Create an empty DataFrame to store the results
    outliers_lof_result_df = pd.DataFrame(columns=['#Case', '#Frequency', '#Defect', '#Anomaly Segments'])

    # Loop through each unique case
    for case in df['#Case'].unique():
        # Loop through each frequency
        for freq in frequencies:
            # Create features list based on frequency
            features = [f'std_{freq.lower()}', f'area_{freq.lower()}', f'peri_{freq.lower()}', f'dist_{freq.lower()}']

            # Create a sub-dataframe for each case
            sub_df = df[df['#Case'] == case]

            # Initialize Local Outlier Factor
            lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination)
            pred = lof.fit_predict(sub_df[features])

            # Find rows where LOF labels them as outliers
            outlier_rows = sub_df[pred == -1]

            # If there are any outlier rows, add them to the DataFrame
            if not outlier_rows.empty:
                outlier_segments = outlier_rows['#Segment'].tolist()
                defect_value = df[df['#Case'] == case]['#Defect'].iloc[0]  # Assuming all rows for a case have the same #Defect value
                new_row = pd.DataFrame({'#Case': [case], '#Frequency': [freq], '#Defect': [defect_value], '#Anomaly Segments': [outlier_segments]})
                outliers_lof_result_df = pd.concat([outliers_lof_result_df, new_row], ignore_index=True)

    return outliers_lof_result_df


def run_analysis_(df_merged: pd.DataFrame, method:str, results_text_widget: tk.Text, tree,root, right_frame):
   

    if df_merged is not None:
        results_text_widget.delete('1.0', tk.END)  # Clear previous results
        results_text_widget.insert('1.0', f"Running analysis using {method}...\n")
        
        frequencies = ['36Hz', '44Hz', '67Hz']  # Assuming these are your frequency columns
        
        if method == 'Z-Score Method':
            results_df = z_score_method(df_merged, frequencies)
        elif method == 'OneClass SVM':
            results_df = one_class_svm_method(df_merged, frequencies)
        elif method == 'Modified Z-Score Method':
            results_df = modified_z_score_method(df_merged, frequencies)
        elif method == 'Local Outlier Factor':
            results_df = local_outlier_factor_method(df_merged, frequencies)
        else:
            results_df = detect_anomalies(df_merged, method)
        
        if not results_df.empty:
            #display_results_in_treeview(results_df)
            display_results_in_treeview(tree, results_df, plot_polar_anomalies, root, right_frame)
            results_text_widget.insert(tk.END, f"Analysis complete. Displaying results for {method}.\n")
        else:
            results_text_widget.insert(tk.END, "No anomalies detected or empty dataset.\n")
    else:
        results_text_widget.insert(tk.END, "Failed to load a file or operation was cancelled.\n")
        #messagebox.showerror("Error", "Please upload an Excel file first.")