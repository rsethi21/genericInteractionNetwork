from interactions import Interaction
from substrate import Substrate
import pdb
import pickle

class Network:
  def __init__(self, name, networkDictionary):
    self.name = name
    self.substrates = self.processSubstrates(networkDictionary)
    self.interactions = self.processInteractions(networkDictionary)

  @classmethod
  def readNetworkObject(cls, objpath):
      with open(objpath, 'rb') as file:
          return pickle.load(file)

  def processSubstrates(self, nd):
    substrates = []
    for substrateName in nd.keys():
      if nd[substrateName]['tag'] == 'protein':
        try:
          k = nd[substrateName]['phosRate']
        except:
          k = 1.0
        try:
          r = nd[substrateName]['dephosRate']
        except:
          r = -0.1
        substrate = Substrate(substrateName, nd[substrateName]['tag'], initialValue=nd[substrateName]['initialValue'], phosRate=k, dephosRate=r)
        substrates.append(substrate)
      elif nd[substrateName]['tag'] == 'stimulus':
        try:
          k = nd[substrateName]['phosRate']
        except:
          k = 1.0
        try:
          r = nd[substrateName]['dephosRate']
        except:
          r = -0.1
        substrate = Substrate(substrateName, nd[substrateName]['tag'], initialValue=nd[substrateName]['initialValue'], phosRate=k, dephosRate=r, maxValue=nd[substrateName]['maxValue'], timeStart=nd[substrateName]['timeStart'], timeEnd=nd[substrateName]['timeEnd'])
        substrates.append(substrate)
      else:
        print('Not a possible substrate.')
    return substrates
  
  def processInteractions(self, nd):
    finalizedInteractions = []
    for substrate in self.substrates:
      name = substrate.name
      if substrate.substrateType == 'stimulus':
        pass
      else:
        interactionList = nd[name]['interactions']
        for interaction in interactionList:
          substrate1 = [sub for sub in self.substrates if sub.name == interaction[0]][0]
          substrate2 = [sub for sub in self.substrates if sub.name == interaction[2]][0]
          behavior = interaction[1]
          try:
            rate = interaction[3]
          except:
            rate = None
          interactionObject = Interaction(substrate1, substrate2, behavior, rate)
          finalizedInteractions.append(interactionObject)
    return finalizedInteractions

  def getInitialValues(self):
    return [s.initialValue for s in self.substrates]

  def stimuliRate(self, t, timeStart, timeEnd, maxValue, value):
    if timeStart != None and timeEnd == None:
      if t >= timeStart:
        currentRate = maxValue - value
      else:
        currentRate = 0
    elif timeStart == None and timeEnd != None:
      if t <= timeEnd:
        currentRate = maxValue - value
      else:
        currentRate = -value
    else:
      if timeStart <= t <= timeEnd:
        currentRate = maxValue - value
      else:
        if t < timeStart:
          currentRate = 0
        else:
          currentRate = -value
    return currentRate

  def diffEQs(self, y, t):
    for s, yValue in zip(self.substrates, y):
      s.currentValue = yValue

    interactionDictionary = {f'{substrate.name}':[] for substrate in self.substrates}
    for interaction in self.interactions:
      interactionDictionary[interaction.substrate2.name].append(interaction)
    dydt = []
    for substrateName in interactionDictionary.keys():
      sub = [s for s in self.substrates if s.name == substrateName][0]
      if sub.substrateType != 'stimulus':
        positiveRate = sub.phosRate
        negativeRate = sub.dephosRate*sub.currentValue
        additionalRate = 0
        for interaction in interactionDictionary[substrateName]:
          if interaction.behavior == 'ur':
            if interaction.rate == None:
              positiveRate *= interaction.substrate1.currentValue
            else:
              additionalRate += interaction.rate*interaction.substrate1.currentValue
          elif interaction.behavior == 'dr':
            if interaction.rate == None:
              negativeRate *= interaction.substrate1.currentValue
            else:
              additionalRate += interaction.rate*interaction.substrate1.currentValue
          else:
            pass
        dydt.append(positiveRate+negativeRate+additionalRate)
      
      else:
        dydt.append(self.stimuliRate(t, sub.timeStart, sub.timeEnd, sub.maxValue, sub.currentValue))
    return dydt
