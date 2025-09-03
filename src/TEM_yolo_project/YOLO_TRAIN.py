from ultralytics import YOLO

model = YOLO('yolov8s.yaml')  


model.train(
    data='tem_crop_dataset/config.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,  
    name='my_yolo_experiment',
    resume=False  
)
