from mlflow.tracking import MlflowClient

client = MlflowClient(tracking_uri="sqlite:///mlflow.db")

# Set stage to Production
client.transition_model_version_stage(
    name="yolo11s-cctv-detector",
    version=1,
    stage="Production"
)

print("Model is now in Production!")
