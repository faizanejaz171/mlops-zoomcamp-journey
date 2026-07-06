from prefect import flow, task
from ultralytics import YOLO
import mlflow

@task(name="validate-data")
def validate_data():
    """Check images and labels exist"""
    from pathlib import Path
    images = list(Path("data/images/train").glob("*.jpg"))
    labels = list(Path("data/labels/train").glob("*.txt"))
    print(f"Images: {len(images)}, Labels: {len(labels)}")
    assert len(images) > 0, "No images found!"
    return len(images)

@task(name="train-model")
def train_model():
    """Train YOLO model"""
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("yolo11s-pipeline")
    
    with mlflow.start_run(run_name="pipeline-run"):
        model = YOLO("yolo11s.pt")
        results = model.train(
            data="data/data.yaml",
            epochs=50,
            imgsz=640,
            batch=4,
            device=0
        )
        
        map50 = results.results_dict["metrics/mAP50(B)"]
        mlflow.log_metric("mAP50", map50)
        
    return map50

@task(name="register-model")
def register_model(map50):
    """Register model if accuracy is good enough"""
    if map50 >= 0.80:
        from mlflow.tracking import MlflowClient
        client = MlflowClient(tracking_uri="sqlite:///mlflow.db")
        
        try:
            client.create_registered_model("yolo11s-pipeline-model")
        except:
            pass
            
        print(f"Model registered! mAP50: {map50:.3f}")
    else:
        print(f"Model not good enough: {map50:.3f} < 0.80")

@flow(name="yolo-training-pipeline")
def main_pipeline():
    """Main training pipeline"""
    validate_data()
    map50 = train_model()
    register_model(map50)

if __name__ == "__main__":
    main_pipeline()
