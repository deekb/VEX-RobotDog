from vex import *

brain = Brain()

if not brain.sdcard.is_inserted():
    brain.screen.print("Please insert the SD card")
    while not brain.sdcard.is_inserted():
        wait(50, MSEC)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

from Robot import Robot

if __name__ == "__main__":
    robot = Robot(brain)
