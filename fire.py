# generate random floating point values
from random import seed
from random import random
from random import randint
import math
import time
# seed random number gene

COL = 100
ROW = 100
ALIVE = "GREEN"
BURNING = "RED"
DEAD = "BROWN"
TICK_INTERVAL = 3
#CV100
rain = randint(1, 2)
humidity = randint(3, 5)
wind = randint(3, 4)
light = randint(6, 8)


def calcOut():
    if rain == 2:
        return math.ceil(wind * rain / light * 5)
    else:
        return math.ceil(wind * humidity / light / 2 * 5)

p_out = calcOut()
p_spread = p_out * (10 / light);

def setFire():
    forest = []
    for i in range(COL):
        row = []
        for j in range(ROW):
            row.append(ALIVE)
        forest.append(row)
    forest[50][50] = BURNING
    return forest


def render(cells, arr):
    i = 0
    j = 0
    for row in cells:
        for cell in row:
            v = arr[i][j]
            if v == ALIVE:
                cell.set_background_color(0, 255, 0)
            elif v == BURNING:
                cell.set_background_color(255, 0, 0)
            else:
                cell.set_background_color(101, 67, 33)
            j += 1
        i += 1
        j = 0
    return i, j


def process_forest_state(forest):
    newForest = forest.copy()
    tmpForest = forest.copy()
    fire = 0
    fire_delta = 0
    for i in range(len(tmpForest)):
        for j in range(len(tmpForest[i])):
            if tmpForest[i][j] != BURNING:
                continue
            fire+=1
            if random() <= p_out:
                #DIES
                newForest[i][j] = DEAD
                continue
            if random() <= p_spread:
                if i > 0 and newForest[i-1][j] == ALIVE:
                    fire_delta+=1
                    newForest[i-1][j] = BURNING
                if j > 0 and newForest[i][j-1] == ALIVE:
                    fire_delta+=1
                    newForest[i][j-1] = BURNING
                if i < COL-1 and  newForest[i+1][j] == ALIVE:
                    fire_delta+=1
                    newForest[i+1][j] = BURNING
                if j < ROW-1 and newForest[i][j+1] == ALIVE:
                    fire_delta+=1
                    newForest[i][j+1] = BURNING
    return newForest, fire, fire_delta

# start the program
def start(collect_metrics = False):
    forest = setFire()
    render(A1:CV100, forest)
    time.sleep(TICK_INTERVAL)
    while True:
        forest, fire, fire_delta = process_forest_state(forest)
        if collect_metrics:
            print("Metrics: Fire " + str(fire) + " Delta: " + str(fire_delta))
        render(A1:CV100, forest)
        if fire == 0:
            return
        time.sleep(TICK_INTERVAL)