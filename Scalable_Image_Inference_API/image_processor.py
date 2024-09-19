import io
from PIL import Image
import torch
from ultralytics import YOLO

# Initialize CUDA in the main process
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load the YOLO-V8 Detector Pretrained model
model = YOLO("yolov8n.pt")
model.to(device)

def process_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        results = model(image)
        
        detections = []
        for result in results:
            for box in result.boxes:
                obj = {
                    "class": result.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist()
                }
                detections.append(obj)
        
        return {"detections": detections}
    except Exception as e:
        return {"error": str(e)}