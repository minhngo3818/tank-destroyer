import pygame,random
from pygame.locals import *

xmax = 1000    #width of window
ymax = 600     #height of window

class Particle():
    def __init__(self, startx, starty, col):
        self.x = startx
        self.y = random.randint(0, starty)
        self.col = col
        self.sx = startx
        self.sy = starty

    def move(self):
        if self.y < 0:
            self.x=self.sx
            self.y=self.sy

        else:
            self.y-=1

        self.x+=random.randint(-2, 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((xmax,ymax))
    white = (255, 255, 255)
    black = (0,0,0)
    grey = (128,128,128)

    clock=pygame.time.Clock()

    particles = []
    for part in range(300):
        if part % 2 > 0: col = black
        else: col = grey
        particles.append( Particle(515, 500, col) )

    exitflag = False
    while not exitflag:
        for event in pygame.event.get():
            if event.type == QUIT:
                exitflag = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exitflag = True

        screen.fill(white)
        for p in particles:
            p.move()
            pygame.draw.circle(screen, p.col, (p.x, p.y), 2)

        pygame.display.flip()
        clock.tick(50)
    pygame.quit()

if __name__ == "__main__":
    main()