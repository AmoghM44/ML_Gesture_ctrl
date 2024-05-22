import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 4
exit_key = ord('e')  # ASCII value for 'e' key for exiting
scroll_speed = 10  # Adjust scroll speed as needed
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x3, y3 = lmList[16][1:]  # For ring finger
        x4, y4 = lmList[20][1:]  # For pinky finger

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        # 4. All four fingers are up: Scrolling Down Mode
        if all(fingers):
            # Move mouse for scrolling down
            pyautogui.scroll(scroll_speed)

            cv2.putText(img, "Scrolling Down", (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        # 5. Index, Middle, and Ring fingers are up: Scrolling Up Mode
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
            # Calculate average y-coordinate of fingers
            y_avg = (y1 + y2 + y3) // 3

            # Move mouse for scrolling up
            pyautogui.scroll(-scroll_speed)

            cv2.putText(img, "Scrolling Up", (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        # 6. Only Index Finger : Moving Mode
        elif fingers[1] == 1 and fingers[2] == 0:
            # Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move Mouse
            pyautogui.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 7. Both Index and middle fingers are up : Clicking Mode
        elif fingers[1] == 1 and fingers[2] == 1:
            # Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # Check if distance short for left-click, or longer for right-click
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
            elif length > 80:
                pyautogui.rightClick()

    # 8. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 9. Display
    cv2.imshow("Image", img)
    pressed = cv2.waitKey(1)
    if pressed == ord('q') or pressed == exit_key:
        break

cv2.destroyAllWindows()
