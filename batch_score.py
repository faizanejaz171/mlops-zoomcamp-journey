import os
import csv
import argparse
import yaml
from ultralytics import YOLO

def process_batch(config_file):
    # 1. Config file ko read karna
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
        
    input_folder = config['data']['input_folder']
    output_file = config['data']['output_file']
    model_path = config['model']['path']

    # 2. Model Load karna
    print(f"Loading model from {model_path}...")
    model = YOLO(model_path)
    
    results_data = []
    
    print(f"Reading images from '{input_folder}'...")
    if not os.path.exists(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    # 3. Processing the images
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            print(f"Processing: {filename}")
            
            results = model(img_path)
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    results_data.append({
                        "image": filename,
                        "class_id": int(box.cls[0]),
                        "confidence": round(float(box.conf[0]), 2),
                        "bbox": box.xyxy[0].tolist()
                    })
                    
    # 4. Result save karna
    print(f"Saving results to '{output_file}'...")
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['image', 'class_id', 'confidence', 'bbox']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results_data:
            writer.writerow(row)
            
    print("Batch processing complete!")

if __name__ == '__main__':
    # Ab terminal mein sirf config file deni paregi
    parser = argparse.ArgumentParser(description="Config-driven batch scoring script")
    parser.add_argument('--config', type=str, default="config.yaml", help="Path to configuration file")
    
    args = parser.parse_args()
    
    process_batch(args.config)
