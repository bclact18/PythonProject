from PIL import Image, ImageGrab
import cv2
import numpy as np
import pyautogui as auto
import random
import time

#Global Variable
GAME_COORDINATE = [0, 0, 2559, 1079]

#Enemy
ENEMY = cv2.imread("Enemy/2SEnemy.png")
BOSS = cv2.imread("Enemy/Boss.png")

#Buttons
BATTLE = cv2.imread("Testing/Battle.png")
CONTINUE1 = cv2.imread("Testing/Continue1.png")
CONTINUE2 = cv2.imread("Testing/Continue2.png")
GO1 = cv2.imread("Testing/Go1.png")
GO2 = cv2.imread("Testing/Go2.png")
CONFIRM = cv2.imread("Testing/Confirm.png")
STAGE = cv2.imread("Testing/Stage.png")
SWITCH = cv2.imread("Testing/Switch.png")

#Reference
CF = cv2.imread("Testing/CF.png")

#select random coordinate
def rngCoord(x1, w, y1, h):
    #(x1, width, y1, height)
    x = x1 + random.randint(0, w)
    y = y1 + random.randint(0, h)
    return (x, y)

#select random time
def rngTime(t1, t2):
    time.sleep(t1 + random.uniform(0, t2))


def buttonPressing(comp, t1, t2):
    for i in range(15):
        # Screen Shot
        img = ImageGrab.grab(bbox=(GAME_COORDINATE))
        img = np.asarray(img)[:, :, ::-1].copy()

        # Search
        result = cv2.matchTemplate(img, comp, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = 0
        loc = np.where(result >= threshold)
        try:
            h, w, _ = comp.shape
            coor = rngCoord(loc[1][0], w, loc[0][0], h)
        except:
            print("Not there yet :P {}")
            rngTime(t1, t2)
            continue
        if coor[0] > GAME_COORDINATE[0] and coor[0] < GAME_COORDINATE[2] and coor[1] > GAME_COORDINATE[1] and coor[1] < GAME_COORDINATE[3]:
            auto.click(coor)
            break

def screen_center():
    #Reference is (580 + 20, 845 + 20)
    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()
    CFResult = cv2.matchTemplate(img, CF, cv2.TM_CCOEFF_NORMED)
    CF_coor = np.unravel_index(CFResult.argmax(), CFResult.shape)
    auto.moveTo(CF_coor[1] + 20, CF_coor[0] + 20)
    auto.dragTo(507, 495,  0.3, button='left')

#Attacking Enemy
def searchStuff(comp, index):
    for i in range(10):
        # Screen Shot
        img = ImageGrab.grab(bbox=(GAME_COORDINATE))
        img = np.asarray(img)[:, :, ::-1].copy()

        #Search
        result = cv2.matchTemplate(img, comp, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = 0
        loc = np.where(result >= threshold)

        try:
            #Clicking
            if index == 0: #Mob
                h, w = 90, 150
                coor = rngCoord(loc[1][0]+30, w, loc[0][0] + 90, h)
                auto.click(coor)
                break
            if index == 1: #Boss
                h, w = 100, 120
                coor = rngCoord(loc[1][0], w, loc[0][0], h)
                auto.click(coor)
                break
        except:
            print(f"Enemy no show :V {i}")
            screen_center()
            rngTime(1, 1)
    buttonPressing(BATTLE, 2, 2)
    rngTime(90, 20)
    buttonPressing(CONTINUE1, 1.5, 1)
    buttonPressing(CONTINUE2, 1.5, 1)
    buttonPressing(CONFIRM, 1.5, 1)
    rngTime(5, 1)


#Testing purpose only
def printOutImage(img, loc):
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, (pt[0] + 30, pt[1] + 90), (pt[0] + 150, pt[1] + 140), (0, 255, 0), 2)
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#main loop
while True:
    if auto.position()[0] < 0 or auto.position()[0] > 2560:
        print("Program Stoped")
        break
    buttonPressing(STAGE, 0.5, 0.5)
    buttonPressing(GO1, 0.5, 0.5)
    rngTime(1.5,1)
    buttonPressing(GO2, 0.5, 0.5)
    rngTime(3, 1)
    screen_center()
    for i in range(5):
        rngTime(5, 1)
        searchStuff(ENEMY, 0)

    buttonPressing(SWITCH, 1, 1)
    screen_center()
    searchStuff(BOSS, 1)
    rngTime(3, 2)
