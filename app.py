from flask import Flask, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io

# 1. Flask app initialize kar rahe hain
app = Flask(__name__)

# 2. Model load kar rahe hain (MLflow se mukammal independent)
print("Loading model...")
model = YOLO("yolo11s.pt")
print("Model loaded successfully!")

# ==========================================
# NAYA ROUTE: Browser ke liye (Home Page)
# ==========================================
@app.route('/', methods=['GET'])
def home():
    # Jab koi browser mein 127.0.0.1:5000 likhega toh yeh JSON show hoga
    return jsonify({
        "status": "Online",
        "model": "YOLO11s",
        "message": "Welcome to the Object Detection API. Send a POST request with an image file to '/predict' to get bounding boxes."
    })

# ==========================================
# PURANA ROUTE: Predictions ke liye
# ==========================================
@app.route('/predict', methods=['POST'])
def predict():
    # Check karna ke request mein 'file' aayi hai ya nahi
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    # Image ko read karna
    file = request.files['file']
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes))
    
    # Model se prediction (inference) karwana
    results = model(img)
    
    # Detections (bounding boxes) ko JSON format mein nikalna
    detections = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            detections.append({
                "class_id": int(box.cls[0]),               
                "confidence": round(float(box.conf[0]), 2), 
                "bbox": box.xyxy[0].tolist()               
            })
            
    # JSON response client ko wapas bhej dena
    return jsonify({"detections": detections})

# Jab file run ho toh server start ho jaye
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
