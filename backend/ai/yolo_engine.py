# backend/ai/yolo_engine.py
"""
CPU-based YOLO-like stub using PyTorch model if available.
This file exposes `load_model()` and `run_inference(image)`.

If you later replace with TensorRT, keep interface the same.
"""
import torch
import numpy as np

class DummyModel:
    def __init__(self):
        pass

    def __call__(self, images):
        # images: batch of numpy arrays (HxWxC)
        results = []
        for img in images:
            h, w = img.shape[:2]
            # dummy detection: center PERSON if brightness high, else NO_THREAT
            mean = img.mean()
            if mean > 100:
                results.append([{
                    "label": "person",
                    "confidence": 0.85,
                    "bbox": [w//4, h//4, w//2, h//2]
                }])
            else:
                results.append([])
        return results

def load_model(device='cpu'):
    # try to load torch model if available (user may provide)
    try:
        # placeholder for user to replace with actual YOLOv5/YOLOv8 load code
        model = DummyModel()
        return model
    except Exception as e:
        print("Failed to load model, using DummyModel.", e)
        return DummyModel()

def run_inference(model, image_np):
    """
    image_np: HxWxC numpy uint8
    returns: list of detections dicts: {label, confidence, bbox[x,y,w,h]}
    """
    # normalize / preprocess if required
    results = model([image_np])
    return results[0]
