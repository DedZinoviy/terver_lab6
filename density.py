from code import interact
import math
import numpy as np
from scipy import integrate

def getDensity(a, sigma):
    '''Возращает строковое представление плотности со значениями'''
    k1 = 1 / (sigma * math.sqrt(2 * math.pi))
    k2 = -1 / (2 * math.pow(sigma, 2))

    densityPatern = "%g•exp(%g•(x-%g)²)"

    density = densityPatern % (k1, k2, a)

    density = density.replace("--","•")

    return density


def densityFunction(a : float, sigma : float, x : np.ndarray) -> np.ndarray:
    '''Функция расчёта значений функции в точках Х'''
    k1 = 1 / (sigma * math.sqrt(2 * math.pi))
    k2 = -1 / (2 * math.pow(sigma, 2))
    y = []

    for xi in x:
        y.append(k1 * np.exp(k2 * math.pow((xi - a), 2)))

    return np.array(y)


def mergeIntervals(intervals, frequency):
    '''Функция объединения интервало: объединяет интервалы, если частота меньше 5'''
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
        
        return intervalsAmount


def transformBorders(bordersList, a, sigma):
    '''Функция преобразования границ интервалов'''
    for interval in bordersList:
        interval[0] = round((interval[0] - a)/sigma,4)
        interval[1] = round((interval[1] - a)/sigma,4)
    
    bordersList[0][0] = -np.Infinity
    bordersList[len(bordersList) - 1][1] = np.Infinity


def getPropabilities(transformedIntervals):
    '''Функция вычисления вероятностей'''
    propabilities = []
    for interval in transformedIntervals:
        propability, err = integrate.quad(propabilityFunction, interval[0], interval[1]) #зачем тут err, я не знаю, но без него не работает :)
        propability *= 1 / np.sqrt(2 * np.pi)
        propabilities.append(round(propability,4))
    return propabilities


def propabilityFunction(x):
    return np.exp(-x ** 2 / 2)


def getTheoreticFrequency(propabilities, frequency):
    n = sum(frequency)
    theoreticFrequency = [n * p for p in propabilities]
    return theoreticFrequency


def main():
    '''Тест из методички'''
    intervals = [[40, 42], [42, 44], [44, 46], [46, 48], [48, 50]]
    frequency = [8, 25, 35, 22, 10]
    a = 45.02
    sigma = 2.182

    mergeIntervals(intervals, frequency)

    transformBorders(intervals, a, sigma)

    propabilities = getPropabilities(intervals)

    print(frequency)
    print(getTheoreticFrequency(propabilities, frequency))