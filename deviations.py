import math
import os
import numpy as np
from replay_reader import ReplayIO
from osu_analysis import StdReplayData, StdScoreData, StdReplayMetrics, StdScoreMetrics, StdMapData

average_offsets = []

def create_deviations(map_data, replay_directory):
    global average_offsets

    press_filter = map_data['type'] == StdMapData.TYPE_PRESS
    map_data = map_data[press_filter]

    score_data_list = []

    settings = StdScoreData.Settings()
    settings.pos_hit_range = 35  # ms point of late hit window
    settings.neg_hit_range = 35  # ms point of early hit window
    settings.pos_hit_miss_range = 35  # ms point of late miss window
    settings.neg_hit_miss_range = 35  # ms point of early miss window

    for replay_file in os.scandir(replay_directory):
        if replay_file.is_file():
            replay = ReplayIO.open_replay(replay_file.path)
            replay_data = StdReplayData.get_replay_data(replay)
            score_data = StdScoreData.get_score_data(replay_data, map_data, settings)
            score_data_list.append(score_data)
            print(f"added {replay_file.path}")

    # get the data per-object
    per_hitobject_data = StdScoreMetrics.get_per_hitobject_score_data(score_data_list)

    index = 0

    while index < len(per_hitobject_data):
        average_offsets.append(0)

        i2 = 0
        div = 0

        while i2 < len(per_hitobject_data[index][2]):
            if not math.isnan(per_hitobject_data[index][i2][2]):
                average_offsets[index] = (average_offsets[index] * i2 + square_distance(per_hitobject_data[index][i2][2] - per_hitobject_data[index][i2][4], per_hitobject_data[index][i2][3] - per_hitobject_data[index][i2][5])) / (i2 + 1)
                div += 1
            i2 += 1

        index += 1

    offsets_index = 0

    while offsets_index < len(average_offsets):
        average_offsets[offsets_index] = average_offsets[offsets_index]**0.5
        offsets_index += 1


def square_distance(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


def square_distance(x_dist, y_dist):
    return x_dist**2 + y_dist