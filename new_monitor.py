import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def test_drift_with_one_file(csv_file, output_html):
    """
    Generates a Data Drift report using a single dataset.
    Splits the dataset in half to simulate reference (historical) 
    and current (production) data for demonstration purposes.
    """
    print(f"Reading dataset from: {csv_file}...")
    
    try:
        # 1. Load the dataset
        df = pd.read_csv(csv_file)
        
        # 2. Split the data into two halves to simulate reference and current datasets
        half = len(df) // 2
        ref_df = df.iloc[:half]   # First half acts as the Reference (Training) Data
        curr_df = df.iloc[half:]  # Second half acts as the Current (Production) Data
        
        print("Calculating Data Drift metrics...")
        
        # 3. Initialize and run the Evidently report with the Data Drift preset
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=ref_df, current_data=curr_df)
        
        # 4. Export the generated report to an HTML file
        report.save_html(output_html)
        print(f"Success! Data Drift report saved to '{output_html}'.")
        print("Open this file in your web browser to view the interactive dashboard.")
        
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found. Please verify the file path.")

if __name__ == '__main__':
    # Execute the drift detection pipeline
    test_drift_with_one_file(
        csv_file="my_predictions.csv", 
        output_html="data_drift_dashboard.html"
    )
