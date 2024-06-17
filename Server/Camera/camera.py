from ultralytics import YOLO
import os
import math 
import cv2
import numpy as np

# colors
colors = {
    "Egg": (0, 255, 255),
    "Goal(Large)": (255, 0, 255),
    "Goal-Large-": (255, 0, 255),
    "Goal(Small)": (255, 0, 255),
    "Goal-Small-": (255, 0, 255),
    "OBall": (255, 165, 0),
    "Obstacle": (0, 0, 255),
    "WBall": (0, 255, 0),
    "Wall": (0, 0, 255),
    "goosegg-tabletennisball-obstacle": (0, 255, 0),
    "robot": (255, 0, 0),
    "robotBack": (255, 0, 0),
    "robotFront": (255, 0, 0),
}

def drawInGrid(img, x1, y1, x2, y2, rgb):
    bgr = (rgb[2], rgb[1], rgb[0])
    # First we crop the sub-rect from the image
    sub_img = img[y1:y2, x1:x2]
    rect = np.ones(sub_img.shape, dtype=np.uint8) * bgr
    rect = np.asarray(rect, np.uint8)

    res = cv2.addWeighted(sub_img, 0.5, rect, 0.5, 1.0)

    # Putting the image back to its position
    img[y1:y2, x1:x2] = res


class Box: 
    def __init__(self):
        self.name = ""

    def updateName(self, name):
        self.name = name

    def getName(self):
        return self.name

class Grid:
    def __init__(self, res_x, res_y, precision):
        self.res_x = res_x
        self.res_y = res_y
        self.precision = precision
        self.size = precision*precision
        self.cols = math.ceil(res_x/precision)
        self.rows = math.ceil(res_y/precision)

        self.boxes = [[Box() for j in range(self.rows)] for i in range(self.cols)]

        self.robot = (0, 0)
        self.robotFront = (0, 0)
        self.robotBack = (0, 0)
        self.egg = (0, 0)
        self.obstacle = (0, 0)
        self.oBall = (0, 0)
        self.wBalls = []
        self.goalSmall = (0, 0)
        self.goalLarge = (0, 0)

    def getRobot(self):
        return self.robot

    def getRobotFront(self):
        return self.robotFront
        
    def getRobotBack(self):
        return self.robotBack
        
    def getEgg(self):
        return self.egg
    
    def getObstacle(self):
        return self.obstacle
    
    def getOball(self):
        return self.oBall
    
    def getWballs(self):
        return self.wBalls
    
    def getGoalSmall(self):
        return self.goalSmall
    
    def getGoalLarge(self):
        return self.goalLarge
        

    def addBox(self, pos_x1, pos_y1, pos_x2, pos_y2, name):
        x_boxes = math.ceil((self.res_x-pos_x1)/self.precision)-(math.floor((self.res_x-pos_x2)/self.precision))
        y_boxes = math.ceil((self.res_y-pos_y1)/self.precision)-(math.floor((self.res_y-pos_y2)/self.precision))
        positions = []
        
        for x in range(x_boxes):
            for y in range(y_boxes):
                position = [min(math.ceil(max(pos_x1, 1)/self.precision)+x, self.cols - 1), min(math.ceil(max(pos_y1, 1)/self.precision)+y, self.rows - 1)]

                if name == "WBall":
                   self.wBalls.append((position[0], position[1]))
                elif name == "OBall":
                    self.oBall = ((position[0], position[1]))
                elif name == "Egg":
                    self.egg = ((position[0], position[1]))
                elif name == "robot":
                    self.robot = ((position[0], position[1]))
                elif name == "robotFront":
                    self.robotFront = ((position[0], position[1]))
                elif name == "robotBack":
                    self.robotBack = ((position[0], position[1]))
                elif name == "Goal-Small-":
                    self.goalSmall = ((position[0], position[1]))
                elif name == "Goal-Large-":
                    self.goalLarge = ((position[0], position[1]))
                elif name == "Obstacle":
                    self.obstacle = ((position[0], position[1]))

                if (name != "Wall" or self.boxes[position[0]][position[1]].getName() == "") and (self.boxes[position[0]][position[1]].getName() != "Egg"): 

                    self.boxes[position[0]][position[1]].updateName(name)

                    positions.append(position)

        return positions

    def flushGrid(self):
        self.boxes = [[Box() for j in range(self.rows)] for i in range(self.cols)]

    def copyGrid(self, grid):
        self.res_x = grid.res_x
        self.res_y = grid.res_y
        self.precision = grid.precision
        self.size = grid.size
        self.cols = grid.cols
        self.rows = grid.rows

        self.boxes = grid.boxes

        self.robot = grid.robot
        self.robotFront = grid.robotFront
        self.robotBack = grid.robotBack
        self.egg = grid.egg
        self.obstacle = grid.obstacle
        self.oBall = grid.oBall
        self.wBalls = grid.wBalls
        self.goalSmall = grid.goalSmall
        self.goalLarge = grid.goalLarge

global grid
grid = Grid(1,1,1)

def getGrid():
    global grid
    return grid

def runModel(cap):
    global grid

    grid = Grid(cap.get(3), cap.get(4), 10)

    tmp_grid = Grid(cap.get(3), cap.get(4), 10)

    print('Choose a model:')

    models = []

    i = 1

    for x in os.listdir():
        if x.startswith("model_"):
            models.append(x)
            print(i, ': ', x)
            i = i + 1

    model_number = input()

    # model
    model = YOLO(models[int(model_number)-1])

    os.system('cls')

    while True:
        success, img = cap.read()
        results = model(img, stream=True)

        objects = []

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

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                cv2.putText(img, name, org, font, fontScale, (255, 0, 0), thickness)

                positions = tmp_grid.addBox(x1, y1, x2, y2, name)

                objects = objects + positions

            grid.copyGrid(tmp_grid)

            for position in objects:
                rgb = [0, 0, 0]

                x = position[0]
                y = position[1]

                x1, y1, x2, y2 = x*grid.precision-grid.precision, y*grid.precision-grid.precision, x * grid.precision, y * grid.precision

                if grid.boxes[x][y].name == "WBall":
                    rgb = [255, 255, 255]
                elif grid.boxes[x][y].name == "OBall":
                    rgb = [255, 165, 0]
                elif grid.boxes[x][y].name == "Obstacle" or grid.boxes[x][y].name == "Wall":
                    rgb = [255, 0, 0]
                elif grid.boxes[x][y].name == "Egg":
                    rgb = [255, 255, 0]
                elif grid.boxes[x][y].name == "Goal-Small-":
                    rgb = [0, 255, 0]
                elif grid.boxes[x][y].name == "Goal-Large-":
                    rgb = [255, 255, 0]
                elif grid.boxes[x][y].name == "robotFront":
                    rgb = [0, 0, 255]
                elif grid.boxes[x][y].name == "robotBack":
                    rgb = [0, 255, 0]

                drawInGrid(img, x1, y1, x2, y2, rgb)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            return
        tmp_grid.flushGrid()

    cap.release()
    cv2.destroyAllWindows()

def runLowPerformanceModel(cap):
    global grid

    grid = Grid(cap.get(3), cap.get(4), 25)

    tmp_grid = Grid(cap.get(3), cap.get(4), 10)

    print('Choose a model:')

    models = []

    i = 1

    for x in os.listdir():
        if x.startswith("model_"):
            models.append(x)
            print(i, ': ', x)
            i = i + 1

    model_number = input()

    # model
    model = YOLO(models[int(model_number)-1])

    os.system('cls')

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
                #print("Box --->",box)
                #print("Confidence --->",confidence)

                # class name
                name = r.names[math.floor(box.cls[0])]
                #print("Class name --> ", name)

                tmp_grid.addBox(x1, y1, x2, y2, name)

        grid.copyGrid(tmp_grid)
        if cv2.waitKey(1) == ord('q'):
            return
        tmp_grid.flushGrid()

    cap.release()
    cv2.destroyAllWindows()