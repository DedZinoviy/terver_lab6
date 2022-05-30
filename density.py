import math
import numpy as np

def getDensity(a, sigma):
    k1 = 1 / (sigma * math.sqrt(2 * math.pi))
    k2 = -1 / (2 * math.pow(sigma, 2))

    densityPatern = "%g•exp(%g•(x-%g)²)"

    density = densityPatern % (k1, k2, a)

    return density


def densityFunction(a : float, sigma : float, x : np.ndarray) -> np.ndarray:
    k1 = 1 / (sigma * math.sqrt(2 * math.pi))
    k2 = -1 / (2 * math.pow(sigma, 2))
    y = []

    for xi in x:
        y.append(k1 * np.exp(k2 * math.pow((xi - a), 2)))

    return np.array(y)


def mergeIntervals(intervals, frequency):
    intervalsAmount = len(intervals)

    i = 0
    while(i < intervalsAmount):
        
        if (frequency[i] < 5):
            removedFrequency = frequency.pop(i)
            removedInterval = intervals.pop(i)
            intervalsAmount -= 1

            if (i == intervalsAmount):
                i -= 1
                intervals[i][1] = removedInterval[1]
            else:
                intervals[i][0] = removedInterval[0]
            
            frequency[i] += removedFrequency
        
        else:
            i += 1