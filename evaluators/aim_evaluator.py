import math

from evaluators import preprocessing
from evaluators.preprocessing import OsuDifficultyHitObject

def evaluate_aim_difficulties(curr_y_values, prev_y_values, next_y_values, prev_curr_y_values, curr_next_y_values, distance_bonus_multiplier):
    aim_difficulties = []

    for current in preprocessing.OsuDifficultyHitObject.objects:
        aim_difficulties.append(distance_difficulties(current) * distance_bonus_multiplier + angle_bonus(current, curr_y_values, prev_y_values, next_y_values, prev_curr_y_values, curr_next_y_values))

    return aim_difficulties


def distance_difficulties(current: OsuDifficultyHitObject):
    if current.index == 0:
        return 0

    base_difficulty = current.distance / current.strain_time

    return base_difficulty


def angle_bonus(current: OsuDifficultyHitObject, curr_y_values, prev_y_values, next_y_values, prev_curr_y_values, curr_next_y_values):
    if current.index < 3 or current.index == len(preprocessing.OsuDifficultyHitObject.objects) - 2:
        return 0

    curr_angle = abs(current.angle) * 180 / math.pi
    prev_angle = abs(current.previous(0).angle) * 180 / math.pi
    next_angle = abs(current.next(0).angle) * 180 / math.pi

    curr_velocity = current.distance / current.strain_time
    prev_0_velocity = current.previous(0).distance / current.previous(0).strain_time
    prev_1_velocity = current.previous(1).distance / current.previous(1).strain_time
    next_velocity = current.next(0).distance / current.next(0).strain_time

    x_values = [0, 30, 60, 90, 120, 150, 180]

    curr_angle_bonus = lerp(curr_angle, x_values, curr_y_values) * min(curr_velocity, prev_0_velocity)
    prev_angle_bonus = lerp(prev_angle, x_values, prev_y_values) * min(prev_0_velocity, prev_1_velocity)
    next_angle_bonus = lerp(next_angle, x_values, next_y_values) * min(next_velocity, curr_velocity)

    x_values_2 = [0, 60, 120, 180, 240, 300, 360]

    prev_curr_angle_bonus = lerp(curr_angle + prev_angle, x_values_2, prev_curr_y_values) * min(curr_velocity, prev_0_velocity, prev_1_velocity)
    curr_next_angle_bonus = lerp(next_angle + curr_angle, x_values_2, curr_next_y_values) * min(next_velocity, curr_velocity, prev_0_velocity)

    return curr_angle_bonus + prev_angle_bonus + next_angle_bonus + prev_curr_angle_bonus + curr_next_angle_bonus


def lerp(x, x_values, y_values):
    if len(x_values) == 0 or len(x_values) != len(y_values):
        return 0

    if x <= x_values[0]:
        return y_values[0]
    if x >= x_values[-1]:
        return y_values[-1]

    for i in range(1, len(x_values)):
        if x_values[i] >= x:
            break

    x0, x1 = x_values[i - 1], x_values[i]
    y0, y1 = y_values[i - 1], y_values[i]

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
