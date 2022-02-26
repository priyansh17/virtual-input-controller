import cv2
import handTrackingModule as htm
import autopy
import time
from pynput.keyboard import Controller as CK
from pynput.mouse import Controller as CM
import numpy as np


keyboard = CK()
mouse = CM()
widthCap = 640
heightCap = 480
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, widthCap)
capture.set(4, heightCap)
prevTime = 0
detector = htm.handDetector(maxHands=1, detectionConfidence=0.8)
wScr, hScr = autopy.screen.size()
frameReducedW = int(widthCap / 2) + 50
frameReducedH = 100
keyW = int((widthCap - frameReducedW) / 3)
keyH = int(heightCap / 3)
prevX, prevY = 0, 0
shooting = False
smoothen = 5


def movementMouse(Vid):
    cv2.rectangle(Vid, (0, frameReducedH), (frameReducedW, heightCap - frameReducedH),
                  (255, 0, 255), 2)


def movementKeys(Vid):
    cv2.rectangle(Vid, (frameReducedW + keyW, keyH), (widthCap - keyW, 2 * keyH),
                  (0, 0, 255), 2)
    cv2.rectangle(Vid, (widthCap - keyW, keyH), (widthCap, 2 * keyH),
                  (0, 0, 255), 2)
    cv2.rectangle(Vid, (frameReducedW + keyW, 0), (widthCap - keyW, keyH),
                  (0, 0, 255), 2)
    cv2.rectangle(Vid, (frameReducedW, keyH), (frameReducedW + keyW, 2 * keyH),
                  (0, 0, 255), 2)


def releaseAll():
    autopy.key.toggle(autopy.key.Code.LEFT_ARROW, False)
    autopy.key.toggle(autopy.key.Code.RIGHT_ARROW, False)
    autopy.key.toggle(autopy.key.Code.UP_ARROW, False)
    autopy.key.toggle(autopy.key.Code.DOWN_ARROW, False)
    autopy.key.toggle(autopy.key.Code.CAPS_LOCK, False)


def keyboardFunctionality(hand, Vid):
    movementKeys(Vid)
    locations = hand["LocationList"]
    up = range(0, keyH)
    down = range(keyH, 2 * keyH)
    left = range(frameReducedW, frameReducedW + keyW)
    right = range(widthCap - keyW, widthCap)
    center = range(frameReducedW + keyW, widthCap - keyW)
    if len(locations):
        x, y = locations[8][1:]
        # releaseAll()
        if y in down:
            if x in left:
                keyboard.press('A')
            elif x in right:
                keyboard.press('D')
            elif x in center:
                keyboard.press('S')
        elif y in up:
            if x in center:
                keyboard.press('W')


def moveMouse(x1, y1):
    global prevX, prevY
    x3 = np.interp(x1, (0, frameReducedW), (0, wScr))
    y3 = np.interp(y1, (frameReducedH, heightCap - frameReducedH), (0, hScr))
    currX = prevX + (x3 - prevX) / smoothen
    currY = prevY + (y3 - prevY) / smoothen
    try:
        autopy.mouse.move(wScr - currX, currY)
    except ValueError:
        pass
    prevX, prevY = currX, currY


def mouseFunctionality(hand, Vid):
    global shooting
    movementMouse(Vid)
    locations = hand["LocationList"]
    if len(locations):
        x1, y1 = locations[8][1:]
        cv2.rectangle(vid, (0, frameReducedH), (frameReducedW, heightCap - frameReducedH),
                      (255, 0, 255), 2)

        fingers = detector.fingersUp(hand)

        if fingers[1] == 1 and (fingers[2] + fingers[3] + fingers[4]) == 0:
            moveMouse(x1, y1)
            if shooting:
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=False)
                shooting = False

        if fingers[1] + fingers[2] == 2 and fingers[3] + fingers[4] == 0:
            # distance, vid, params = detector.findDistance(8, 12, vid)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, down=True)  # Start Shooting
            shooting = True
            moveMouse(x1, y1)


while capture.isOpened():
    success, vid = capture.read()
    hands, vid = detector.detectHands(vid)

    if hands:
        # Hand 1
        hand1 = hands[0]
        handType1 = hand1["type"]
        if handType1 == "Left":
            keyboardFunctionality(hand1, vid)
        else:
            mouseFunctionality(hand1, vid)
        if len(hands) == 2:
            hand2 = hands[1]
            handType2 = hand2["type"]
            if handType2 == "Left":
                keyboardFunctionality(hand2, vid)
            else:
                mouseFunctionality(hand2, vid)

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(vid, "FPS: " + str(int(fps) * 2), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=(255, 0, 255), thickness=3)
    cv2.imshow("Video", vid)
    cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()
