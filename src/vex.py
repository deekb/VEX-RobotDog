"""
This file is for Pycharm autocomplete only and has no functionality,
it does NOT need to be uploaded to the robot or placed on the SD card
it also does not need to be formatted correctly or error-free
"""

# noinspection PyUnusedLocal
# noinspection PyPep8Naming
SECONDS = "SECONDS"
PERCENT = "PERCENT"
DEGREES = "DEGREES"
MM = "MM"
MSEC = "MSEC"
VOLT = "VOLT"
PRIMARY = "PRIMARY"
PARTNER = "PARTNER"
COAST = "COAST"
BRAKE = "BRAKE"
HOLD = "HOLD"
FORWARD = "FORWARD"
REVERSE = "REVERSE"


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
def Thread(*args, **kwargs):
    pass


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class Competition:
    def __init__(self, *args):
        pass

    @staticmethod
    def is_enabled():
        return False

    @staticmethod
    def is_autonomous():
        return False

    @staticmethod
    def is_driver_control():
        return False


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class Inertial:

    # noinspection PyUnusedLocal
    def __init__(self, port):
        pass

    @staticmethod
    def calibrate():
        pass

    @staticmethod
    def heading(*args):
        pass

    @staticmethod
    def rotation(*args):
        pass

    @staticmethod
    def is_calibrating():
        return False

    @staticmethod
    def set_heading(*args):
        pass

    @staticmethod
    def set_rotation(*args):
        pass


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class Distance:
    def __init__(self, port):
        pass

    def object_distance(self, units):
        pass

    def is_object_detected(self):
        pass


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class Controller:
    def __init__(self, port):
        self.port = port
        pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonL1:
        def pressed(*args):
            pass

        def pressing(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonL2:
        def pressed(*args):
            pass

        def pressing(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonR1:
        def pressed(*args):
            pass

        def pressing(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonR2:
        def pressed(*args):
            pass

        def pressing(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class screen:
        @staticmethod
        def print(text):
            pass

        @staticmethod
        def set_cursor(row, column):
            pass

        @staticmethod
        def next_row():
            pass

        @staticmethod
        def clear_screen():
            pass

        @staticmethod
        def clear_row(row=-1):
            pass

        @staticmethod
        def draw_pixel(x, y):
            pass

        @staticmethod
        def draw_line(start_x, start_y, end_x, end_y):
            pass

        @staticmethod
        def draw_rectangle(x, y, width, height):
            pass

        @staticmethod
        def draw_circle(x, y, radius):
            pass

        @staticmethod
        def set_font(font_type):
            pass

        @staticmethod
        def set_pen_width(pen_width):
            pass

        @staticmethod
        def set_pen_color(color):
            pass

        @staticmethod
        def set_fill_color(color):
            pass

        @staticmethod
        def pressed(callback):
            pass

        @staticmethod
        def released(callback):
            pass

        @staticmethod
        def row():
            return 20

        @staticmethod
        def column():
            return 80

        @staticmethod
        def pressing():
            return False

        @staticmethod
        def x_position():
            return 0

        @staticmethod
        def y_position():
            return 0

        @classmethod
        def draw_image_from_file(cls, *args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonLeft:
        @staticmethod
        def pressing():
            return False

        def pressed(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonRight:
        @staticmethod
        def pressing():
            return False

        def pressed(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonA:
        @staticmethod
        def pressing():
            return False

        def pressed(*args):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class buttonB:
        @staticmethod
        def pressing():
            return False

        def pressed(*args):
            pass

    @staticmethod
    def rumble(*args):
        pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class axis1:
        @staticmethod
        def position():
            return 0

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class axis2:
        @staticmethod
        def position():
            return 0

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class axis3:
        @staticmethod
        def position():
            return 0

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class axis4:
        @staticmethod
        def position():
            return 0


class Motor:
    # noinspection PyUnusedLocal
    def __init__(self, port, gear_ratio, inverted):
        pass

    @staticmethod
    def spin(direction, voltage=10, unit=VOLT):
        pass

    @staticmethod
    def spin_for(direction, degrees, unit=DEGREES):
        pass

    @staticmethod
    def stop():
        pass

    @staticmethod
    def set_position():
        pass

    @staticmethod
    def position(*args):
        pass

    @staticmethod
    def set_velocity(*args):
        pass

    @staticmethod
    def velocity():
        return 0


class MotorGroup:
    def __init__(self, *motors):
        pass

    def spin(self, direction):
        pass

    def set_stopping(self, *args):
        pass

    def set_velocity(self, *args):
        pass

    # noinspection PyUnusedLocal
    @staticmethod
    def position(*args):
        return 0

    def stop(self):
        pass


class Ports:
    PORT1 = "Port 1"
    PORT2 = "Port 2"
    PORT3 = "Port 3"
    PORT4 = "Port 4"
    PORT5 = "Port 5"
    PORT6 = "Port 6"
    PORT7 = "Port 7"
    PORT8 = "Port 8"
    PORT9 = "Port 9"
    PORT10 = "Port 10"
    PORT11 = "Port 11"
    PORT12 = "Port 12"
    PORT13 = "Port 13"
    PORT14 = "Port 14"
    PORT15 = "Port 15"
    PORT16 = "Port 16"
    PORT17 = "Port 17"
    PORT18 = "Port 18"
    PORT19 = "Port 19"
    PORT20 = "Port 20"
    PORT21 = "Port 21"


class GearSetting:
    RATIO_6_1 = "6 to 1"
    RATIO_18_1 = "18 to 1"
    RATIO_36_1 = "36 to 1"


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class FontType:
    @staticmethod
    def MONO12():
        pass

    @staticmethod
    def MONO15():
        pass

    @staticmethod
    def MONO20():
        pass

    @staticmethod
    def MONO30():
        pass

    @staticmethod
    def MONO40():
        pass

    @staticmethod
    def MONO60():
        pass

    @staticmethod
    def PROP20():
        pass

    @staticmethod
    def PROP30():
        pass

    @staticmethod
    def PROP40():
        pass

    @staticmethod
    def PROP60():
        pass


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class Color:
    @staticmethod
    def BLACK():
        pass

    @staticmethod
    def WHITE():
        pass

    @staticmethod
    def RED():
        pass

    @staticmethod
    def GREEN():
        pass

    @staticmethod
    def BLUE():
        pass

    @staticmethod
    def YELLOW():
        pass

    @staticmethod
    def ORANGE():
        pass

    @staticmethod
    def PURPLE():
        pass

    @staticmethod
    def CYAN():
        pass

    @staticmethod
    def TRANSPARENT():
        pass


# noinspection PyUnusedLocal
# noinspection PyPep8Naming
class Brain:
    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class screen:
        @staticmethod
        def print(text):
            pass

        @staticmethod
        def set_cursor(row, column):
            pass

        @staticmethod
        def next_row():
            print("\n")

        @staticmethod
        def clear_screen():
            pass

        @staticmethod
        def clear_row(row=-1):
            pass

        @staticmethod
        def draw_pixel(x, y):
            pass

        @staticmethod
        def draw_line(start_x, start_y, end_x, end_y):
            pass

        @staticmethod
        def draw_rectangle(x, y, width, height):
            pass

        @staticmethod
        def draw_circle(x, y, radius):
            pass

        @staticmethod
        def set_font(font_type):
            pass

        @staticmethod
        def set_pen_width(pen_width):
            pass

        @staticmethod
        def set_pen_color(color):
            pass

        @staticmethod
        def set_fill_color(color):
            pass

        @staticmethod
        def pressed(callback):
            callback()

        @staticmethod
        def released(*args):
            pass

        @staticmethod
        def row():
            return 20

        @staticmethod
        def column():
            return 80

        @staticmethod
        def pressing():
            return False

        @staticmethod
        def x_position():
            return 0

        @staticmethod
        def y_position():
            return 0

        @classmethod
        def draw_image_from_file(cls, param, param1, param2):
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class sdcard:
        @staticmethod
        def is_inserted():
            pass

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class battery:
        @staticmethod
        def voltage():
            return 12.0

        @staticmethod
        def current():
            return 16.0

        @staticmethod
        def capacity():
            return 100.0

    # noinspection PyUnusedLocal
    # noinspection PyPep8Naming
    class timer:
        @staticmethod
        def event(callback, timee):
            pass

        @staticmethod
        def clear():
            pass

        @staticmethod
        def time(units):
            pass


# noinspection PyUnusedLocal
def wait(*args):
    pass
