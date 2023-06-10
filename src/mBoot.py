from lib.mBot import *
import pygame

pygame.init()
pygame.joystick.init()

AXIS_STICK_LEFTRIGHT = 0
AXIS_STICK_UPDOWN = 1
AXIS_THROTTLE_UPDOWN = 2
AXIS_STICK_TWIST= 3
AXIS_THROTTLE_BUTTONS = 4

BUTTON_STICK_THUMB = 1

joystick_count = pygame.joystick.get_count()
print("joystick_count:")
print(joystick_count)
if joystick_count == 0:
    print("No joystick detected :-(")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

toetSound = pygame.mixer.Sound("toet.wav")

buttonReleased = False

if __name__ == '__main__':
    bot = mBot()
    bot.startWithHID()
    while(1):

        if( joystick.get_button(1) == 0 ):
                buttonReleased = True
        else:
                if( buttonReleased ):
                        pygame.mixer.Sound.play(toetSound)
                buttonReleased = False

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

        speed = -joystick.get_axis(AXIS_THROTTLE_UPDOWN)
        turn = joystick.get_axis(AXIS_THROTTLE_BUTTONS)

        speedLeft = speed
        if( turn < 0 ):
                speedLeft += 2 * turn * speed

        speedRight = speed
        if( turn > 0):
                speedRight -= 2 * turn * speed

        print( "speed: " + str(speed) + " -- turn: " + str(turn) + " => speedLeft: " + str(speedLeft) + " -- speedRight: " + str(speedRight))
        
        bot.doMove( (int)(speedLeft * 255), (int)(speedRight * 255))