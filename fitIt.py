# implementation of genetic algorithm
    # later can add other heuristic/approaches
import argparse
from tqdm import tqdm
import openIt
import modifyIt
import odeint


class geneticAlgo:
    def __init__(self, network, data, time, crossRate=0.8, mutRate=0.1, numGens=10, numInds=10, constraints=None):
        self.network = network
        self.data = data
        self.ratesDict = {}
        self.crossRate = crossRate
        self.mutRate = mutRate
        self.numGens = numGens
        self.numInds = numInds
        self.initialpopulation = []
        self.constraints = constraints

    def intialPopulation(self):
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
            key = keys[i]
            self.ratesDict[]
        return y

    def cost(self, new_y):
        metadata = [s.name for s in self.network.substrates]
        modifyIt.editSubstrate(self.network)
        rss = 0
        for key, value in self.data:
            index = metadata.find(key)
            time = value[0]
            quant = value[1]
            cost = (quant - new_y[time, index])**2
            rss += cost
        return rss

    def selection():
        return

    def mating():
        return

    def mutation():
        return

    def convergence():
        return

    def goodnessOfFit():
        return

    def run():
        return
