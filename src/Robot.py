from vex import *
import Constants
import math
from Leg import Leg
from Utilities import Terminal, PIDController


SCREEN_Y_SIZE = 240
SCREEN_X_SIZE = 480

FIELD_X_SIZE = 366
FIELD_Y_SIZE = 366


class Robot:
    def __init__(self, brain):
        self.brain = brain
        self.terminal = Terminal(self.brain)
        self.print = self.terminal.print
        self.clear = self.terminal.clear

        # Physical devices/groups of devices:
        self.inertial_sensor = Inertial(Constants.inertial_sensor_port)

        self.front_left_hip_motor = Motor(
            Constants.front_left_hip_motor_port,
            Constants.front_left_hip_motor_gear_ratio,
            Constants.front_left_hip_motor_inverted,
        )
        self.front_right_hip_motor = Motor(
            Constants.front_right_hip_motor_port,
            Constants.front_right_hip_motor_gear_ratio,
            Constants.front_right_hip_motor_inverted,
        )
        self.back_left_hip_motor = Motor(
            Constants.back_left_hip_motor_port,
            Constants.back_left_hip_motor_gear_ratio,
            Constants.back_left_hip_motor_inverted,
        )
        self.back_right_hip_motor = Motor(
            Constants.back_right_hip_motor_port,
            Constants.back_right_hip_motor_gear_ratio,
            Constants.back_right_hip_motor_inverted,
        )

        self.front_left_knee_motor = Motor(
            Constants.front_left_knee_motor_port,
            Constants.front_left_knee_motor_gear_ratio,
            Constants.front_left_knee_motor_inverted,
        )
        self.front_right_knee_motor = Motor(
            Constants.front_right_knee_motor_port,
            Constants.front_right_knee_motor_gear_ratio,
            Constants.front_right_knee_motor_inverted,
        )
        self.back_left_knee_motor = Motor(
            Constants.back_left_knee_motor_port,
            Constants.back_left_knee_motor_gear_ratio,
            Constants.back_left_knee_motor_inverted,
        )
        self.back_right_knee_motor = Motor(
            Constants.back_right_knee_motor_port,
            Constants.back_right_knee_motor_gear_ratio,
            Constants.back_right_knee_motor_inverted,
        )

        self.front_left_leg = Leg(self.front_left_hip_motor, self.front_left_knee_motor)
        self.front_right_leg = Leg(
            self.front_right_hip_motor, self.front_right_knee_motor
        )
        self.back_left_leg = Leg(self.back_left_hip_motor, self.back_left_knee_motor)
        self.back_right_leg = Leg(self.back_right_hip_motor, self.back_right_knee_motor)

        self.balance_PID = PIDController(
            self.brain.timer,
            Constants.balance_Kp,
            Constants.balance_Ki,
            Constants.balance_Kd,
            0.01,
            0.5,
        )

        self.primary_controller = Controller(PRIMARY)

        self.on_driver_control()

    def on_driver_control(self):
        """
        This is the function designated to run when the driver control portion of the program is triggered
        """
        # Wait for setup to finish
        self.print("Calibrating Inertial sensor...")
        self.inertial_sensor.calibrate()

        while self.inertial_sensor.is_calibrating():
            pass

        self.print("Done")

        self.balance_PID.target_value = 0

        for leg in (self.front_left_leg, self.front_right_leg, self.back_left_leg, self.back_right_leg):
            leg.move_hip_motor_to_position(Constants.hip_idle)
            leg.move_knee_motor_to_position(Constants.knee_idle)

        # while True:
        #     roll = math.radians(
        #         self.inertial_sensor.orientation(OrientationType.ROLL, DEGREES)
        #     )
        #
        #     pid_output = self.balance_PID.update(roll)
        #
        #     # self.front_left_leg.set_hip_motor_power(pid_output)
        #     # self.back_left_leg.set_hip_motor_power(pid_output)
        #     # self.front_left_leg.set_knee_motor_power(pid_output)
        #     # self.back_left_leg.set_knee_motor_power(pid_output)
        #     #
        #     # self.front_right_leg.set_hip_motor_power(-pid_output)
        #     # self.back_right_leg.set_hip_motor_power(-pid_output)
        #     # self.front_right_leg.set_knee_motor_power(-pid_output)
        #     # self.back_right_leg.set_knee_motor_power(-pid_output)
        #
        #     wait(10, MSEC)
