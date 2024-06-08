from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-pose.pt')  # load an official model

# Predict with the model
results = model('11_28_22-player9.webm',max_det=1, show=True, save=True)  # predict on a video file
