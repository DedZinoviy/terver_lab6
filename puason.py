import numpy as np
from density import getTheoreticFrequency

def getDensity(lamb):
    '''Возращает строковое представление плотности со значениями'''
    densityPatern = "(%g^xᵢ)•exp(-%g)/xᵢ!"
    density = densityPatern % (lamb, lamb)
    return density


def getPropabilities(groupedSerias, lamb):
    propabilities = []
    for xi in groupedSerias:
        propability = (lamb ** xi * np.exp(-lamb)) / np.math.factorial(xi)
        propabilities.append(propability)
    return propabilities

def main():
    print(getDensity(2.3))

    groupedSerias = [0, 1, 2, 3, 4, 5]
    frequancy = [6, 24, 32, 18, 12, 8]

    print(groupedSerias, frequancy)

    propabilities = getPropabilities(groupedSerias, 2.3)
    print(getTheoreticFrequency(propabilities, frequancy))


main()