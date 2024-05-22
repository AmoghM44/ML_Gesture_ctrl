from time import sleep
import cv2
import mediapipe as mp
import pyautogui as p
import numpy as np

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands()
    
def Handspos(img,test=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    pos=[]
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                x,y,c=img.shape
                currentx,currenty=int(lm.x*x),int(lm.y*y)
                pos.append([currentx,currenty])
                if test:
                    mpDraw.draw_landmarks(img, handLms)

        return pos

def mediacontroller(pos):
    if pos[8][1]<pos[7][1] and pos[12][1]>pos[11][1] and pos[16][1]>pos[15][1] and pos[20][1]>pos[19][1]:
        p.press("space")
        sleep(1)
    if pos[8][1]<pos[7][1] and pos[12][1]<pos[11][1] and pos[16][1]>pos[15][1] and pos[20][1]>pos[19][1]:
        p.press("volumeup")  
    if pos[8][1]<pos[7][1] and pos[12][1]<pos[11][1] and pos[16][1]<pos[15][1] and pos[20][1]>pos[19][1]:
        p.press("volumedown")  
    if pos[8][1]<pos[7][1] and pos[12][1]<pos[11][1] and pos[16][1]<pos[15][1] and pos[20][1]<pos[19][1]:
        p.press("right")
    if pos[8][1]>pos[7][1] and pos[12][1]>pos[11][1] and pos[16][1]>pos[15][1] and pos[20][1]<pos[19][1]:
        p.press("left")  

def main():
    Frame=cv2.VideoCapture(0)
    while True:
        t,img=Frame.read()
        pos=Handspos(img)
        
        if pos!=None:
            pos=np.array(pos)
            mediacontroller(pos)
        
        cv2.imshow("Detector",img)
        if cv2.waitKey(10) & 0xff==ord('e'):  # Check for exit key ('e')
            break
    cv2.destroyAllWindows()

if __name__ =="__main__":
    main()
