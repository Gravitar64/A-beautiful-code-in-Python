from pygamezero import *

WIDTH = HEIGHT = 500

gameState = 0
blocks = []
qbert = Actor('qbert2', center=(250, 80))
qbert.movex = qbert.movey = qbert.frame = count = 0;
bounce = [-6,-4,-2,-1,0,0,0,0,0,0,0,0,1,2,4,6]

for r in range(0, 7):
    for b in range(0, 7-r):
        blocks.append(Actor('block0', center=(60+(b*64)+(r*32), 400-(r*48))))

def draw():
    screen.blit("background", (0, 0))
    for b in range(0, 28): blocks[b].draw()
    if gameState == 0 or (gameState == 1 and count%4 == 0): qbert.draw()
    if gameState == 2 : screen.draw.text("YOU CLEARED THE LEVEL!", center = (250, 250), owidth=0.5, ocolor=(255,255,255), color=(255,0,255) , fontsize=40)
    
def update():
    global gameState, count
    if gameState == 0:
        if qbert.movex == 0 and qbert.movey == 0 :
            if keyboard.left: jump(32,48,3)
            if keyboard.right: jump(-32,-48,1)
            if keyboard.up: jump(-32,48,0)
            if keyboard.down: jump(32,-48,2)
        if qbert.movex != 0 : move()
    count += 1;
    
def move():
    if qbert.movex > 0 :
        qbert.x -=2
        qbert.movex -=2
    if qbert.movex < 0 :
        qbert.x +=2
        qbert.movex +=2
    if qbert.movey > 0 :
        qbert.y -=3 - bounce[qbert.frame]
        qbert.movey -=3
    if qbert.movey < 0 :
        qbert.y +=3 + bounce[qbert.frame]
        qbert.movey +=3
    qbert.frame +=1
    if qbert.movex == 0 :
        checkBlock()

def checkBlock():
    global gameState
    block = -1
    curBlock = 0
    numSelected = 0
    for r in range(0, 7):
        for b in range(0, 7-r):
            x = 60+(b*64)+(r*32) -2
            y = 400-(r*48) -32
            if qbert.x == x and qbert.y == y :
                block = curBlock
                blocks[block].image = "block1"
            curBlock +=1
    if block == -1 : gameState = 1
    for b in range(0, 28):
        if blocks[b].image == "block1" : numSelected += 1
    if numSelected == 28 : gameState = 2

def jump(x,y,d):
    qbert.movex = x
    qbert.movey = y
    qbert.image = "qbert"+str(d)
    qbert.frame = 0