# Name:          Farris Matar
# Date:          March 20, 2017
# Description:   Drawing a character (Meta Knight).

# Starting up Pygame.
from math import pi
import pygame
pygame.init()

# Setting up some variables for the screen and colours.
SIZE = (1280,750)
screen = pygame.display.set_mode(SIZE)
WHITE = (255,255,255)
RUBY_RED = (244,14,33)
GLOVE_WHITE = (226,226,226)
GLOVE_OUTLINE = (176,176,176)
DARK_OUTLINE = (166,166,166)
BLACK = (0,0,0)
WING_PURPLE = (91,89,122)
WING_OUTLINE = (37,33,91)
PURPLE = (75,20,107)
DARK_PURPLE = (45,11,66)
BACKGROUND = (42, 29, 51)
LIGHT_GRAY = (210, 213, 224)
LIGHT_BLUE = (78,220,252)
STEEL = (78,75,122)
DARK_BLUE = (1,28,150)
YELLOW = (232,224,18)
GOLD = (255,212,0)
SWORD_GOLD = (249,249,33)
LIGHT_SWORD_GOLD = (255,255,73)
screen.fill(BACKGROUND)
waitTime = 7500

# Creating a function for the superhero.
def drawHero(heroX,heroY):
    # Drawing the shoes.
    pygame.draw.ellipse(screen,PURPLE,pygame.Rect(heroX-90,heroY+85,60,110))
    pygame.draw.ellipse(screen,PURPLE,pygame.Rect(heroX+35,heroY+85,60,110))
    
    # Details for the shoes.
    pygame.draw.arc(screen,DARK_PURPLE,[heroX-88,heroY+145,61,25],0.5,3.2,3)
    pygame.draw.arc(screen,DARK_PURPLE,[heroX-89,heroY+145,61,25],0.5,3.2,3)
    pygame.draw.arc(screen,DARK_PURPLE,[heroX-90,heroY+145,61,25],0.5,3.2,3)
    pygame.draw.arc(screen,DARK_PURPLE,[heroX+36,heroY+145,61,25],0.5,3.2,3)
    pygame.draw.arc(screen,DARK_PURPLE,[heroX+37,heroY+145,61,25],0.5,3.2,3)
    pygame.draw.arc(screen,DARK_PURPLE,[heroX+38,heroY+145,61,25],0.5,3.2,3) 
    
    pygame.draw.line(screen,DARK_PURPLE,(heroX-62,heroY+194),(heroX-62,heroY+146),3)
    pygame.draw.line(screen,DARK_PURPLE,(heroX+64,heroY+194),(heroX+64,heroY+146),3)   
    
    # Drawing the shoulder plates and arms.
    # Right arm.
    pygame.draw.ellipse(screen,DARK_BLUE,pygame.Rect(heroX+120,heroY-80,65,105))
    
    # Right shoulder plates.
    pygame.draw.ellipse(screen,STEEL,pygame.Rect(heroX+29,heroY-160,180,160))
    pygame.draw.rect(screen,BACKGROUND,pygame.Rect(heroX+118,heroY-160,180,80))
    pygame.draw.rect(screen,BACKGROUND,pygame.Rect(heroX+16,heroY-160,95,160))
    pygame.draw.rect(screen,BACKGROUND,pygame.Rect(heroX+10,heroY-160,150,85))
    
    pygame.draw.ellipse(screen,STEEL,pygame.Rect(heroX+29,heroY-90,180,20))
    pygame.draw.rect(screen,STEEL,pygame.Rect(heroX+85,heroY-90,30,28))
    
    # Left arm.
    pygame.draw.ellipse(screen,DARK_BLUE,pygame.Rect(heroX-185,heroY-80,65,105))
    
    # Left shoulder plates.
    pygame.draw.ellipse(screen,STEEL,pygame.Rect(heroX-209,heroY-160,180,160))
    pygame.draw.rect(screen,BACKGROUND,pygame.Rect(heroX-298,heroY-160,180,80))
    pygame.draw.rect(screen,BACKGROUND,pygame.Rect(heroX-111,heroY-160,95,160))
    pygame.draw.rect(screen,BACKGROUND,pygame.Rect(heroX-160,heroY-160,150,85))
    
    pygame.draw.ellipse(screen,STEEL,pygame.Rect(heroX-209,heroY-90,180,20))
    pygame.draw.rect(screen,STEEL,pygame.Rect(heroX-115,heroY-90,32,32))    
    
    # Drawing the wings.
    # Right wing.
    pygame.draw.polygon(screen,WING_PURPLE,[[heroX+230,heroY-260],[heroX+240,heroY-110],[heroX+20,heroY-80]])
    pygame.draw.arc(screen,BACKGROUND,[heroX+79,heroY-130,182,90],0,3.0,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX+80,heroY-130,182,90],0,3.0,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX+81,heroY-130,182,90],0,3.0,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX+84,heroY-130,182,90],0,3.0,44)
    pygame.draw.line(screen,WING_OUTLINE,(heroX+230,heroY-260),(heroX+20,heroY-80),4)
    
    pygame.draw.polygon(screen,WING_PURPLE,[[heroX+230,heroY-260],[heroX+240,heroY-115],[heroX+400,heroY-170]])
    pygame.draw.arc(screen,BACKGROUND,[heroX+239,heroY-175,210,90],0,3.6,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX+240,heroY-175,210,90],0,3.6,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX+241,heroY-175,210,90],0,3.6,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX+244,heroY-175,210,90],0,3.6,44)
    pygame.draw.line(screen,WING_OUTLINE,(heroX+230,heroY-260),(heroX+240,heroY-115),4)
    
    pygame.draw.polygon(screen,WING_PURPLE,[[heroX+230,heroY-260],[heroX+400,heroY-170],[heroX+450,heroY-290]])
    pygame.draw.ellipse(screen,BACKGROUND,pygame.Rect(heroX+385,heroY-287,120,139))
    pygame.draw.line(screen,WING_OUTLINE,(heroX+230,heroY-260),(heroX+400,heroY-170),4)
    pygame.draw.line(screen,WING_OUTLINE,(heroX+230,heroY-260),(heroX+450,heroY-290),4)
    
    # Left wing.
    pygame.draw.polygon(screen,WING_PURPLE,[[heroX-230,heroY-260],[heroX-240,heroY-110],[heroX-20,heroY-80]])
    pygame.draw.arc(screen,BACKGROUND,[heroX-261,heroY-130,182,90],0,3.0,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX-260,heroY-130,182,90],0,3.0,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX-259,heroY-130,182,90],0,3.0,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX-256,heroY-130,182,90],0,3.0,44)
    pygame.draw.line(screen,WING_OUTLINE,(heroX-230,heroY-260),(heroX-20,heroY-80),4)
    
    pygame.draw.polygon(screen,WING_PURPLE,[[heroX-230,heroY-260],[heroX-240,heroY-115],[heroX-400,heroY-170]])
    pygame.draw.arc(screen,BACKGROUND,[heroX-449,heroY-175,210,90],-1,3.6,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX-450,heroY-175,210,90],-1,3.6,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX-451,heroY-175,210,90],-1,3.6,44)
    pygame.draw.arc(screen,BACKGROUND,[heroX-454,heroY-175,210,90],-1,3.6,44)
    pygame.draw.line(screen,WING_OUTLINE,(heroX-230,heroY-260),(heroX-240,heroY-115),4)
    
    pygame.draw.polygon(screen,WING_PURPLE,[[heroX-230,heroY-260],[heroX-400,heroY-170],[heroX-450,heroY-290]])
    pygame.draw.ellipse(screen,BACKGROUND,pygame.Rect(heroX-505,heroY-287,120,139))
    pygame.draw.line(screen,WING_OUTLINE,(heroX-230,heroY-260),(heroX-400,heroY-170),4)
    pygame.draw.line(screen,WING_OUTLINE,(heroX-230,heroY-260),(heroX-450,heroY-290),4)    

    # Drawing the basic body.
    pygame.draw.circle(screen,DARK_BLUE,(heroX,heroY),125)
    
    # Drawing the mask and eyes.
    pygame.draw.circle(screen,LIGHT_GRAY,(heroX,heroY),110)
    pygame.draw.polygon(screen,BLACK,[[heroX-77,heroY-42],[heroX-77,heroY+8],[heroX,heroY+38],[heroX,heroY-12]])
    pygame.draw.polygon(screen,BLACK,[[heroX+77,heroY-42],[heroX+77,heroY+8],[heroX,heroY+38],[heroX,heroY-12]])
    
    pygame.draw.ellipse(screen,YELLOW,pygame.Rect(heroX-50,heroY-48,30,60))
    pygame.draw.ellipse(screen,YELLOW,pygame.Rect(heroX+22,heroY-48,30,60))
    
    pygame.draw.polygon(screen,LIGHT_GRAY,[[heroX-77,heroY-62],[heroX-77,heroY-42],[heroX,heroY-12],[heroX,heroY-42]])
    pygame.draw.polygon(screen,LIGHT_GRAY,[[heroX+77,heroY-62],[heroX+77,heroY-42],[heroX,heroY-12],[heroX,heroY-42]])    
    
    # Drawing the shoulder plate outlines.
    # Right outlines.
    pygame.draw.arc(screen,GOLD,[heroX+27,heroY-160,180,160],-1.5,0.1,3)
    pygame.draw.arc(screen,GOLD,[heroX+28,heroY-160,180,160],-1.5,0.1,3)
    pygame.draw.arc(screen,GOLD,[heroX+29,heroY-160,180,160],-1.5,0.1,3)
    
    pygame.draw.arc(screen,GOLD,[heroX,heroY-99,125,183],-0.1,1.1,3)
    pygame.draw.arc(screen,GOLD,[heroX,heroY-98,125,183],-0.1,1.1,3)
    pygame.draw.arc(screen,GOLD,[heroX,heroY-97,125,183],-0.1,1.1,3)
    
    pygame.draw.arc(screen,GOLD,[heroX+29,heroY-89,180,20],-0.35,2.05,3)
    pygame.draw.arc(screen,GOLD,[heroX+29,heroY-90,180,20],-0.35,2.05,3)
    pygame.draw.arc(screen,GOLD,[heroX+29,heroY-91,180,20],-0.35,2.05,3)
    
    # Left outlines.
    pygame.draw.arc(screen,GOLD,[heroX-208,heroY-160,180,160],-3.2,-1.65,3)
    pygame.draw.arc(screen,GOLD,[heroX-207,heroY-160,180,160],-3.2,-1.65,3)
    pygame.draw.arc(screen,GOLD,[heroX-206,heroY-160,180,160],-3.2,-1.65,3)
    
    pygame.draw.arc(screen,GOLD,[heroX-126,heroY-98,125,183],-4.3,-3.1,3)
    pygame.draw.arc(screen,GOLD,[heroX-125,heroY-98,125,183],-4.3,-3.1,3)
    pygame.draw.arc(screen,GOLD,[heroX-124,heroY-98,125,183],-4.3,-3.1,3)
    
    pygame.draw.arc(screen,GOLD,[heroX-209,heroY-90,180,20],1.23,2.87,3)
    pygame.draw.arc(screen,GOLD,[heroX-209,heroY-89,180,20],1.23,2.87,3)
    pygame.draw.arc(screen,GOLD,[heroX-209,heroY-88,180,20],1.23,2.87,3)
    
    # Drawing the hands/gloves.
    # Right glove.
    pygame.draw.ellipse(screen,GLOVE_OUTLINE,pygame.Rect(heroX+137,heroY-4,73,88))
    pygame.draw.ellipse(screen,GLOVE_WHITE,pygame.Rect(heroX+141,heroY,65,80))
    pygame.draw.ellipse(screen,GLOVE_WHITE,pygame.Rect(heroX+141,heroY+35,40,55))
    
    pygame.draw.arc(screen,DARK_OUTLINE,[heroX+139,heroY+35,40,55],-3.6,0.3,2)
    pygame.draw.arc(screen,DARK_OUTLINE,[heroX+141,heroY+35,40,55],-3.6,0.3,2)
    pygame.draw.arc(screen,DARK_OUTLINE,[heroX+140,heroY+35,40,55],-3.6,0.3,2)
    
    # Left glove.
    pygame.draw.ellipse(screen,GLOVE_OUTLINE,pygame.Rect(heroX-210,heroY-4,73,88))
    pygame.draw.ellipse(screen,GLOVE_WHITE,pygame.Rect(heroX-206,heroY,65,80))
    
    # Drawing the sword under the thumb of the glove.
    # Handle.
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-149,heroY+40],[heroX-167,heroY+35],[heroX-187,heroY+95],[heroX-169,heroY+100]])
    
    # Left guard.
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-183,heroY+104],[heroX-183,heroY+120],[heroX-207,heroY+107],[heroX-207,heroY+91]])
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-207,heroY+91],[heroX-207,heroY+107],[heroX-222,heroY+111],[heroX-222,heroY+95]])
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-222,heroY+111],[heroX-222,heroY+95],[heroX-240,heroY+98]])
    
    # Right guard.
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-183,heroY+104],[heroX-183,heroY+120],[heroX-161,heroY+130],[heroX-151,heroY+114]])
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-151,heroY+114],[heroX-161,heroY+130],[heroX-156,heroY+142],[heroX-141,heroY+132]])
    pygame.draw.polygon(screen,SWORD_GOLD,[[heroX-156,heroY+142],[heroX-141,heroY+132],[heroX-130,heroY+156]])    
    
    # Main blade.
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-242,heroY+246],[heroX-222,heroY+254],[heroX-173,heroY+113],[heroX-193,heroY+107]])
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-242,heroY+246],[heroX-222,heroY+254],[heroX-243.5,heroY+280]])
    
    # Additional blades.
    # Left blades.
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-211,heroY+157],[heroX-236,heroY+155],[heroX-240,heroY+135],[heroX-204,heroY+137]])
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-236,heroY+155],[heroX-240,heroY+135],[heroX-260,heroY+175]])
    
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-232,heroY+217],[heroX-260,heroY+215],[heroX-272,heroY+195],[heroX-225,heroY+197]])
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-260,heroY+215],[heroX-272,heroY+195],[heroX-284,heroY+235]])
    
    # Right blades.
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-189,heroY+162],[heroX-168,heroY+185],[heroX-150,heroY+175],[heroX-182,heroY+142]])
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-168,heroY+185],[heroX-150,heroY+175],[heroX-171,heroY+212]])
    
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-211,heroY+222],[heroX-178,heroY+240],[heroX-160,heroY+230],[heroX-203,heroY+202]])
    pygame.draw.polygon(screen,LIGHT_SWORD_GOLD,[[heroX-178,heroY+240],[heroX-160,heroY+230],[heroX-175,heroY+270]])
    
    # Center guard.
    pygame.draw.circle(screen,SWORD_GOLD,(heroX-181,heroY+110),19)
    pygame.draw.circle(screen,RUBY_RED,(heroX-181,heroY+110),15)
    pygame.draw.circle(screen,WHITE,(heroX-183,heroY+107),6)
    
    # Continuing the left glove.
    pygame.draw.ellipse(screen,GLOVE_WHITE,pygame.Rect(heroX-181,heroY+35,40,55))
    
    pygame.draw.arc(screen,DARK_OUTLINE,[heroX-179,heroY+35,40,55],-3.4,0.6,2)
    pygame.draw.arc(screen,DARK_OUTLINE,[heroX-180,heroY+35,40,55],-3.4,0.6,2)
    pygame.draw.arc(screen,DARK_OUTLINE,[heroX-181,heroY+35,40,55],-3.4,0.6,2)
    
    pygame.display.flip()
    pygame.time.wait(waitTime)

drawHero(640,375)
pygame.quit()

