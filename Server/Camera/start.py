import cv2
import os
from camera import runModel

usr_input = 0

cap = 0

while usr_input == 0:
    os.system('cls')

    print('1. Run Test Footage')
    print('2. Run Webcam')
    print('3. Quit')
    print()

    x = input()
    print()

    if x == '1':
        os.system('cls')
        
        print('loading video...')
        cap = cv2.VideoCapture("test_video.mp4")

        os.system('cls')

        runModel(cap)
    elif x == '2':
        os.system('cls')

        print('What resolution do you want?')
        print()
        print('Width: ', end="")
        width = input()
        print('Height: ', end="")
        height = input()

        os.system('cls')

        print('loading camera...')
        # start webcam
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        os.system('cls')
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        cap.set(3, int(width))
        cap.set(4, int(height))
        runModel(cap)
    elif x == '3':
        os.system('cls')
        usr_input = 1