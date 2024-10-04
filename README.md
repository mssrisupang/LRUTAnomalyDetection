# LRUT Anomaly Detection

This project is a GUI application for anomaly detection using various statistical and machine learning methods. The application provides an intuitive interface to upload data, run anomaly detection algorithms, and visualize the results using polar plots.

## Features

- **Z-Score Method** Detects outliers using the standard Z-score method.
- **OneClass SVM** Uses One-Class Support Vector Machine to identify anomalies.
- **Local Outlier Factor** Implements the LOF algorithm for outlier detection.
- **Polar Plot Visualization** Visual representation of anomalies in a polar plot format.

## Usage
1. Clone the repository

```bash
git clone https://github.com/yourusername/LRUTAnomalyDetection.git
```

2. Navigate to the project directory

```bash
cd LRUTAnomalyDetection
```

3. Run the application

```bash
python main.py
```
## Requirements
The project dependencies are listed in the requirements.txt file. You can install them using  the following command:

```bash
pip install -r requirements.txt
```

## How to Use
- **Set Image Base Path** Use the "Set Image Base Path" button to specify the directory where your ground truth images are stored.
- **Select Method** Choose one of the anomaly detection methods from the dropdown menu.
- **Run Analysis** Click "Run Analysis" to perform the anomaly detection.
- **View Results** The results will be displayed in the tree view, and anomalies will be visualized in the polar plot.

## Video Demonstration
[![Anomaly Detection Video](https://img.youtube.com/vi/WfHFRsidWQU?si/0.jpg)](https://www.youtube.com/watch?v=WfHFRsidWQU?si)

