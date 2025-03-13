import csv

FPS = 60
SCALER = 3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 5
ARROW_SPEED = 10
OFFSET = 12
WEAPON_SCALER = 1.5
ITEM_SCALER = 2.5
POTION_SCALER = 2
TOP_PANNEL = (50,50,50)
TILE_SIZE = 16 * ITEM_SCALER #fixeed this
TILE_RANGE = 18
ROWS = 150
COLS = 150
LEVEL = 1

MAP = []
for row in range(ROWS):
    r = [-1] * COLS
    MAP.append(r)

with open(f"levels/level{LEVEL}_data.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            MAP[x][y] = int(tile)

            



RED = (255,0,0)
WHITE = (255,255,255)
BG = (40,25,25)

SCROLL_THRESH = 200

