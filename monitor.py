import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset

def generate_monitoring_report(csv_file, output_html):
    """
    Generates a Data Quality monitoring report using Evidently AI.
    Reads batch predictions from a CSV file and exports an HTML dashboard.
    """
    print(f"Reading data from {csv_file}...")
    
    try:
        # Load the batch inference data
        df = pd.read_csv(csv_file)
        
        # Initialize the Evidently Report with Data Quality metrics
        print("Generating Data Quality Report...")
        report = Report(metrics=[DataQualityPreset()])
        
        # Execute the report on the current dataset
        # Note: reference_data is set to None as we are only analyzing current data quality
        report.run(reference_data=None, current_data=df)
        
        # Export the generated report to an HTML file
        report.save_html(output_html)
        print(f"Success! Report saved to '{output_html}'.")
        
    except FileNotFoundError:
        print(f"Error: '{csv_file}' not found. Please execute the batch scoring script first.")

if __name__ == '__main__':
    # Execute the monitoring report generation pipeline
    generate_monitoring_report(
        csv_file="my_predictions.csv", 
        output_html="monitoring_dashboard.html"
    )
