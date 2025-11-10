# TODO Dodadeni prepreki i nivna logika
import random, pygame, sys
from pygame.locals import *

FPS = 8
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0
assert WINDOWHEIGHT % CELLSIZE == 0

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

# Dodadena e globalna lista za prepreki
OBSTACLES = []


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy with Obstacles')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    global OBSTACLES

    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [
        {'x': startx, 'y': starty},
        {'x': startx - 1, 'y': starty},
        {'x': startx - 2, 'y': starty}
    ]
    direction = RIGHT

    OBSTACLES = generateObstacles(wormCoords)

    apple = getRandomAppleLocation(wormCoords)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    if not willHitObstacle(LEFT, wormCoords[HEAD]):
                        direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    if not willHitObstacle(RIGHT, wormCoords[HEAD]):
                        direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    if not willHitObstacle(UP, wormCoords[HEAD]):
                        direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    if not willHitObstacle(DOWN, wormCoords[HEAD]):
                        direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        newHead = getNextHead(direction, wormCoords[HEAD])


        if (newHead['x'] < 0 or newHead['x'] >= CELLWIDTH or
                newHead['y'] < 0 or newHead['y'] >= CELLHEIGHT):
            return


        for body in wormCoords:
            if body['x'] == newHead['x'] and body['y'] == newHead['y']:
                return

        # Sudir so prepreka
        if isObstacleCell(newHead['x'], newHead['y']):
            return


        if newHead['x'] == apple['x'] and newHead['y'] == apple['y']:
            wormCoords.insert(0, newHead)
            apple = getRandomAppleLocation(wormCoords)
        else:
            wormCoords.insert(0, newHead)
            del wormCoords[-1]

        drawFrame(wormCoords, apple)


# Predvremena proverka na colizija
def willHitObstacle(direction, headCoord):
    nextHead = getNextHead(direction, headCoord)
    return isObstacleCell(nextHead['x'], nextHead['y'])


# Predvremena proverka za glavata
def getNextHead(direction, headCoord):
    if direction == UP:
        return {'x': headCoord['x'], 'y': headCoord['y'] - 1}
    elif direction == DOWN:
        return {'x': headCoord['x'], 'y': headCoord['y'] + 1}
    elif direction == LEFT:
        return {'x': headCoord['x'] - 1, 'y': headCoord['y']}
    elif direction == RIGHT:
        return {'x': headCoord['x'] + 1, 'y': headCoord['y']}
    return dict(headCoord)


# Generira prepreki od 1 do 5% od vkupni kelii
def generateObstacles(wormCoords):
    total_cells = CELLWIDTH * CELLHEIGHT
    max_obstacles = max(1, int(total_cells * 0.05))
    num_obstacles = random.randint(1, max_obstacles)

    obstacles = []
    forbidden = set((seg['x'], seg['y']) for seg in wormCoords)

    while len(obstacles) < num_obstacles:
        x = random.randint(0, CELLWIDTH - 1)
        y = random.randint(0, CELLHEIGHT - 1)
        coord = (x, y)
        if coord in forbidden:
            continue
        if coord in [(o['x'], o['y']) for o in obstacles]:
            continue
        obstacles.append({'x': x, 'y': y})
    return obstacles


# Proverka na preklopuvacka kelija
def isObstacleCell(x, y):
    for obs in OBSTACLES:
        if obs['x'] == x and obs['y'] == y:
            return True
    return False


def getRandomAppleLocation(wormCoords):
    occupied = set((seg['x'], seg['y']) for seg in wormCoords)
    occupied.update((obs['x'], obs['y']) for obs in OBSTACLES)
    while True:
        x = random.randint(0, CELLWIDTH - 1)
        y = random.randint(0, CELLHEIGHT - 1)
        if (x, y) not in occupied:
            return {'x': x, 'y': y}


def drawFrame(wormCoords, apple):
    DISPLAYSURF.fill(BGCOLOR)
    drawGrid()
    drawObstacles(OBSTACLES)  # Da se generiraat prepreki
    drawWorm(wormCoords)
    drawApple(apple)
    drawScore(len(wormCoords) - 3)
    pygame.display.update()
    FPSCLOCK.tick(FPS)


# Gi crta preprekite
def drawObstacles(obstacles):
    for coord in obstacles:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGRAY, rect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 220, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def terminate():
    pygame.quit()
    sys.exit()


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)

        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3
        degrees2 += 7


def showGameOverScreen():

    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)

    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 80)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 100)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()

    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return


if __name__ == '__main__':
    main()
