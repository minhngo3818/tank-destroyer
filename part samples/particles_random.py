import pygame, random, math

def radians(degrees):
    return degrees*math.pi/180

class Particle:
    def __init__(self, x, y, radius, speed, angle, colour, surface):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.radius = 3
        self.surface = surface
        self.colour = colour
        self.rect = pygame.draw.circle(surface,(255,255,0),
                           (int(round(x,0)),
                            int(round(y,0))),
                           self.radius)
    def move(self):
        """ Update speed and position based on speed, angle """
        # for constant change in position values.
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        # pygame.rect likes int arguments for x and y
        self.rect.x = int(round(self.x))
        self.rect.y = int(round(self.y))

    def draw(self):
        """ Draw the particle on screen"""
        pygame.draw.circle(self.surface,self.colour,self.rect.center,self.radius)

    def bounce(self):
        """ Tests whether a particle has hit the boundary of the environment """

        if self.x > self.surface.get_width() - self.radius: # right
            self.x = 2*(self.surface.get_width() - self.radius) - self.x
            self.angle = - self.angle

        elif self.x < self.radius: # left
            self.x = 2*self.radius - self.x
            self.angle = - self.angle            

        if self.y > self.surface.get_height() - self.radius: # bottom
            self.y = 2*(self.surface.get_height() - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius: # top
            self.y = 2*self.radius - self.y
            self.angle = math.pi - self.angle

def main():
    xmax = 640    #width of window
    ymax = 480     #height of window
    white = (255, 255, 255)
    black = (0,0,0)
    grey = (128,128,128)

    pygame.init()
    screen = pygame.display.set_mode((xmax,ymax))
    clock = pygame.time.Clock()

    particles = []

    for i in range(1000):
        if i % 2:
            colour = black
        else:
            colour = grey
        # for readability
        x = random.randint(0, xmax)
        y = random.randint(0, ymax)
        speed = random.randint(0,20)*0.1
        angle = random.randint(0,360)
        radius = 3
        particles.append( Particle(x,y, radius, speed, angle, colour, screen)) 

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    break
        if done:
            break

        screen.fill(white)
        for p in particles:
            p.move()
            p.bounce()
            p.draw()

        clock.tick(40)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()