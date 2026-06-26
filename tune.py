import mlflow
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from ultralytics import YOLO

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("yolo11s-tuning")

def objective(params):
    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        
        model = YOLO("yolo11s.pt")
        results = model.train(
            data="data/data.yaml",
            epochs=10,          # tuning k liye kam epochs
            imgsz=int(params["imgsz"]),
            batch=int(params["batch"]),
            lr0=params["lr0"],
            device=0,
            verbose=False
        )
        
        map50 = results.results_dict["metrics/mAP50(B)"]
        mlflow.log_metric("mAP50", map50)
        
    return {"loss": -map50, "status": STATUS_OK}

search_space = {
    "imgsz": hp.choice("imgsz", [416, 640]),
    "batch": hp.choice("batch", [4, 8]),
    "lr0": hp.uniform("lr0", 0.001, 0.01)
}

with mlflow.start_run(run_name="hyperopt-search"):
    best = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=6,        # 6 combinations try karega
        trials=Trials()
    )
    print(f"Best params: {best}")
