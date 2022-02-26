import cv2
import handTrackingModule as htm
import autopy
import time

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
        if y in down:
            if x in left:
                print("A")
            elif x in right:
                print("D")
            elif x in center:
                print("S")
        elif y in up:
            if x in center:
                print("W")


while capture.isOpened():
    global currY, currX, x3, y3, x1, y1
    success, vid = capture.read()
    hands, vid = detector.detectHands(vid)

    if hands:
        # Hand 1
        hand1 = hands[0]
        handType1 = hand1["type"]
        if handType1 == "Left":
            keyboardFunctionality(hand1, vid)
        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            hand2 = hands[1]
            handType2 = hand2["type"]
            fingers2 = detector.fingersUp(hand2)

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime
    cv2.putText(vid, "FPS: " + str(int(fps) * 2), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1, color=(255, 0, 255), thickness=3)
    cv2.imshow("Video", vid)
    cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()
