import cv2
import os
from camera import runModel, runLowPerformanceModel
import threading
import time
from client import algo

usr_input = 0

cap = 0

def chooseVersion(cap):
    print('1. Run with visuals')
    print('2. Run without visuals')
    print('3. Quit')

    print()

    x = input()
    print()

    os.system('cls')

    if x == '1':
        t1 = threading.Thread(target=runModel, args=[cap])
        t2 = threading.Thread(target=algo)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        return 0
    elif x == '2':
        t1 = threading.Thread(target=runLowPerformanceModel, args=[cap])
        t2 = threading.Thread(target=algo)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        return 0
    elif x == '3':
        return 1
    else:
        return chooseVersion(cap)

while usr_input == 0:
    os.system('cls')

    print('1. Run Test Footage')
    print('2. Run Webcam')
    print('3. Quit')
    print('4. Run QuickTest')
    print()

    x = input()
    print()

    if x == '1':
        os.system('cls')
        
        print('loading video...')
        cap = cv2.VideoCapture("test_video_2.mp4")

        os.system('cls')

        usr_input = chooseVersion(cap)
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
        usr_input = chooseVersion(cap)
    elif x == '3':
        os.system('cls')
        usr_input = 1
    
    elif x == '4':
        os.system('cls')
        print('Starting quick test with 1280x720')
        width = 1280
        height = 720
        os.system('cls')
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        cap.set(3, int(width))
        cap.set(4, int(height))
        t1 = threading.Thread(target=runLowPerformanceModel, args=[cap])
        t2 = threading.Thread(target=algo)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

