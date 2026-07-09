import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()

# Create registered model
try:
    client.create_registered_model("yolo11s-cctv-detector")
except:
    pass  # already exists

# Create version pointing to existing artifact
client.create_model_version(
    name="yolo11s-cctv-detector",
    source="file:///home/faizan/Documents/mlops-zoomcamp-journey/mlruns/1/41d89f8bac2d406ba680e39a8c2971d8/artifacts/best.pt",
    run_id="41d89f8bac2d406ba680e39a8c2971d8"
)

print("Model version created!")
