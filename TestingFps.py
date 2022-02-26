import cv2
import time

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
prevTime = 0

while capture.isOpened():
    success, vid = capture.read()

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    cv2.putText(vid, str(int(fps)*4), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=2, color=(255, 0, 255), thickness=3)
    cv2.imshow("Video", vid)

    cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()