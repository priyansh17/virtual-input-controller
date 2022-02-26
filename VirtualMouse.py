import cv2
import handTrackingModule as htm
import numpy as np
import autopy
import time
from autopy.key import *
from autopy import *


def moveMouse():
    global prevX, prevY, currY, currX, x3, y3, x1, y1
    x3 = np.interp(x1, (0, frameReducedW), (0, wScr))
    y3 = np.interp(y1, (frameReducedH, heightCap - frameReducedH), (0, hScr))
    currX = prevX + (x3 - prevX) / smoothen
    currY = prevY + (y3 - prevY) / smoothen
    try:
        autopy.mouse.move(wScr - currX, currY)
    except ValueError:
        pass
    prevX, prevY = currX, currY


widthCap = 640
heightCap = 480
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# capture.set(cv2.CAP_PROP_FPS, 30)
capture.set(3, widthCap)
capture.set(4, heightCap)
prevTime = 0
detector = htm.handDetector(maxHands=1, detectionConfidence=0.8)
wScr, hScr = autopy.screen.size()
frameReducedW = int(widthCap / 2) + 100
frameReducedH = 100
smoothen = 5
prevX, prevY = 0, 0
shooting = False

while capture.isOpened():
    global currY, currX, x3, y3, x1, y1
    success, vid = capture.read()

    hands, _ = detector.detectHands(vid)
    locations, bbox = detector.findLocations(vid)

    if len(locations):
        x1, y1 = locations[8][1:]
        x2, y2 = locations[12][1:]
        cv2.rectangle(vid, (0, frameReducedH), (frameReducedW, heightCap - frameReducedH),
                      (255, 0, 255), 2)

        fingers = detector.fingersUp(hands[0])

        if fingers[1] == 1 and (fingers[2] + fingers[3] + fingers[4]) == 0:
            moveMouse()
            if shooting:
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=False)
                shooting = False

        if fingers[1] + fingers[2] == 2 and fingers[3] + fingers[4] == 0:
            # distance, vid, params = detector.findDistance(8, 12, vid)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=True)  # Start Shooting
            shooting = True
            moveMouse()

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(vid, str(int(fps) * 2), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=2, color=(255, 0, 255), thickness=3)
    cv2.imshow("Video", vid)
    cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()
