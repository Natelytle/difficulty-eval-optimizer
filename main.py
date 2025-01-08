
from beatmap_reader import BeatmapIO
from osu_analysis import StdMapData

import deviations
import evaluators.aim_evaluator
from evaluators import preprocessing

import numpy as np

if __name__ == '__main__':
    print("Setting up deviations")
    beatmap = BeatmapIO.open_beatmap('./maps/Example/Adust Rain - Seven Style (Ayla) [Nightmare Essence].osu')
    map_data = StdMapData.get_map_data(beatmap)

    replay_directory = './replays/Example'

    preprocessing.create_objects(map_data)
    difficulties = evaluators.aim_evaluator.evaluate_aim_difficulties([0], [0], [0], [0], [0])
    deviations.create_deviations(map_data, replay_directory)

    offset_mean = np.mean(deviations.average_offsets)
    difficulty_mean = np.mean(difficulties)

    for difficulty in difficulties:
        difficulty *= offset_mean / difficulty_mean

    zipped_deviations = list(zip(deviations.average_offsets, difficulties))

    print(zipped_deviations)