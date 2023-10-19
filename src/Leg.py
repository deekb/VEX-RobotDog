from vex import *
import math


class Leg:
    def __init__(self, hip_motor, knee_motor, thigh_length, calf_length):
        self.hip_motor = hip_motor
        self.knee_motor = knee_motor
        self.thigh_length = thigh_length
        self.calf_length = calf_length
        self.hip_point = (0, 0)
        self.hip_motor.set_velocity(50, PERCENT)
        self.knee_motor.set_velocity(50, PERCENT)
        self.hip_motor.spin(FORWARD)
        self.knee_motor.spin(FORWARD)

    def set_hip_motor_power(self, power):
        self.hip_motor.set_velocity(power * 100, PERCENT)

    def move_hip_motor_to_position(self, position):
        self.hip_motor.spin_to_position(position, DEGREES, wait=False)

    def set_knee_motor_power(self, power):
        self.knee_motor.set_velocity(power * 100, PERCENT)

    def move_knee_motor_to_position(self, position):
        self.knee_motor.spin_to_position(position, DEGREES, wait=False)

    @staticmethod
    def _get_points_at_distance_from_center(center_point, radius, resolution=64):
        direction = 0
        direction_increment = (math.pi * 2) / resolution

        points = set()

        for point_index in range(resolution):
            direction += direction_increment

            point = (
                center_point[0] + (math.cos(direction) * radius),
                center_point[1] + (math.sin(direction) * radius),
            )

            points.add(point)

        return points

    def solve(self, position):
        costs = []

        for point in self._get_points_at_distance_from_center(
            self.hip_point, self.thigh_length, resolution=512
        ):
            direction_to_target = math.atan2(
                position[1] - point[1], position[0] - point[0]
            )

            distance = math.hypot(point[0] - position[0], point[1] - position[1])

            error = abs(distance - self.calf_length)

            costs.append((point, error))

        sorted_costs = sorted(costs, key=lambda cost: (cost[1]))

        best_knee_point = sorted_costs[0][0]
        next_best_knee_point = sorted_costs[1][0]

        best_knee_point_y = best_knee_point[1]
        next_best_knee_point_y = next_best_knee_point[1]

        if next_best_knee_point_y > best_knee_point_y:
            # Redefine the second-best solution as the best solution if it's knee point is higher than the "best" solution
            best_knee_point = next_best_knee_point_y

        angle_from_hip_to_knee_rad = math.atan2(
            best_knee_point[1] - self.hip_point[1],
            best_knee_point[0] - self.hip_point[0],
        )

        angle_from_hip_to_knee_rad += math.pi / 2

        angle_from_knee_to_foot_rad = math.atan2(
            position[1] - best_knee_point[1],
            position[0] - best_knee_point[0],
        )

        angle_from_knee_to_foot_rad += math.pi / 2

        angle_from_knee_to_foot_rad -= angle_from_hip_to_knee_rad

        angle_from_hip_to_knee_deg = math.degrees(angle_from_hip_to_knee_rad)
        angle_from_knee_to_foot_deg = math.degrees(angle_from_knee_to_foot_rad)

        self.move_hip_motor_to_position(angle_from_hip_to_knee_deg)
        self.move_knee_motor_to_position(angle_from_knee_to_foot_deg)
