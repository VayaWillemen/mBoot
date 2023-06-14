from lib.mBot import *
import pygame

def FindJoystick():
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
                print("No joystick detected :-(")
                print("Connect a joystick or game controller and start again...")
                pygame.quit()
                exit()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print( "Yes! I found " + str(joystick_count) + " joystick" + ("" if joystick_count == 1 else "s"))
        print( "I will use this one: '" + joystick.get_name() + "'")

        return joystick

def FindMBot():
    try:
        bot = mBot()
        bot.startWithHID()
        return bot
    except Exception as err:
        print(f"Could not initialize mBot {err=}, {type(err)=}")
        print("Insert a 2.4GHz-dongle, turn on the mBot and start again...")
        exit()

# Constants for axis for the Thrustmaster T-Flight Hotas X v.2
AXIS_TRUSTMASTER_STICK_LEFTRIGHT = 0
AXIS_TRUSTMASTER_STICK_UPDOWN = 1
AXIS_TRUSTMASTER_THROTTLE_UPDOWN = 2
AXIS_TRUSTMASTER_STICK_TWIST= 3
AXIS_TRUSTMASTER_THROTTLE_BUTTONS = 4
BUTTON_TRUSTMASTER_STICK_THUMB = 1

# Constants for the usb game controller
AXIS_GAMEPAD_JOYLEFT_UPDOWN = 1
AXIS_GAMEPAD_JOYLEFT_LEFTRIGHT = 0
BUTTON_GAMEPAD_RIGHT_THUMB_1 = 0

# True if the button was released (to detect edges)
buttonReleased = False

if __name__ == '__main__':

    # Initialize PyGame & joystick
    pygame.init()
    pygame.joystick.init()
    joystick = FindJoystick()
    
    # Inittilize axis, buttons and sounds, depending on which joystick is being used
    if( joystick.get_name().upper().startswith("T.FLIGHT")):
        axis_throttle = AXIS_TRUSTMASTER_THROTTLE_UPDOWN
        axis_turn = AXIS_TRUSTMASTER_THROTTLE_BUTTONS
        button_sound = BUTTON_TRUSTMASTER_STICK_THUMB
        toetSound = pygame.mixer.Sound("toet.wav")
    else:
        axis_throttle = AXIS_GAMEPAD_JOYLEFT_UPDOWN
        axis_turn = AXIS_GAMEPAD_JOYLEFT_LEFTRIGHT
        button_sound = BUTTON_GAMEPAD_RIGHT_THUMB_1
        toetSound = pygame.mixer.Sound("toet2.wav")

    # Connect with the mBot
    bot = FindMBot()

    # Start the fun :-)
    while(True):
         # Process all pygame events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

        # Button not pushed? Remember it! Than you're allowed to play a sound once the button is pushed
        if( joystick.get_button(button_sound) == 0 ):
                buttonReleased = True
        else:
                # The button is pushed => Only play a new sound if it was not yet pushed before
                if( buttonReleased ):
                        pygame.mixer.Sound.play(toetSound)
                buttonReleased = False
  

        # Calculate the sped of each wheel
        speed = -joystick.get_axis(axis_throttle)
        turn = joystick.get_axis(axis_turn)

        speedLeft = speed
        if( turn < 0 ):
                speedLeft += 2 * turn * speed

        speedRight = speed
        if( turn > 0):
                speedRight -= 2 * turn * speed

        print( "speed: " + str(speed) + " -- turn: " + str(turn) + " => speedLeft: " + str(speedLeft) + " -- speedRight: " + str(speedRight))
        
        # Send the speeds to the mBot / mBoot
        bot.doMove( (int)(speedLeft * 255), (int)(speedRight * 255))