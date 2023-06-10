from lib.mBot import *
import pygame

pygame.init()
pygame.joystick.init()

AXIS_STICK_LEFTRIGHT = 0
AXIS_STICK_UPDOWN = 1
AXIS_THROTTLE_UPDOWN = 2
AXIS_STICK_TWIST= 3
AXIS_THROTTLE_BUTTONS = 4

joystick_count = pygame.joystick.get_count()
print("joystick_count:")
print(joystick_count)
if joystick_count == 0:
    print("No joystick detected :-(")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

if __name__ == '__main__':
    bot = mBot()
    bot.startWithHID()
    while(1):

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                
        speed = -joystick.get_axis(2)
        
        bot.doMove( (int)(speed * 255), (int)(speed * 255))