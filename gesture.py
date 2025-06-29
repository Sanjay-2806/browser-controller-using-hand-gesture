import cv2 as cv
import mediapipe as mp
import pyautogui
import time


mp_hands=mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
 
hands=mp_hands.Hands(max_num_hands=1)


def get(hand_landmarks):
    tip=[4,8,12,16,20]
    fingers=[]

    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in range(1,5):
        if hand_landmarks.landmark[tip[i]].y < hand_landmarks.landmark[tip[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

cap=cv.VideoCapture(0)
print("show ur hand to swtich the tab")

pt=0
gcd=1.5


while True:
    ret,frame=cap.read()
    if not ret:
        break
    frame=cv.flip(frame,1)
    rgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results=hands.process(rgb)

    if results.multi_hand_landmarks:
        hand_landmarks=results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

        fingers=get(hand_landmarks)
        t=sum(fingers)

        currenttime=time.time()
        if currenttime - pt > gcd:
            if fingers == [0,1,1,0,0]:
                print("Next tab")
                pyautogui.keyDown('ctrl')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')
                pt=currenttime
            elif fingers==[0,1,0,0,0]:
                print("prev tab")
                pyautogui.keyDown('ctrl')
                pyautogui.keyDown('shift')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')
                pyautogui.keyUp('shift')
                pt=currenttime
            elif fingers==[0,0,0,0,0]:
                print("zooming in")
                pyautogui.hotkey('command', '+')
                pt=currenttime
            elif fingers==[1,1,1,1,1]:
                print("zoom out")
                pyautogui.hotkey('command','-')
                pt=currenttime
            elif fingers==[0,1,1,1,0]:
                print("new tab")
                pyautogui.hotkey('command','n')
                pt=currenttime
            elif fingers==[0,0,0,0,1]:
                print("close the new tab")
                pyautogui.hotkey('command','w')
                pt=currenttime
            elif fingers==[0,1,0,0,1]:
                print("pause the vid")
                pyautogui.press('space')
                pt=currenttime
            elif fingers==[1,0,0,0,0]:
                print("full screen")
                pyautogui.press('f')
                pt=currenttime
            elif fingers==[1,1,1,0,0]:
                print("screenshot")
                pyautogui.hotkey('command','shift','3')
                pt=currenttime
            elif fingers==[0,0,1,0,0]:
                print("private browse")
                pyautogui.hotkey('command','shift','n')
                pt=currenttime
            
    cv.imshow('gesture tab changing',frame)
    if cv.waitKey(2) & 0xFF==ord('q'):
        break

cap.release()
cv.destroyAllWindows()