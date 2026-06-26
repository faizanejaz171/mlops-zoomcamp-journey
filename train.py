model = YOLO("yolo11s.pt")

model.train(
    data="data/data.yaml",
    epochs=50,    # 50 se kam, 1060 pe safe
    imgsz=640,    # 640 ki jagah, VRAM bachega
    batch=4,      # 8 se kam, crash nahi hoga
    device=0
)
