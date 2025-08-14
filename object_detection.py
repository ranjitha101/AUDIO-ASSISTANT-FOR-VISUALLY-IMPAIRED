# object_detection.py
from ultralytics import YOLO
import cv2
import pyttsx3
import os

# Auto-download the model if not present
if not os.path.exists("yolov8n.pt"):
    print("Downloading YOLOv8n model...")
    model = YOLO("yolov8n")  # This will download and save yolov8n.pt automatically
else:
    model = YOLO("yolov8n.pt")  # Load the model from local file

# Initialize text-to-speech
engine = pyttsx3.init()

def start_detection():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        names = model.names

        detected = set()

        for box in results.boxes:
            cls = int(box.cls[0])
            label = names[cls]
            detected.add(label)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        if detected:
            spoken = ", ".join(detected)
            print("Detected:", spoken)
            engine.say(f"I see {spoken}")
            engine.runAndWait()

        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
