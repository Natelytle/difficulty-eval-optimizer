import math

import scipy.optimize
from beatmap_reader import BeatmapIO
from osu_analysis import StdMapData

import deviations
import evaluators.aim_evaluator
from evaluators import preprocessing

import numpy as np
from scipy.optimize import minimize

from evaluators.aim_evaluator import evaluate_aim_difficulties

best_error = math.inf

def objective_function(params):
    global best_error

    curr_y_values = params[:7]
    prev_y_values = params[7:14]
    next_y_values = params[14:21]
    prev_curr_y_values = params[21:28]
    curr_next_y_values = params[28:35]
    distance_bonus_multiplier = params[35]

    computed_aim_difficulties = evaluate_aim_difficulties(curr_y_values, prev_y_values, next_y_values, prev_curr_y_values, curr_next_y_values, distance_bonus_multiplier)

    combined_list = list(zip(computed_aim_difficulties, deviations.average_offsets))

    # Compute the squared error between computed and observed values
    error = sum((difficulty - deviation) ** 2 for difficulty, deviation in combined_list)

    if best_error > error:
        print(f"Best error: {error}")

    best_error = min(best_error, error)

    return error

if __name__ == '__main__':
    beatmap = BeatmapIO.open_beatmap('./maps/Example/Adust Rain - Seven Style (Ayla) [Nightmare Essence].osu')
    map_data = StdMapData.get_map_data(beatmap)

    print("Creating difficulty hit objects")
    preprocessing.create_objects(map_data)

    replay_directory = './replays/Example'

    print("Getting replay note error")
    deviations.create_deviations(map_data, replay_directory)

    # Define initial guesses for the values of curr_y_values, prev_y_values, next_y_values, etc.
    initial_guess = np.zeros(35)

    # Call minimize to find the optimal parameters
    result = minimize(objective_function, initial_guess, method='Nelder-Mead', options={'maxiter': np.inf, 'disp': True, 'maxfun': np.inf})

    # Extract the optimized values
    optimized_values = result.x

    # Extract the optimized arrays
    multiplier = optimized_values[0]
    optimized_curr_y_values = optimized_values[0:14]
    optimized_prev_y_values = optimized_values[14:27]
    optimized_next_y_values = optimized_values[27:40]
    optimized_prev_curr_y_values = optimized_values[40:53]
    optimized_curr_next_y_values = optimized_values[53:]

    print(result)
    print(optimized_values)

# 30506.234746786547
# [-0.29988197 -0.76875782  0.63378283  0.47458822  0.81378876 -0.59969685
#   2.46533138  1.12500366  2.4519582  -1.29403362  0.89749442  0.03397498
#   0.81412396  0.81913834  1.66114963 -0.84295065  0.75529879  1.15777942
#  -0.18238538  1.43681892  1.10477889 -0.9545547  -2.91241947 -0.3948108
#   0.07976148  0.76640801 -0.20710094  1.46424087 -1.05875852 -2.09460008
#  -0.93851227 -0.39447279  0.74903991  0.3425476  -0.12374892]

# 30506.234746782186
# [ -1.88817953  -2.35705012   0.5617955    0.55265081  -9.7285849
#    8.03368092   8.99620042   1.12500528   2.45194808  -1.0852154
#    0.50954553 -15.07708046   5.5595342    4.61012454   3.63948646
#    2.8100483   -0.77844435   1.23589769   7.89627973  -5.98769546
#    2.22821539  -0.95455612  -2.9124321   -2.53644017   1.8122581
#    3.47358344  -1.58163971   5.59591822  -1.44879813  -5.83393904
#    0.11703439  -1.53650039  -3.10283546   2.86421956   3.98399441]

# 30588.685580242254
# [-0.45899294 -0.30536024  0.60736445  0.08470523  0.54932118  0.32184534
#  -0.05300529 -1.94653474  2.3178724   0.55312054  1.29048584  0.78531118
#   1.13306187  0.96715015  2.24279288 -0.9207931   0.45017049  1.16184665
#   1.91484606  1.74533566  1.74308328  0.44033466 -0.2534292  -0.84916367
#  -0.44001534  0.25872847  0.19569879  1.00216843 -0.09250267 -0.37889358
#  -2.0125615  -2.1383017   0.25247311  2.87203951  5.06375873]

