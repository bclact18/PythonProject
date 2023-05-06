from PIL import Image, ImageGrab
import cv2
import numpy as np
import pyautogui as auto
import random
import time
import winsound

#Global Variable
GAME_COORDINATE = [0, 0, 2559, 1079]

#Enemy
ENEMY1 = cv2.imread("Enemy/1SEnemy.png")
ENEMY2 = cv2.imread("Enemy/2SEnemy.png")
ENEMY3 = cv2.imread("Enemy/3SEnemy.png")
SIREN1 = cv2.imread("Enemy/Siren1.png")
SIREN2 = cv2.imread("Enemy/Siren2.png")
SIREN3 = cv2.imread("Enemy/Siren3.png")
BOSS = cv2.imread("Enemy/Boss1.png")

#Buttons
BATTLE = cv2.imread("Testing/Battle.png")
CONTINUE1 = cv2.imread("Testing/Continue1.png")
CONTINUE2 = cv2.imread("Testing/Continue2.png")
GO1 = cv2.imread("Testing/Go1.png")
GO2 = cv2.imread("Testing/Go2.png")
CONFIRM = cv2.imread("Testing/Confirm.png")
STAGE = cv2.imread("Testing/Stage.png")
SWITCH = cv2.imread("Testing/Switch.png")
ELITE = cv2.imread("Testing/Elite.png")
CONFIRM_B = cv2.imread("Testing/ConfirmB.png")

#Reference
CF = cv2.imread("Testing/CF.png")
CFCoor = [[1832, 850], [1766, 363]]
CFNum = 0

SIRENS = [SIREN1, SIREN2, SIREN3]

#Image List
SEARCH_LIST = [STAGE, GO1, GO2, SWITCH, CONTINUE1, CONTINUE2, ELITE, CONFIRM, CONFIRM_B]
BUTTONS_A = [STAGE, GO1, GO2]
BUTTONS_B = [CONTINUE1, CONTINUE2, ELITE, CONFIRM, CONFIRM_B]
ENEMY_LIST = [BOSS, SIREN1, SIREN2, SIREN3, ENEMY3, ENEMY2, ENEMY1]
ENEMY_NAME = ['BOSS', 'SIREN1', 'SIREN2', 'SIREN3', 'ENEMY3', 'ENEMY2', 'ENEMY1']
#0 = Main Screen, 1 = Battle field, 2 = End Battle Screen
AT_SCREEN = 0
#Time in Battle
BATTLE_DURATION = [40, 55, 55, 55, 90, 80, 60]

#select random coordinate
def rngCoord(x1, w, y1, h):
    #(x1, width, y1, height)
    x = x1 + random.randint(0, w)
    y = y1 + random.randint(0, h)
    return x, y

#select random time
def rngTime(t1, t2):
    t = t1 + random.randint(0, t2)
    for i in range(t, 0, -1):
        time.sleep(1)
        print(f"Count Down: {i}s")
    print('Done\n--------------------------------------------------')

#Entering Battle Button
def buttonPressingA():
    for i in range(5):
        # Screen Shot
        img = ImageGrab.grab(bbox=(GAME_COORDINATE))
        img = np.asarray(img)[:, :, ::-1].copy()
        for j in range(len(BUTTONS_A)):
            # Search
            result = cv2.matchTemplate(img, BUTTONS_A[j], cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(result >= threshold)
            try:
                h, w, _ = BUTTONS_A[j].shape
                coor = rngCoord(loc[1][0], w, loc[0][0], h)
                auto.click(coor)
                print(j)
                break
            except:
                if j == len(BUTTONS_A) - 1:
                    return -1
        time.sleep(0.5)

#End Battle Button
def buttonPressingB():
    for i in range(7):
        # Screen Shot
        img = ImageGrab.grab(bbox=(GAME_COORDINATE))
        img = np.asarray(img)[:, :, ::-1].copy()
        for j in range(len(BUTTONS_B)):
            # Search
            result = cv2.matchTemplate(img, BUTTONS_B[j], cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(result >= threshold)
            try:
                h, w, _ = BUTTONS_B[j].shape
                coor = rngCoord(loc[1][0], w, loc[0][0], h)
                auto.click(coor)
                if j == 2:
                    rngTime(2, 1)
                break
            except:
                if j == len(BUTTONS_B) - 1:
                    return -1
        time.sleep(1.2)

#Centering Screen
def screen_center(num):
    #Reference is (580 + 20, 845 + 20)
    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()
    CFResult = cv2.matchTemplate(img, CF, cv2.TM_CCOEFF_NORMED)
    CF_coor = np.unravel_index(CFResult.argmax(), CFResult.shape)
    auto.moveTo(CF_coor[1] + 20, CF_coor[0] + 20)
    auto.dragTo(CFCoor[num][0], CFCoor[num][1],  0.3, button='left')
    print("Screen Centered")

#Attacking Enemy
def searchEnemy():

    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()

    #Search
    for i in range(len(ENEMY_LIST)):
        result = cv2.matchTemplate(img, ENEMY_LIST[i], cv2.TM_CCOEFF_NORMED)
        threshold = 0.76
        loc = np.where(result >= threshold)
        coor = 0
        try:
            #Clicking
            if i == 4 or i == 5 or i == 6: #Mob
                h, w = 50, 140
                coor = rngCoord(loc[1][0] + 30, w, loc[0][0] + 90, h)
                auto.click(coor)
            if i == 1 or i == 2 or i == 3: #Siren
                h, w, _ = ENEMY_LIST[i].shape
                coor = rngCoord(loc[1][0], w, loc[0][0] + h - 30, 40)
                auto.click(coor)

            if i == 0: #BOSS
                h, w, _ = BOSS.shape
                coor = rngCoord(loc[1][0], w, loc[0][0], h)
                print("boss")
                switch()
                rngTime(1, 1)
                screen_center(0)
                rngTime(1, 1)

                result = cv2.matchTemplate(img, BOSS, cv2.TM_CCOEFF_NORMED)
                threshold = 0.76
                loc = np.where(result >= threshold)
                print("Coor reset")

                coor = rngCoord(loc[1][0], w, loc[0][0] + 20, h)
                auto.click(coor)
            print(f"Enemy Type<{ENEMY_NAME[i]}> Coordinate {coor}")
            return i
        except:
            continue
    return -1

#Find Current Location
def whereAmI():
    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()

    # Search
    for i in range(len(SEARCH_LIST)):
        result = cv2.matchTemplate(img, SEARCH_LIST[i], cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        try:
            h, w, _ = SEARCH_LIST[i].shape
            coor = rngCoord(loc[1][0], w, loc[0][0], h)
            if i <= 2:
                return 1
            if i == 3:
                return 2
            if i <= 8:
                return 3
            print(f"TESTING {i}")
        except:
            continue

#Switch
def switch():
    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()

    result = cv2.matchTemplate(img, SWITCH, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75
    loc = np.where(result >= threshold)
    h, w, _ = SWITCH.shape
    coor = rngCoord(loc[1][0], w, loc[0][0], h)
    auto.click(coor)
    print("Switch")

#esting purpose only
def printOutImage():
    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()

    # Search
    for i in range(len(ENEMY_LIST)):
        result = cv2.matchTemplate(img, ENEMY_LIST[i], cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            h, w, _ = ENEMY_LIST[i].shape
            print(f"{h} {w} {i}")
            cv2.rectangle(img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#Main Loop
repeat = 0
while True:
    AT_SCREEN = whereAmI()
    repeat += 1

    print(f"{repeat} - {AT_SCREEN}")

    error_code = 0
    if_enter_battle = 0

    if auto.position()[0] < 0 or auto.position()[0] > 2560:
        print("Program Stoped")
        break

    #Search for battle button
    if AT_SCREEN == None:
        winsound.Beep(1000, 500)
    if AT_SCREEN == 1:
        CFNum = 0
        buttonPressingA()
        rngTime(2, 1)
    if AT_SCREEN == 2:
        while AT_SCREEN == 2:
            error_code = searchEnemy()
            if error_code is not -1:
                print(f"Enemy Search Code: {ENEMY_NAME[error_code]} (-1 = Can't find Enemy')")
            else:
                print(f"Enemy Search Code: {error_code} (-1 = Can't find Enemy')")
                screen_center(CFNum)
                CFNum = (CFNum + 1)%2
            if error_code != -1:
                time.sleep(7)
            else:
                time.sleep(2)
            AT_SCREEN = whereAmI()

        rngTime(BATTLE_DURATION[error_code], 10)

    if AT_SCREEN == 3:
        buttonPressingB()
        rngTime(2, 1)
