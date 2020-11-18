import random
import pyautogui
from pygame import gfxdraw
import pygame
from GameEngine.GameManager import *
from mss import mss
import numpy as np

WHITE = 255, 255, 255
BLACK = 0, 0, 0

# RGB

RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

# Simple colors

YELLOW = 255, 255, 0
PURPLE = 255, 0, 255
LIGHT_BLUE = 0, 255, 255
LIME = 19, 255, 0
DARK_GREEN = 0, 128, 0
VIOLET = 238, 130, 238
INDIGO = 75, 0, 130
BROWN = 139, 69, 19
DARK_BLUE = 0, 0, 128
AQUA = 0, 128, 128
GREY = 128, 128, 128
LIGHT_GREY = 211, 211, 211
OLIVE = 128, 128, 0


def GetRandomColor(step=1):
    r = random.randint(0, 255)
    r -= r % step
    g = random.randint(0, 255)
    g -= g % step
    b = random.randint(0, 255)
    b -= b % step
    return r, g, b


ALL = 3
B = 0
G = 1
R = 2


def ChangeColor( color, G=5, mode=ALL):
    r, g, b = color
    r1 = random.randint(-G, G)
    r += r1
    g1 = random.randint(-G, G)
    g += g1
    b1 = random.randint(-G, G)
    b += b1

    def calc(n):
        return 255 - (255 - (n ** 2) ** 0.5)

    if mode == ALL:
        r1 = calc(r1)
        g1 = calc(g1)
        b1 = calc(b1)
    elif mode == R:
        r1 = calc(r1)
    elif mode == G:
        g1 = calc(g1)
    elif mode == B:
        b1 = calc(b1)

    print(r1, g1, b1)
    print(r, g, b)
    return r1, g1, b1

def GetColorFromScreen(x, y):
    # Проба цвета с координат
    m = mss()
    monitor = {
        "left": x,
        "top": y,
        "width": 1,
        "height": 1,
    }
    # Получаем пиксель с экрана монитора
    img = m.grab(monitor)

    # Преобразуем этот пиксель в матрицу
    img_arr = np.array(img)
    item = img_arr[0][0]
    r = item[2]
    g = item[1]
    b = item[0]

    return([r, g, b])