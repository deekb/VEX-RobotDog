import Constants
from vex import *


def main():
    front_left_hip_motor = Motor(
        Constants.front_left_hip_motor_port,
        Constants.front_left_hip_motor_gear_ratio,
        Constants.front_left_hip_motor_inverted,
    )
    front_right_hip_motor = Motor(
        Constants.front_right_hip_motor_port,
        Constants.front_right_hip_motor_gear_ratio,
        Constants.front_right_hip_motor_inverted,
    )
    back_left_hip_motor = Motor(
        Constants.back_left_hip_motor_port,
        Constants.back_left_hip_motor_gear_ratio,
        Constants.back_left_hip_motor_inverted,
    )
    back_right_hip_motor = Motor(
        Constants.back_right_hip_motor_port,
        Constants.back_right_hip_motor_gear_ratio,
        Constants.back_right_hip_motor_inverted,
    )

    front_left_knee_motor = Motor(
        Constants.front_left_knee_motor_port,
        Constants.front_left_knee_motor_gear_ratio,
        Constants.front_left_knee_motor_inverted,
    )
    front_right_knee_motor = Motor(
        Constants.front_right_knee_motor_port,
        Constants.front_right_knee_motor_gear_ratio,
        Constants.front_right_knee_motor_inverted,
    )
    back_left_knee_motor = Motor(
        Constants.back_left_knee_motor_port,
        Constants.back_left_knee_motor_gear_ratio,
        Constants.back_left_knee_motor_inverted,
    )
    back_right_knee_motor = Motor(
        Constants.back_right_knee_motor_port,
        Constants.back_right_knee_motor_gear_ratio,
        Constants.back_right_knee_motor_inverted,
    )

    for motor in (
        front_left_hip_motor,
        front_right_hip_motor,
        back_left_hip_motor,
        back_right_hip_motor,
        front_left_knee_motor,
        front_right_knee_motor,
        back_left_knee_motor,
        back_right_knee_motor,
    ):
        motor.set_position(0, DEGREES)

    for motor in (
        front_left_hip_motor,
        front_right_hip_motor,
        back_left_hip_motor,
        back_right_hip_motor,
    ):
        motor.spin_to_position(Constants.hip_idle, DEGREES, wait=False)

    for motor in (
        front_left_knee_motor,
        front_right_knee_motor,
        back_left_knee_motor,
        back_right_knee_motor,
    ):
        motor.spin_to_position(Constants.knee_idle, DEGREES, wait=False)
