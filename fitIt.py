# implementation of genetic algorithm
    # later can add other heuristic/approaches
from dataclasses import dataclass
import argparse
from tqdm import tqdm
import openIt
import modifyIt
from scipy.integrate import odeint
import math
import pandas


class runGA:
    # geneticalgorithm or pyGAD based implementation
    
@dataclass
class Gen:
    genNum: int
    population: list
    scores: list
    parents: list = None
    children: list = None
    newpopulation: list = None

    def newPop(self):
        return

    def createDF(self):
        return

class geneticAlgo:
    def __init__(self, network, data, time, crossRate=0.8, mutRate=0.1, numGens=30, numparents=14, constraints=None):
        self.network = network
        self.data = data
        self.time = time
        self.ratesDict = {}
        self.crossRate = crossRate
        self.mutRate = mutRate
        self.numGens = numGens
        self.initialpopulation = []
        self.numparents = numparents
        self.numInds = math.comb(numparents, 2) + numparents
        self.constraints = constraints
        self.pastGens = []

    def initialPopulation(self):
        ratesDictionary = {}
        for s in self.network.substrates:
            k = s.phosRate
            r = s.dephosRate
            if s.name not in ratesDictionary.keys():
                ratesDictionary[f'k_for_{s.name}'] = k
                ratesDictionary[f'r_for_{s.name}'] = r
            else:
                pass

        for i in self.network.interactions:
            rate = i.rate
            if rate == None:
                continue
            else:
                if rate < 0:
                    identity = f'{i.substrate1.name}-|{i.substrate2.name}'
                else:
                    identity = f'{i.substrate1.name}->{i.substrate2.name}'
            if identity not in ratesDictionary.keys():
                ratesDictionary[identity] = rate
            else:
                pass
        population = list(ratesDictionary.values()) # add more
        self.ratesDict = ratesDictionary
        self.initialpopulation = population

    def adjustModel(self, rates):
        y = None
        keys = list(self.ratesDict.keys())
        for i, r in enumerate(rates):
            # need some way to identify what rate each index applies to
            # need to change indices from one to looking for the spaces for adaptability to longer names
            key = keys[i]
            if key[0] == 'k':
                subs = key[-1]
                for s in self.network.substrates:
                    if subs == s.name:
                        s.phosRate = r
            elif key[0] == 'r':
                subs = key[-1]
                for s in self.network.substrates:
                    if subs == s.name:
                        s.dephosRate = r
            else:
                sub1 = key[0]
                sub2 = key[3]
                for i in self.network.interactions:
                    if i.substrate1 == sub1 and i.substrate2 == sub2:
                        i.rate = r

        y0 = self.network.getInitialValues()
        y = odeint(self.network.diffEQs, y0, self.time) 

        return y

    def cost(self, new_y):
        metadata = [s.name for s in self.network.substrates]
        rss = 0
        for key, value in self.data.items():
            index = metadata.index(key)
            for tup in value:
                time = tup[0]
                quant = tup[1]
                cost = (quant - new_y[time, index])**2
                rss += cost
        return rss

    def selection(self, df):
        sortedPop = 0
        return

    def mating(self, parents):
        return

    def mutation(self, children):
        return

    def convergence():
        return

    def goodnessOfFit():
        return

    def run(self):
        # rethink, probably won't need this part
        
        # for individual in initialpop:
        #     y = self.adjustModel(individual)
        #     initialCosts = self.cost(y)
        #     initialGen = Gen(0, initialpop, initialCosts)
        # df = initialGen.createDF()
        # parents = self.selection(df)
        # children = self.mating(parents)
        # children = self.mutation(children)
        # initialGen.parents = parents
        # initialGen.children = children
        # self.pastGens.append(initialGen)

        for i in range(self.numGens+1):
            try:
                pastGen = self.pastGens[i-1]
            except:
                initialpop = self.initialpopulation()
                initialGen = Gen(0, initialpop, None)
                self.pastGens.append(initialGen)
                
            nextGen = None
            
            newpopulation = pastGen.newPop()
            for inidivudal in newpopulation:
                y = self.adjustModel(individual)
                costs = self.cost(y)
                nextGen = Gen(i,newpopulation, costs)
            newdf = 
