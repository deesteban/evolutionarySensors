import sys
import time

import requests
import random
import math
import os

# Parametros a modificar
N_CYCLES = 10000
individuals = 100
chromosomeSize = 384
# factor mutacion inicial
mutA = 0.01

# Variables globales
numEvals = 0
random.seed(2029250501289735059)
population = []
fitnessValues = []
matingPool = []
minGlobal = 10000
results = "min,max\n"

winningGenome = ""


def getFitnessVal(callStr):
    url = "http://memento.evannai.inf.uc3m.es/age/isidro?c="
    url += callStr
    r = requests.get(url).content
    r = r.decode("utf-8")
    result = float(r)
    global numEvals
    numEvals += 1
    return result


def selectionProcessTournament(percentage):
    value = math.floor(percentage * len(population))
    temp = 0
    minFitness = 0

    for xSPT in range(int(value)):
        randIntSPT = random.randint(0, len(population) - 1)
        if xSPT == 0:
            minFitness = fitnessValues[randIntSPT]
            temp = population[randIntSPT]
        if minFitness > fitnessValues[randIntSPT]:
            minFitness = fitnessValues[randIntSPT]
            temp = population[randIntSPT]
    matingPool.append(temp)


def matingProcess():
    global matingPool
    global population
    randIntMP = random.randint(0, chromosomeSize - 1)
    for xMP in range(individuals - 1):
        father = matingPool[xMP]
        mother = matingPool[xMP + 1]
        child1 = father[0:randIntMP]
        child1 += mother[randIntMP:len(mother)]
        child2 = mother[0:randIntMP]
        child2 += father[randIntMP:len(father)]
        matingPool[xMP] = child1
        matingPool[xMP + 1] = child2

    population = matingPool
    matingPool = []


def bestOfPopulation():
    bestPersonBP = 0
    minError = fitnessValues[0]
    for xBOP in range(len(fitnessValues)):
        if minError > fitnessValues[xBOP]:
            minError = fitnessValues[xBOP]
            bestPersonBP = xBOP
    return bestPersonBP


def getNewFitnessVals():
    for xNFV in range(individuals):
        newStrNFV = ''.join((map(str, population[xNFV])))
        fitnessValues[xNFV] = getFitnessVal(newStrNFV)


def mutate():
    global mutA
    if numEvals % 10000 == 0 and mutA > 0:
        mutA = mutA - 0.001
    for xM in range(individuals):
        for yM in range(chromosomeSize):
            randIntM = random.randint(0, 1000)
            if randIntM < mutA * 1000:
                temp = population[xM][yM]
                if temp == "0":
                    randIntMA = random.randint(0, 1)
                    if randIntMA == 0:
                        temp = 'H'
                    if randIntMA == 1:
                        temp = 'F'
                elif temp == "H":
                    randIntMA = random.randint(0, 1)
                    if randIntMA == 0:
                        temp = 0
                    if randIntMA == 1:
                        temp = 'F'
                elif temp == "F":
                    randIntMA = random.randint(0, 1)
                    if randIntMA == 0:
                        temp = 'H'
                    if randIntMA == 1:
                        temp = '0'
                population[xM][yM] = str(temp)


if __name__ == '__main__':
    print(
        "\n---------Cada 5 Ciclos se imprimira el mejor individuo global, el numero de evaluaciones y el tiempo restante del programa.\n")
    for x in range(individuals):
        population.append([])
        for y in range(chromosomeSize):
            randInt = random.randint(0, 2)
            if randInt == 1:
                randInt = 'F'
            elif randInt == 2:
                randInt = 'H'
            population[x].append(str(randInt))
        newStr = ''.join((map(str, population[x])))
        fitnessValues.append(getFitnessVal(newStr))
    start_time = time.time()
    average_time = 0
    for x in range(N_CYCLES):
        if x % 5 == 0:
            if x <= 5:
                elapsed_time = time.time() - start_time
            else:
                elapsed_time = time.time() - average_time
            remainingCycles = N_CYCLES - x
            elapsed_time = (remainingCycles * elapsed_time) / 5
            elapsed_seconds = int(elapsed_time) % 60
            elapsed_minutes = (elapsed_time / 60) % 60
            elapsed_hours = (elapsed_time / 3600) % 60
            average_time = time.time()
            print("\n---------Estimated Time Remaining %dHr:%dMin:%dSec" % (
                elapsed_hours, elapsed_minutes, elapsed_seconds))
            print("---------Ciclo " + str(x) + " El mejor global: " + str(minGlobal) + " " + winningGenome)
            print("---------Numero de Evaluaciones:  " + str(numEvals) + "\n")

        for y in range(individuals):
            selectionProcessTournament(0.05)
        matingProcess()
        mutate()
        bestPerson = bestOfPopulation()
        if fitnessValues[bestPerson] < minGlobal:
            minGlobal = fitnessValues[bestPerson]
            winningGenome = ''.join((map(str, population[bestPerson])))
        print("Ciclo " + str(x) + " El mejor este ciclo: " + str(fitnessValues[bestPerson]) + " " + ''.join(
            (map(str, population[bestPerson]))))
        results += str(min(fitnessValues)) + "," + str(max(fitnessValues)) + "\n"
        if fitnessValues[bestPerson] == 0:
            print("El minimo ha sido obtenido, con codificacion: " + ''.join(
                (map(str, population[bestPerson]))))
            break
        getNewFitnessVals()

    outputFile = open("fitnessVal-alfa2-base.csv", "w+")
    outputFile.write(results)
    outputFile.close()
