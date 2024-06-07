from ultralytics import YOLO
import cv2
import math 
import numpy as np

# start webcam
cap = cv2.VideoCapture("test_video.mp4")
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

class BoxObject:
    def __init__(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"{self.name}(x1: {self.x1}, y1:{self.y1}, x2:{self.x2}, y2:{self.y2})"   

    def updateBox(self, name, x1, y1, x2, y2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

boxObjects = {}

class Box: 
    def __init__(self):
        self.name = ""

    def updateName(self, name):
        self.name = name

class Grid:
    def __init__(self, res_x, res_y, precision):
        self.res_x = res_x
        self.res_y = res_y
        self.precision = precision
        self.size = precision*precision
        self.cols = math.ceil(res_x/precision)
        self.rows = math.ceil(res_y/precision)

        self.boxes = [[Box() for j in range(self.rows)] for i in range(self.cols)]

    def getBox(self, pos_x, pos_y):
        return self.boxes(math.ceil(pos_x/self.precision), math.ceil(pos_y/self.precision))

    def addBox(self, pos_x1, pos_y1, pos_x2, pos_y2, name):
        x_boxes = math.ceil((self.res_x-pos_x1)/self.precision)-(math.ceil((self.res_x-pos_x2)/self.precision))+1
        y_boxes = math.ceil((self.res_y-pos_y1)/self.precision)-(math.ceil((self.res_y-pos_y2)/self.precision))+1
        
        for x in range(x_boxes):
            for y in range(y_boxes):
                self.boxes[min(round(pos_x2/self.precision)+x-1, self.cols - 1)][min(round(pos_y2/self.precision)+y-1, self.rows - 1)].updateName(name)


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    grid = Grid(1920, 1080, 25)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            #print("Box --->",box)
            #print("Confidence --->",confidence)

            # class name
            name = r.names[math.floor(box.cls[0])]
            #print("Class name --> ", name)

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = colors[name]
            thickness = 2

            boxObject = BoxObject(name, x1, y1, x2, y2)

            boxObjects[name] = boxObject

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            cv2.putText(img, name, org, font, fontScale, (255, 0, 0), thickness)

            grid.addBox(x1, y1, x2, y2, name)

        for x in range(grid.cols):
            for y in range(grid.rows):
                x1, y1, x2, y2 = x*grid.precision-grid.precision, y*grid.precision-grid.precision, x * grid.precision, y * grid.precision
                if grid.boxes[x][y].name == "WBall":
                    # First we crop the sub-rect from the image
                    sub_img = img[y1:y2, x1:x2]
                    white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255

                    res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)

                    # Putting the image back to its position
                    img[y1:y2, x1:x2] = res
                    #cv2.rectangle(img, (x*grid.precision-grid.precision, y*grid.precision-grid.precision), (x * grid.precision, y * grid.precision), (255, 255, 255, 100), -1)
                else:
                    cv2.rectangle(img, (x*grid.precision-grid.precision, y*grid.precision-grid.precision), (x * grid.precision, y * grid.precision), (255, 255, 255), 1)


    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
