"""
This module provides various utility functions and classes for controlling VEX robots.

Module dependencies:
- math
- vex

Classes:
- Terminal: A class for interacting with the brain console.
    Methods:
    - __init__(self, brain): Initialize the Terminal object.
    - clear(self): Clears the brain screen.
    - print(self, text: str, end: str = "\n"): Prints a string to the console.

- MotorPID: A class for controlling motors using a custom PID controller.
    Methods:
    - __init__(self, timer: Brain.timer, motor_object, kp: float = 0.4, ki: float = 0.01, kd:
    float = 0.05, t: float = 0.1): Initialize the MotorPID object.
    - update(self): Update the PID state with the most recent motor and target velocities and send the normalized value to the motor.
    - loop(self): Run the PID in a new thread, updating the values and applying them to the motor.
    - set_velocity(self, velocity: float): Set the motor's target velocity using the PID.
    - spin(self, DIRECTION): Spin the motor in the specified direction.
    - stop(self): Stop the motor.
    - velocity(self, _type): Get the motor's velocity.

- PIDController: A generalized PID controller implementation.
    Methods:
    - __init__(self, timer: Brain.timer, kp: float = 1, ki: float = 0, kd: float = 0): Initialize the PIDController object.
    - update(self, current_value: float) -> float: Update the PID state with the most recent current value and calculate the control output.

- Logging: A class for logging events to the SD card.
    Methods:
    - __init__(self, log_name, log_format: str): Initialize the Logging object.
    - log(self, string: str, function_name: str = ""): Send a string to the log file using the log format.
    - exit(self): Close the log object.

Functions:
- apply_deadzone: Apply a dead zone to a value.
- check_position_within_tolerance: Check if two sets of coordinates are within a certain distance.
- apply_cubic: Normalize a value across a cubic curve.
- clamp: Restrict a value within a specified range.

Author: derek.m.baier@gmail.com
Modified: Friday, July 7, 2023
"""

import math
from vex import *


class Terminal(object):
    def __init__(self, brain):
        self.brain = brain
        self.log = Logging("Terminal")
        self.brain.screen.set_font(FontType.MONO12)

    def clear(self):
        """
        Clears the brain screen
        """

        self.log.log("{Clearing terminal}\n")
        self.brain.screen.clear_screen()
        self.brain.screen.set_cursor(1, 1)

    def print(self, text: str, end: str = "\n"):
        """
        Prints a string to a console
        :param text: the text to print to the screen
        :param end: The string to print at the end (defaults to new line)
        """

        self.log.log(str(text) + str(end))

        # Deal with the vex brain class' inability to parse "\n" as a newline (^ look, Logging.log can do it ^)
        text_split = str(text).split("\n")
        i = 0
        for part in text_split:
            self.brain.screen.print(str(part))
            if i != len(text_split) - 1:
                self.brain.screen.next_row()
            i += 1

        # And again :)
        end_split = str(end).split("\n")
        i = 0
        for part in end_split:
            self.brain.screen.print(str(part))
            if i != len(end_split) - 1:
                self.brain.screen.next_row()
            i += 1


def apply_deadzone(value: float, dead_zone: float, maximum: float) -> float:
    """
    Apply a dead_zone to the passed value
    :param maximum: The maximum value for the input, helps to smooth out the returned values when the value is outside the dead zone
    :param value: The value to apply a deadzone to
    :param dead_zone: The lowest value that should have a nonzero output
    """

    if abs(value) < dead_zone:
        return 0
    else:
        return maximum / (maximum - dead_zone) * (value - dead_zone)


def check_position_within_distance(current_coordinates: tuple, target_coordinates: tuple, max_distance: float):
    """
    Checks whether two sets of coordinates are within a distance from each other
    :param current_coordinates: The set of coordinates corresponding to the robot's position
    :type current_coordinates: tuple[float | float]
    :param target_coordinates: The set of coordinates corresponding to the target's position
    :type target_coordinates: tuple[float | float]
    :param max_distance: the maximum distance apart that should return True
    """

    current_x, current_y = current_coordinates
    target_x, target_y = target_coordinates
    distance = math.sqrt((current_y - target_y) ** 2 + (current_x - target_x) ** 2)
    return distance <= max_distance


class MotorPID(object):
    """
    Wrap a motor definition in this class to use a custom PID to control its movements ie: my_motor = MotorPID(Motor(...), kp, kd, t)
    Waring, this class disables all motor functionality except the following functions:[set_velocity, set_stopping, stop, spin, velocity]
    :param motor_object: The motor to apply the PID to
    :param kp: Kp value for the PID: How quickly to modify the target value if it has not yet reached the desired value
    :param ki: Ki value for the PID: Integral gain to reduce steady-state error
    :param kd: Kd value for the PID: Higher values reduce the response time and limit overshoot
    :param t: Time between PID updates
    """

    def __init__(self, timer: Brain.timer, motor_object, kp: float = 0.4, ki: float = 0.01, kd: float = 0.05,
                 t: float = 0.1) -> None:
        self.motor_object = motor_object
        self.motor_PID = PIDController(timer, kp, ki, kd)
        self.pid_thread = Thread(self.loop)
        self.t = t

    def update(self) -> None:
        """
        Update the PID state with the most recent motor and target velocities and send the normalized value to the motor
        """

        self.motor_object.set_velocity(self.motor_PID.update(self.velocity()), PERCENT)

    def loop(self) -> None:
        """
        Used to run the PID in a new thread:
         updates the values the PID uses and handles
          applying those updated unsigned_target_speed values to the motor
        """

        while True:
            self.update()
            wait(self.t, SECONDS)

    def set_velocity(self, velocity: float) -> None:
        """
        Set the motors target velocity using the PID, make sure you run PID_loop in a new thread or this
        will have no effect
        :param velocity: The new target velocity of the motor
        :type velocity: float
        """

        self.motor_PID._target_value = velocity

    def spin(self, direction):
        self.motor_object.spin(direction)

    def stop(self):
        self.motor_object.stop()

    def velocity(self):
        return self.motor_object.velocity(PERCENT)


class PIDController(object):
    """
    A generalized PID controller implementation.
    """

    def __init__(self, timer: Brain.timer, kp: float = 1.0, ki: float = 0.0, kd: float = 0.0, t: float = 0.05, integral_limit: float = 1.0):
        """
        Initializes a PIDController instance.
        :param timer: The timer object used to measure time.
        :param kp: Kp value for the PID.
        :param ki: Ki value for the PID.
        :param kd: Kd value for the PID.
        :param t: Minimum time between update calls.
        All calls made before this amount of time has passed since the last calculation will be ignored.
        :param integral_limit: The maximum absolute value for the integral term to prevent windup.
        """

        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._timer = timer
        self._time_step = t
        self._previous_time = timer.time(SECONDS)
        self._current_value = 0.0
        self._target_value = 0.0
        self._error_integral = 0.0
        self._integral_limit = integral_limit
        self._previous_error = 0.0
        self._control_output = 0.0

    @property
    def kp(self) -> float:
        """
        Getter for the Kp value of the PID.
        :return: The Kp value.
        """

        return self._kp

    @kp.setter
    def kp(self, value: float):
        """
        Setter for the Kp value of the PID.
        :param value: The new Kp value.
        """

        self._kp = value

    @property
    def ki(self) -> float:
        """
        Getter for the Ki value of the PID.
        :return: The Ki value.
        """

        return self._ki

    @ki.setter
    def ki(self, value: float):
        """
        Setter for the Ki value of the PID.
        :param value: The new Ki value.
        """

        self._ki = value

    @property
    def kd(self) -> float:
        """
        Getter for the Kd value of the PID.
        :return: The Kd value.
        """

        return self._kd

    @kd.setter
    def kd(self, value: float):
        """
        Setter for the Kd value of the PID.
        :param value: The new Kd value.
        """

        self._kd = value

    @property
    def target_value(self) -> float:
        """
        Getter for the target value of the PID.
        :return: The target value.
        """

        return self._target_value

    @target_value.setter
    def target_value(self, value: float):
        """
        Setter for the target value of the PID.
        :param value: The new target value.
        """
        if value != self._target_value:
            self._target_value = value
            # self._previous_error = self._target_value - self._current_value
            # self._control_output = 0

    def reset(self):
        self._error_integral = 0
        self._previous_error = self._target_value - self._current_value
        self._control_output = 0

    def update(self, current_value: float) -> float:
        """
        Update the PID state with the most recent current value and calculate the control output.
        :param current_value: The current measurement or feedback value.
        :return: The calculated control output.
        """

        current_time = self._timer.time(SECONDS)
        delta_time = current_time - self._previous_time

        if delta_time < self._time_step:
            return self._control_output

        self._previous_time = current_time

        current_error = self._target_value - current_value
        self._error_integral += current_error * delta_time
        # Apply integral windup prevention
        # PID integral windup is a phenomenon that occurs when the integral term of a PID
        # controller continues to accumulate error even when the controller's output is saturated.
        # This can lead to overshoot, instability, and poor performance in control systems.
        # if your Kp is reasonably low, and you are still experiencing overshoot/instability/oscillation,
        # then try decreasing the integral limit
        if self._ki != 0:
            self._error_integral = clamp(self._error_integral, -self._integral_limit / self._ki, self._integral_limit / self._ki)
        error_derivative = (current_error - self._previous_error) / delta_time
        self._control_output = (
                self._kp * current_error + self._ki * self._error_integral + self._kd * error_derivative
        )
        self._previous_error = current_error
        return self._control_output


class Logging(object):
    """
    A class that can run multiple logs for different events and store their outputs to the SD card
    """

    def __init__(self, log_name, flush_interval=1):
        """
        Create a new instance of the class
        :param log_name: The name to use for the log, a number preceded by a hyphen "-" will be appended to this name to avoid overwriting old logs
        :type log_name: str
        """

        self.file_name = "/Logs/" + str(log_name) + ".log"
        self.file_object = open(self.file_name, "w")
        self.write_lock = False
        self.log("Starting log at " + self.file_name)

        Thread(self.auto_flush_logs, [flush_interval])

    def log(self, string: str):
        """
        Send a string to the file, using the log format
        :param string:
        """
        while self.write_lock:
            wait(5, MSEC)
        self.write_lock = True
        self.file_object.write(string)
        self.write_lock = False

    def exit(self):
        """
        Close the log object
        """
        while self.write_lock:
            wait(5, MSEC)
        self.log("Ending log at " + self.file_name)
        self.file_object.close()

    def flush_file_contents(self):
        while self.write_lock:
            wait(5, MSEC)
        self.write_lock = True
        self.file_object.flush()
        self.file_object.close()
        self.file_object = open(self.file_name, "a")
        self.write_lock = False

    def auto_flush_logs(self, interval_sec):
        while True:
            wait(interval_sec, SECONDS)
            self.flush_file_contents()



def distance_from_point_to_line(point, slope, x_intercept, y_intercept):
    # Convert the line equation to standard form: (Ax - y + C = 0)
    a = slope
    b = -1
    c = y_intercept
    # Extract the coordinates of the point
    x0, y0 = point
    # Calculate the distance using the formula
    if math.isinf(slope):
        return abs(x0 - x_intercept)
    else:
        return abs(a * x0 + b * y0 + c) / math.sqrt(a ** 2 + b ** 2)


def clamp(value: float, lower_limit: float = None, upper_limit: float = None) -> float:
    """
    Restricts a value within a specified range.
    :param value: The value to be clamped.
    :param lower_limit: The lower limit of the range.
        If None, no lower limit is applied.
    :param upper_limit: The upper limit of the range.
        If None, no upper limit is applied.
    :return: The clamped value.
    """

    if lower_limit is None or upper_limit is None:
        return value
    if lower_limit is not None:
        if value < lower_limit:
            return lower_limit
    if upper_limit is not None:
        if value > upper_limit:
            return upper_limit
    return value


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def load_from_tuple(self, _tuple):
        self.x, self.y = _tuple

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])
