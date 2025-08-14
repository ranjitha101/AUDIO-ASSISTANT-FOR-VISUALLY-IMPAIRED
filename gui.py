import cv2
import pyttsx3

def detect_objects():
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # Make sure these files are in the same folder
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    cap = cv2.VideoCapture(0)

    engine.say("Object detection started. Press Q to quit.")
    engine.runAndWait()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        detected = set()

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = int(scores.argmax())
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in indexes:
            i = i[0] if isinstance(i, (tuple, list, np.ndarray)) else i
            label = str(classes[class_ids[i]])
            if label not in detected:
                engine.say(f"{label} detected")
                detected.add(label)
        
        engine.runAndWait()

        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
