from ultralytics import YOLO
import cv2
import math 
# start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
 print("Cannot open camera")
 exit()
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("model_- 10 april 2024 9_41.pt")

# colors
colors = {
    "Egg": (0, 255, 255),
    "Goal(Large)": (255, 0, 255),
    "Goal(Small)": (255, 0, 255),
    "OBall": (255, 165, 0),
    "Obstacle": (0, 0, 255),
    "WBall": (0, 255, 0),
    "Wall": (0, 0, 255),
    "goosegg-tabletennisball-obstacle": (0, 255, 0),
    "robot": (255, 0, 0),
}

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            name = r.names[math.floor(box.cls[0])]
            print("Class name --> ", name)

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = colors[name]
            thickness = 2

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            cv2.putText(img, name, org, font, fontScale, (255, 0, 0), thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
