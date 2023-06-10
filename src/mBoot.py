from lib.mBot import *

if __name__ == '__main__':
        bot = mBot()
        bot.startWithHID()
        while(1):

                bot.doMove( 0, 0)
                sleep(1)
                bot.doMove( 63, 63)
                sleep(1)
                bot.doMove( 127, 127)
                sleep(1)
                bot.doMove( 255, 255)
                sleep(1)