import cv2
import numpy as np
from pybricks.messaging import BluetoothMailboxClient, TextMailbox

# Initialize the Bluetooth connection
SERVER = "ev3dev"  # Name of the EV3 Brick
client = BluetoothMailboxClient()
mbox = TextMailbox("command", client)

print("Establishing connection to EV3...")
client.connect(SERVER)
print("Connected to EV3!")

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Adjust the camera index if needed

# Define the lower and upper bounds for the orange color in HSV
lower_orange = np.array([10, 100, 20])
upper_orange = np.array([25, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    orange_mask = cv2.inRange(hsv_frame, lower_orange, upper_orange)
    contours, _ = cv2.findContours(orange_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Assuming a significant area indicates the presence of the ball
            # Send a command to EV3
            mbox.send("start_indsamler")
            break  # Assuming only one command is needed per detection

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client.disconnect()
