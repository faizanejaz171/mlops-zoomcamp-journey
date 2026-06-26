import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("yolo11s-cctv")

with mlflow.start_run(run_name="yolo11s-first-run"):
    mlflow.log_params({
        "model": "yolo11s",
        "epochs": 50,
        "imgsz": 640,
        "batch": 4,
        "dataset": "cctv-head-person-employee"
    })
    
    mlflow.log_metrics({
        "mAP50": 0.862,
        "mAP50_95": 0.685,
        "head_mAP50": 0.927,
        "person_mAP50": 0.866,
        "employee_mAP50": 0.792
    })
    
    mlflow.log_artifact("runs/detect/train/weights/best.pt")

print("Logged!")
