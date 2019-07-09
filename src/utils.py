
import time
import random
import math

def boolean_from_random(stat):
    rand = random.random() * 100 #0.524879654422 * 100 => 52.2454865456%
    return rand <= stat


def index_from_random(array):
    # Array must be made of numbers
    rand = random.random() * 100
    sum = 0
    for i in range(len(array)):
        sum += array[i]
        if rand <= sum:
            return i
    
    raise Exception("Provided array sum isn't equal to 100%")

def profile_distances_from_array(profile, array):
    distances = list()
    for interest in array:
        sum = 0
        for key in interest['profile'].keys():
            sum += math.pow(profile[key] - interest['profile'][key], 2)
        interest['distance'] = math.sqrt(sum)
        distances.append(interest)
    return distances

def timer(func):
    def wrapper(*args, **kwargs):
        time_start = time.clock()
        ret = func(*args, **kwargs)
        time_end = time.clock()
        print('%s %ds' % (func.__name__, time_end-time_start))
        return ret
    return wrapper
