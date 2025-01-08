
from osu_analysis import StdMapData
from osu_analysis import StdMapMetrics

def create_objects(map_data):
    press_filter = map_data['type'] == StdMapData.TYPE_PRESS
    map_data = map_data[press_filter]

    dnc, dist = StdMapMetrics.calc_path_dist(map_data)
    dist = [None] + dist.tolist()
    dnc, angle = StdMapMetrics.calc_angles(map_data)
    angle = [None, None] + angle.tolist()
    time = StdMapData.all_times(map_data)

    index = 0

    while index < len(time):
        OsuDifficultyHitObject.objects.append(OsuDifficultyHitObject(dist, time, angle, index))
        index += 1

class OsuDifficultyHitObject:
    objects = []

    distance = None
    angle = None
    strain_time = None
    index = -1

    def __init__(self, note_distances, start_times, angles, index):
        self.distance = note_distances[index]
        self.angle = angles[index]
        self.index = index

        if index > 0:
            self.strain_time = max(25, start_times[0] - start_times[1])

    def previous(self, backwards_index):
        index = self.index - (backwards_index + 1)
        return self.objects[index]

    def next(self, forwards_index):
        index = self.index - (forwards_index + 1)
        return self.objects[index]


