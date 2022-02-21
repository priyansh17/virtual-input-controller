import cv2
import handTrackingModule as htm
import numpy as np
import mediapipe
import autopy
import time

widthCap = 640
heightCap = 480
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, widthCap)
capture.set(4, heightCap)
prevTime = 0
detector = htm.handDetector(maxHands=1, detectionConfidence=0.7)
wScr, hScr = autopy.screen.size()
frameReducedW = int(widthCap / 2) - 100
frameReducedH = 100
smoothen = 5
prevX, prevY = 0, 0

while capture.isOpened():
    success, vid = capture.read()

    detector.detectHands(vid)
    locations, bbox = detector.findLocations(vid)

    if len(locations):
        x1, y1 = locations[8][1:]
        x2, y2 = locations[12][1:]
        cv2.rectangle(vid, (frameReducedW, frameReducedH), (widthCap, heightCap - frameReducedH),
                      (255, 0, 255), 2)

        fingers = detector.fingersUp()

        if fingers[1] == 1 and (fingers[2] + fingers[3] + fingers[4]) == 0:
            x3 = np.interp(x1, (frameReducedW, widthCap), (0, wScr))
            y3 = np.interp(y1, (frameReducedH, heightCap - frameReducedH), (0, hScr))
            currX = prevX + (x3 - prevX) / smoothen
            currY = prevY + (y3 - prevY) / smoothen
            try:
                autopy.mouse.move(wScr - currX, currY)
            except ValueError:
                pass
            prevX, prevY = currX, currY

        if fingers[1] + fingers[2] == 2 and fingers[3] + fingers[4] == 0:
            distance, vid, params = detector.findDistance(8, 12, vid)
            if distance < 20:
                cv2.circle(vid, (params[4], params[5]), 6, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(vid, str(int(fps)), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=2, color=(255, 0, 255), thickness=3)
    cv2.imshow("Video", vid)
    cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()
