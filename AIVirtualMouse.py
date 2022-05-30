import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import time

######################
wCam, hCam = 640, 480
frameR = 100     #Frame Reduction
smoothening = 7  #random value
######################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(2)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

# print(wScr, hScr)

while True:
    # Step1: Find the landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Step2: Get the tip of the index and middle finger
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Step3: Check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

      

        # Step8: Both Index and middle are up: Clicking Mode
        if fingers[0] == 1 and fingers[1] == 1:

            # Step9: Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Step10: Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[3], lineInfo[4]), 15, (0, 255, 0), cv2.FILLED)
                #autopy.mouse.click()
                #autopy.bitmap.capture_screen().save('/home/oleh/Зображення/screen.png')
                #autopy.key.scroll(10)  
                autopy.key.tap(autopy.key.Code.PAGE_DOWN)
            if length > 40:
                cv2.circle(img, (lineInfo[3], lineInfo[4]), 15, (0, 255, 0), cv2.FILLED)
                #autopy.mouse.click()
                #autopy.bitmap.capture_screen().save('/home/oleh/Зображення/screen.png')
                #autopy.key.scroll(10)  
                autopy.key.tap(autopy.key.Code.PAGE_UP)

    # Step11: Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (28, 58), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 8), 3)

    # Step12: Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)