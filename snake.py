import math
import random
import pygame
import random


class cube(object):
    rows, w = 20, 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx, self.dirny = dirnx, dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i, j = self.pos[0], self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.body[0].dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] and self.body[0].dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] and self.body[0].dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] and self.body[0].dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]

            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                if c.dirnx == 1 and c.pos[0] >= c.rows - 1: c.pos = (-1, c.pos[1])
                if c.dirny == 1 and c.pos[1] >= c.rows - 1: c.pos = (c.pos[0], -1)
                if c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.turns = {}

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx, self.body[-1].dirny = dx, dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeGap = w // rows
    x, y = 0, 0

    for i in range(rows):
        x, y = x + sizeGap, y + sizeGap

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, food
    surface.fill((0, 0, 0))
    s.draw(surface)
    food.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnake(item):
    global rows
    positions = item.body

    while True:
        x, y = random.randrange(rows), random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y

def main():
    global width, rows, s, food
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    oneX, oneY = random.randint(0,19), random.randint(0,19)
    s = snake((255, 0, 0), (oneX, oneY))
    food = cube(randomSnake(s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == food.pos:
            s.addCube()
            food = cube(randomSnake(s), color=(0, 255, 0))

        for c in s.body[1:]:
            if s.body[0].pos == c.pos:
                print("Score: ", len(s.body))
                s.reset((oneX, oneY))
                
                redrawWindow(win)
                
                while True:
                    decision = input('Play Again(Y/N): ')
                    if(len(decision)>1 or len(decision)==0):
                        continue
                    if(decision.upper()=='N'):  
                        flag = False
                    break;
        redrawWindow(win)            
        


main()
