import argparse
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from networkObj import Network
from interactions import Interaction
from substrate import Substrate
import storeIt
import openIt
import pickle

parser = argparse.ArgumentParser(description='change the values of substrates or interactions')
parser.add_argument('-i', '-input', help='input pickle file path', required=True)

# essentially can edit any of the substrate or interaction object attributes

def openTheNetwork(filePath):
    return openIt.openNetwork(filePath)

def editSubstrate(network, name, storeFile=None, substrateType=None, initialValue=None, phosRate=None, dephosRate=None, maxValue=None, timeStart=None, timeEnd=None, currentValue=None):
    for substrate in network.substrates:
        if substrate.name == name:
            if substrateType != None:
                substrate.substrateType = substrateType
            if initialValue != None:
                substrate.initialValue = initialValue
            if phosRate != None:
                substrate.phosRate = phosRate
            if dephosRate != None:
                substrate.dephosRate = dephosRate
            if maxValue != None:
                substrate.maxValue = maxValue
            if timeStart != None:
                substrate.timeStart = timeStart
            if timeEnd != None:
                substrate.timeEnd = timeEnd
            if currentValue != None:
                substrate.currentValue = currentValue
            print('Substrate Successfully Edited')
        else:
            continue
    if storeFile == None:
        return network
    else:
        storeIt.saveIt(network, storeFile)

def editInteraction(network, substrate1Name, substrate2Name, storeFile=None, behavior=None, rate=None):
    for interaction in network.interactions:
        if interaction.substrate1.name == substrate1Name and interaction.substrate2.name == substrate2Name:
            if behavior != None:
                interaction.behavior = behavior
            if rate != None:
                interaction.rate = float(rate)
            print('Interaction Successfully Edited!')
        else:
            continue
    if storeFile == None:
        return network
    else:
        storeIt.saveIt(network, storeFile)

def addSubstrate():
    return None
