from operator import truediv
from xmlrpc.server import SimpleXMLRPCDispatcher
import numpy as np
from collections import defaultdict

"""Таблица крит значений Хи квадрат Пирсона"""
# 0.995 0.99 0.975, 0.95, 0.9, 0.75, 0.5, 0.25, 0.1, 0.05, 0.025, 0.01
one = {0.995 : 0.000039, 0.99 : 0.00016, 0.975 : 0.00098, 0.95 : 0.0039, 0.9 : 0.016, 0.75 : 0.102, 0.5 : 0.455, 0.25 : 1.32, 0.1 : 2.71, 0.05 : 3.84, 0.025 : 5.02, 0.01 : 6.63, 0.005 : 7.88, 0.001 : 10.8}
two = {0.995 : 0.01, 0.99 : 0.02, 0.975 : 0.051, 0.95 : 0.103, 0.9 : 0.211, 0.75 : 0.575, 0.5 : 1.39, 0.25 : 2.77, 0.1 : 4.61, 0.05 : 5.99, 0.025 : 7.38, 0.01 : 9.21, 0.005 : 10.6, 0.001 : 13.8}
three = {0.995 : 0.072, 0.99 : 0.115, 0.975 : 0.216, 0.95 : 0.352, 0.9 : 0.584, 0.75 : 1.21, 0.5 : 2.37, 0.25 : 4.11, 0.1 : 6.25, 0.05 : 7.81, 0.025 : 9.35, 0.01 : 11.3, 0.005 : 12.8, 0.001 : 16.3}
four = {0.995 : 0.207, 0.99 : 0.297, 0.975 : 0.484, 0.95 : 0.711, 0.9 : 1.06, 0.75 : 1.92, 0.5 : 3.36, 0.25 : 5.39, 0.1 : 7.78, 0.05 : 9.49, 0.025 : 11.1, 0.01 : 13.3, 0.005 : 14.9, 0.001 : 18.5}
five = {0.995 : 0.412, 0.99 : 0.554, 0.975 : 0.831, 0.95 : 1.15, 0.9 : 1.61, 0.75 : 2.67, 0.5 : 4.35, 0.25 : 6.63, 0.1 : 9.24, 0.05 : 11.1, 0.025 : 12.8, 0.01 : 15.1, 0.005 : 16.7, 0.001 : 20.5}
six = {0.995 : 0.676, 0.99 : 0.872, 0.975 : 1.24, 0.95 : 1.64, 0.9 : 2.2, 0.75 : 3.45, 0.5 : 5.35, 0.25 : 7.84, 0.1 : 10.6, 0.05 : 12.6, 0.025 : 14.4, 0.01 : 16.8, 0.005 : 18.5, 0.001 : 22.5}
seven = {0.995 : 0.989, 0.99 : 1.24, 0.975 : 1.69, 0.95 : 2.17, 0.9 : 2.83, 0.75 : 4.25, 0.5 : 6.35, 0.25 : 9.04, 0.1 : 12, 0.05 : 14.1, 0.025 : 16, 0.01 : 18.5, 0.005 : 20.3, 0.001 : 24.3}
eight = {0.995 : 1.34, 0.99 : 1.65, 0.975 : 2.18, 0.95 : 2.73, 0.9 : 3.49, 0.75 : 5.07, 0.5 : 7.34, 0.25 : 10.2, 0.1 : 13.4, 0.05 : 15.5, 0.025 : 17.5, 0.01 : 20.1, 0.005 : 22, 0.001 : 26.1}
nine = {0.995 : 1.73, 0.99 : 2.09, 0.975 : 2.7, 0.95 : 3.33, 0.9 : 4.17, 0.75 : 5.9, 0.5 : 8.34, 0.25 : 11.4, 0.1 : 14.7, 0.05 : 16.9, 0.025 : 19, 0.01 : 21.7, 0.005 : 23.6, 0.001 : 27.9}
ten = {0.995 : 2.16, 0.99 : 2.56, 0.975 : 3.25, 0.95 : 3.94, 0.9 : 4.87, 0.75 : 6.74, 0.5 : 9.34, 0.25 : 12.5, 0.1 : 16, 0.05 : 18.3, 0.025 : 20.5, 0.01 : 23.2, 0.005 : 25.2, 0.001 : 29.6}
eleven = {0.995 : 2.6, 0.99 : 3.05, 0.975 : 3.82, 0.95 : 4.57, 0.9 : 5.58, 0.75 : 7.58, 0.5 : 10.3, 0.25 : 13.7, 0.1 : 17.3, 0.05 : 19.7, 0.025 : 21.9, 0.01 : 24.7, 0.005 : 26.8, 0.001 : 31.3}
twelve = {0.995 : 3.07, 0.99 : 3.57, 0.975 : 4.4, 0.95 : 5.23, 0.9 : 6.3, 0.75 : 8.44, 0.5 : 11.3, 0.25 : 14.8, 0.1 : 18.5, 0.05 : 21, 0.025 : 23.3, 0.01 : 26.2, 0.005 : 28.3, 0.001 : 32.9}
thirteen = {0.995 : 3.57, 0.99 : 4.11, 0.975 : 5.01, 0.95 : 5.89, 0.9 : 7.04, 0.75 : 9.3, 0.5 : 12.3, 0.25 : 16, 0.1 : 19.8, 0.05 : 22.4, 0.025 : 24.7, 0.01 : 27.7, 0.005 : 29.8, 0.001 : 34.5}
fourteen = {0.995 : 4.07, 0.99 : 4.66, 0.975 : 5.63, 0.95 : 6.57, 0.9 : 7.79, 0.75 : 10.2, 0.5 : 13.3, 0.25 : 17.1, 0.1 : 21.1, 0.05 : 23.7, 0.025 : 26.1, 0.01 : 29.1, 0.005 : 31.3, 0.001 : 36.1}
fifteen = {0.995 : 4.6, 0.99 : 5.23, 0.975 : 6.26, 0.95 : 7.26, 0.9 : 8.55, 0.75 : 11, 0.5 : 14.3, 0.25 : 18.2, 0.1 : 22.3, 0.05 : 25, 0.025 : 27.5, 0.01 : 30.6, 0.005 : 32.8, 0.001 : 37.7}
sixteen = {0.995 : 5.14, 0.99 : 5.81, 0.975 : 6.91, 0.95 : 7.96, 0.9 : 9.31, 0.75 : 11.9, 0.5 : 15.3, 0.25 : 19.4, 0.1 : 23.5, 0.05 : 26.3, 0.025 : 28.8, 0.01 : 32, 0.005 : 34.3, 0.001 : 39.3}
seventeen = {0.995 : 5.7, 0.99 : 6.41, 0.975 : 7.56, 0.95 : 8.67, 0.9 : 10.1, 0.75 : 12.8, 0.5 : 16.3, 0.25 : 20.5, 0.1 : 24.8, 0.05 : 27.6, 0.025 : 30.2, 0.01 : 33.4, 0.005 : 35.7, 0.001 : 40.8}
eighteen = {0.995 : 6.26, 0.99 : 7.01, 0.975 : 8.23, 0.95 : 9.39, 0.9 : 10.9, 0.75 : 13.7, 0.5 : 17.3, 0.25 : 21.6, 0.1 : 26, 0.05 : 28.9, 0.025 : 31.5, 0.01 : 34.8, 0.005 : 37.2, 0.001 : 42.3}
nineteen = {0.995 : 6.84, 0.99 : 7.63, 0.975 : 8.91, 0.95 : 10.1, 0.9 : 11.7, 0.75 : 14.6, 0.5 : 18.3, 0.25 : 22.7, 0.1 : 27.2, 0.05 : 30.1, 0.025 : 32.9, 0.01 : 36.2, 0.005 : 38.6, 0.001 : 43.8}
twenty = {0.995 : 7.43, 0.99 : 8.26, 0.975 : 9.59, 0.95 : 10.9, 0.9 : 12.4, 0.75 : 15.5, 0.5 : 19.3, 0.25 : 23.8, 0.1 : 28.4, 0.05 : 31.4, 0.025 : 34.2, 0.01 : 37.7, 0.005 : 40, 0.001 : 45.3}
twentyOne = {0.995 : 8.03, 0.99 : 8.9, 0.975 : 10.3, 0.95 : 11.6, 0.9 : 13.2, 0.75 : 16.3, 0.5 : 20.3, 0.25 : 24.9, 0.1 : 29.6, 0.05 : 32.7, 0.025 : 35.5, 0.01 : 38.9, 0.005 : 41.4, 0.001 : 46.8}
twentyTwo = {0.995 : 8.64, 0.99 : 9.54, 0.975 : 11, 0.95 : 12.3, 0.9 : 14, 0.75 : 17.2, 0.5 : 21.3, 0.25 : 26, 0.1 : 30.8, 0.05 : 33.9, 0.025 : 36.8, 0.01 : 40.3, 0.005 : 42.8, 0.001 : 48.3}
twentyThree = {0.995 : 9.26, 0.99 : 10.2, 0.975 : 11.7, 0.95 : 13.1, 0.9 : 14.8, 0.75 : 18.1, 0.5 : 22.3, 0.25 : 27.1, 0.1 : 32, 0.05 : 35.2, 0.025 : 38.1, 0.01 : 41.6, 0.005 : 44.2, 0.001 : 49.7}
twentyFour = {0.995 : 9.89, 0.99 : 10.9, 0.975 : 12.4, 0.95 : 13.8, 0.9 : 15.7, 0.75 : 19, 0.5 : 23.3, 0.25 : 28.2, 0.1 : 33.2, 0.05 : 36.4, 0.025 : 39.4, 0.01 : 43, 0.005 : 45.6, 0.001 : 51.2}
twentyFive = {0.995 : 10.5, 0.99 : 11.5, 0.975 : 13.1, 0.95 : 14.6, 0.9 : 16.5, 0.75 : 19.9, 0.5 : 24.3, 0.25 : 29.3, 0.1 : 34.4, 0.05 : 37.7, 0.025 : 40.6, 0.01 : 44.3, 0.005 : 46.9, 0.001 : 52.6}
twentySix = {0.995 : 11.2, 0.99 : 12.2, 0.975 : 13.8, 0.95 : 15.4, 0.9 : 17.3, 0.75 : 20.8, 0.5 : 25.3, 0.25 : 30.4, 0.1 : 35.6, 0.05 : 38.9, 0.025 : 41.9, 0.01 : 45.6, 0.005 : 48.3, 0.001 : 54.1}
twentySeven = {0.995 : 11.8, 0.99 : 12.9, 0.975 : 14.6, 0.95 : 16.2, 0.9 : 18.1, 0.75 : 21.7, 0.5 : 26.3, 0.25 : 31.5, 0.1 : 36.7, 0.05 : 40.1, 0.025 : 43.2, 0.01 : 47, 0.005 : 49.6, 0.001 : 55.5}
twentyEight = {0.995 : 12.5, 0.99 : 13.6, 0.975 : 15.3, 0.95 : 16.9, 0.9 : 18.9, 0.75 : 22.7, 0.5 : 27.3, 0.25 : 32.6, 0.1 : 37.9, 0.05 : 41.3, 0.025 : 44.5, 0.01 : 48.3, 0.005 : 51, 0.001 : 56.9}
twentyNine = {0.995 : 13.1, 0.99 : 14.3, 0.975 : 16, 0.95 : 17.7, 0.9 : 19.8, 0.75 : 23.6, 0.5 : 28.3, 0.25 : 33.7, 0.1 : 39.1, 0.05 : 42.6, 0.025 : 45.7, 0.01 : 49.6, 0.005 : 52.3, 0.001 : 58.3}
thirty = {0.995 : 13.8, 0.99 : 15, 0.975 : 16.8, 0.95 : 18.5, 0.9 : 20.6, 0.75 : 24.5, 0.5 : 29.3, 0.25 : 34.8, 0.1 : 40.3, 0.05 : 43.8, 0.025 : 47, 0.01 : 50.9, 0.005 : 53.7, 0.001 : 59.7}


pirson = {1 : one, 2 : two, 3 : three, 4 : four, 5 : five, 6 : six, 7 : seven, 8 : eight, 9 : nine, 10 : ten, 11 : eleven, 12 : twelve, 13 : thirteen, 14 : fourteen, 15 : fifteen, 16 : sixteen, 17 : seventeen, 18 : eighteen, 19 : nineteen, 20 : twenty, 21 : twentyOne, 22 : twentyTwo, 23 : twentyThree, 24 : twentyFour, 25 : twentyFive, 26 : twentySix, 27 : twentySeven, 28 : twentyEight, 29 : twentyNine, 30 : thirty}

def khi_emp(numberOfIntervals : int, theoreticFrequenceList : list(int), empericFrequenceList : list(int)):
    '''Функция для расчёта Хи квадрат наблюдаемое'''
    khi = 0
    for i in range(0, numberOfIntervals - 1):
        khi += (pow(empericFrequenceList[i]-theoreticFrequenceList[i], 2))/theoreticFrequenceList[i]
    return khi

def isEqualKhi(empericKhi : float, criticalKhi : float):
    '''Функция сравнения Хи квадрат наблюдаемого и Хи квадрат критического'''
    if empericKhi <= criticalKhi:
        return True
    else:
        return False

print(pirson[22][0.9])