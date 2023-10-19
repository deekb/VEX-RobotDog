from vex import Ports, GearSetting

inertial_sensor_port = Ports.PORT9

front_left_hip_motor_port = Ports.PORT1
front_right_hip_motor_port = Ports.PORT4
back_left_hip_motor_port = Ports.PORT2
back_right_hip_motor_port = Ports.PORT3

front_left_knee_motor_port = Ports.PORT5
front_right_knee_motor_port = Ports.PORT8
back_left_knee_motor_port = Ports.PORT6
back_right_knee_motor_port = Ports.PORT7

front_left_hip_motor_gear_ratio = GearSetting.RATIO_18_1
front_right_hip_motor_gear_ratio = GearSetting.RATIO_18_1
back_left_hip_motor_gear_ratio = GearSetting.RATIO_18_1
back_right_hip_motor_gear_ratio = GearSetting.RATIO_18_1

front_left_knee_motor_gear_ratio = GearSetting.RATIO_18_1
front_right_knee_motor_gear_ratio = GearSetting.RATIO_18_1
back_left_knee_motor_gear_ratio = GearSetting.RATIO_18_1
back_right_knee_motor_gear_ratio = GearSetting.RATIO_18_1

front_left_hip_motor_inverted = False
front_right_hip_motor_inverted = True
back_left_hip_motor_inverted = True
back_right_hip_motor_inverted = False

front_left_knee_motor_inverted = True
front_right_knee_motor_inverted = False
back_left_knee_motor_inverted = False
back_right_knee_motor_inverted = True

# For tuning the PID gains, please refer to the "Tuning a PID controller" section of Utilities.md
balance_Kp = 0.5
balance_Ki = 0
balance_Kd = 0
hip_idle = 100
knee_idle = -100


class ControllerAxis(object):
    """A class for defining Controller axis constants."""
    x_axis = 0
    y_axis = 1
