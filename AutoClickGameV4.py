from PIL import Image, ImageGrab
import cv2
import numpy as np
import pyautogui as auto
import random
import time
import os
import threading
import concurrent.futures

#STATIC VARIABLE
#Global
GAME_COORDINATE = [0, 0, 2559, 1079]

multiplyer = 0.95
os.chdir('V3')
#Enemy
ENEMY_LIST = ['Boss', 'Siren1', 'Siren2', 'siren3', '3SEnemy', '2SEnemy']
THRESHOLD = [0.76, 0.65, 0.78]
INDEXS = {0:0, 1:1, 2:1, 3:1, 4:2, 5:2, 6:2}
COORDINATE = [(0, 0, 0, 0), (20, 170, -10, 30), (40, 70, 100, 100), (0, 0, 0, 0)]
#Buttons
BUTTON_ENTER = ['Stage', 'Go1', 'Go2']
BUTTON_CONTINUE = ['Continue1', 'Continue2', 'Elite', 'Confirm']
BUTTON_FLEET = ['Retreat', 'ConfirmC']
BUTTON_SPECIAL = ['Disconnect', 'Mission']
#Mix (To Find Location)
LOCATION_REFERENCE_LIST = ['Disconnect', 'Mission', 'Stage', 'Go1', 'Go2', 'Retreat', 'InBattle', 'Continue1', 'Continue2', 'Elite', 'Confirm']
LOCATION_TRANSLATE = {0:0, 1:0, 2:1, 3:1, 4:1, 5:2, 6:3, 7:4, 8:4, 9:4, 10:4}
#                               0       1       2       3           4              5            6       7           8             9         10
#0-1, 2-4, 5, 6, 7-10
# 0    1   2  3     4

#Pyautogui Failsafe
auto.FAILSAFE = False

#Variable
Siren_Kill = 0
KILL_SWITCH = False

#Variable Settings
Total_Siren = 2

#Enemy Only
def find_enemy():
    start = time.perf_counter()
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(find_coor, ENEMY_LIST)
        for i, pt in enumerate(results):
            if pt:
                size = COORDINATE[INDEXS[i]]
                tem = cv2.imread(f'Enemy/{ENEMY_LIST[i]}.png')
                h, w, _ = tem.shape
                if pt:
                    cv2.rectangle(img, (pt[0] + size[0], pt[1] + size[1]), (pt[0] + size[2] + w, pt[1] + size[3] + h),(0, 255, 0), 3)
                print(f'{ENEMY_LIST[i]} - {pt}')
    end = time.perf_counter()
    print(f"{end - start}")
    img = cv2.resize(img, (int(img.shape[1] * 0.8), int(img.shape[0] * 0.8)), interpolation=cv2.INTER_AREA)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_coor(enemy):
    tem = cv2.imread(f'Enemy/{enemy}.png')
    index = INDEXS[ENEMY_LIST.index(enemy)]
    for i in range(3):
        img = ImageGrab.grab(bbox=(GAME_COORDINATE))
        img = np.asarray(img)[:, :, ::-1].copy()
        stem = cv2.resize(tem, (int(tem.shape[1]*1.1), int(tem.shape[0]*1.1)), interpolation=cv2.INTER_AREA)
        for k in range(5):
            result = cv2.matchTemplate(img, stem, cv2.TM_CCOEFF_NORMED)
            threshold = THRESHOLD[index]
            loc = np.where(result>= threshold)
            for pt in zip(*loc[::-1]):
                if pt:
                    return pt
            stem = cv2.resize(stem, (int(stem.shape[1]*multiplyer), int(stem.shape[0]*multiplyer)), interpolation=cv2.INTER_AREA)


#Buttons Untilities
def button_enter():
    for button in BUTTON_ENTER:
        tem = cv2.imread(f'Button Enter/{button}.png')
        pt = find_button(tem)
        if pt:
            random_click(pt, tem, 3)
        random_time(1, 0.2)
    random_time(1, 0.5)

def button_continue():
    for button in BUTTON_CONTINUE:
        tem = cv2.imread(f'Button Continue/{button}.png')
        pt = find_button(tem)
        if pt:
            random_click(pt, tem, 3)
            index = BUTTON_CONTINUE.index(button)
            if index is not 0:
                random_time(0.8, 0.4)
            random_time(0.7, 0.5)
    random_time(2, 1)

def button_switch():
    tem = cv2.imread('Button Fleet/Switch.png')
    pt = find_button(tem)
    if pt:
        random_click(pt, tem, 3)
    random_time(0.5, 0.3)

def button_retreat():
    for button in BUTTON_FLEET:
        tem = cv2.imread(f'Button Fleet/{button}.png')
        pt = find_button(tem)
        if pt:
            random_click(pt, tem, 3)
        random_time(0.7, 0.4)
    random_time(0.4, 0.4)

def button_special():
    for button in BUTTON_SPECIAL:
        tem = cv2.imread(f'Button Special/{button}.png')
        pt = find_button(tem)
        if pt:
            random_click(pt, tem, 3)
            break
    random_time(0.8, 0.5)

def find_button(tem):
    for i in range(2):
        img = ImageGrab.grab(bbox=(GAME_COORDINATE))
        img = np.asarray(img)[:, :, ::-1].copy()
        stem = cv2.resize(tem, (int(tem.shape[1]*1.0), int(tem.shape[0]*1.0)), interpolation=cv2.INTER_AREA)

        for k in range(7):
            result = cv2.matchTemplate(img, stem, cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(result>= threshold)
            for pt in zip(*loc[::-1]):
                if pt:
                    #print(pt)
                    return pt
            stem = cv2.resize(stem, (int(stem.shape[1]*multiplyer), int(stem.shape[0]*multiplyer)), interpolation=cv2.INTER_AREA)

def move():
    x = 1734 + random.randint(0, 626)
    y = 711 + random.randint(0, 100)
    auto.moveTo(x, y)
    time.sleep(0.5)
    x = 617 + random.randint(0, 259)
    y = 170 + random.randint(0, 224)
    auto.dragTo(x, y, duration=0.2)
    random_time(0.6, 0.3)

def moveup():
    x = 820 + random.randint(0, 611)
    y = 465 + random.randint(0, 218)
    auto.moveTo(x, y)
    random_time(0.5, 0.3)
    auto.scroll(-11)
    random_time(0.8, 0.5)

#Where am I
def where_am_I():
    # Screen Shot
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()

    # Search
    for reference in LOCATION_REFERENCE_LIST:
        stem = cv2.imread(f'Location Reference/{reference}.png')
        for i in range(2):
            result = cv2.matchTemplate(img, stem, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(result >= threshold)
            for pt in zip(*loc[::-1]):
                if pt:
                    #print(reference)
                    return LOCATION_TRANSLATE[LOCATION_REFERENCE_LIST.index(reference)]
            stem = cv2.resize(stem, (int(stem.shape[1]*multiplyer), int(stem.shape[0]*multiplyer)), interpolation=cv2.INTER_AREA)
    return -1

#All Utilities
def random_click(coor, tem, index):
    correction = COORDINATE[index]
    h, w, _ = tem.shape
    x = coor[0] + correction[0] + random.randint(0, (w + correction[2] - correction[0])) + GAME_COORDINATE[0]
    y = coor[1] + correction[1] + random.randint(0, (h + correction[3] - correction[1])) + GAME_COORDINATE[1]
    if x > 1620 and y > 935 and index is not 3:
        moveup()
        return -1
    auto.click(x, y)

def random_time(min, delay):
    t = round((random.uniform(0, delay) + min), 3)
    time.sleep(t)

def kill():
    global KILL_SWITCH
    KILL_SWITCH = True

#Debug Utilities
def print_box(pt, tem, index):
    img = ImageGrab.grab(bbox=(GAME_COORDINATE))
    img = np.asarray(img)[:, :, ::-1].copy()
    size = COORDINATE[index]
    h, w, _ = tem.shape
    if pt:
        cv2.rectangle(img, (pt[0] + size[0], pt[1] + size[1]), (pt[0] + size[2] + w, pt[1] + size[3] + h), (0, 255, 0), 3)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_image(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#Main Program
def main_loop(times):
    global Siren_Kill, KILL_SWITCH
    for i in range(times):
        if KILL_SWITCH:
            break
        location = where_am_I()
        if location == 0:
            print('Might Have Some Issue here...')
            button_special()
        elif location == 1:
            print('Entering Battle')
            Siren_Kill = 0
            button_enter()
        elif location == 2:
            print('Searching Enemy:', end=' ')
            find_enemy()
            time.sleep(20)
        elif location == 3:
            print('In battle, wait 10 seconds')
            for i in range(10, 0, -1):
                print(f'{i}s  ', end = ' ')
                time.sleep(1)
            print()
        elif location == 4:
            print('Returning to Battle Field')
            button_continue()
        elif location == -1:
            print('We Experience Some Issue Here')
            time.sleep(5)

def init(times):
    global Siren_Kill, KILL_SWITCH
    Siren_Kill = 0
    KILL_SWITCH = False
    main_loop(times)

find_enemy()