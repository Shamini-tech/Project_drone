# test_ai_inference.py
from backend.ai.inference import infer_from_b64
def load_sample(path="sample.jpg"):
    import base64
    with open(path,"rb") as f:
        b = f.read()
    return "data:image/jpeg;base64," + base64.b64encode(b).decode()

if __name__ == "__main__":
    b64 = load_sample()
    detections, alert, img = infer_from_b64(b64)
    print("Detections:", detections)
    print("Alert:", alert)
