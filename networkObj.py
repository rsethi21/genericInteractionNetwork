from interactions import Interaction
from substrate import Substrate
import storeIt
import modifyIt
import pdb
import graphviz
import ipywidgets

class Network:
  def __init__(self, name, networkDictionary):
    self.name = name
    self.substrates = self.processSubstrates(networkDictionary)
    self.interactions = self.processInteractions(networkDictionary)
    self.values = {'y': {}, 'dydt': {}}

#  def findSteadyState(self):
#    roc = self.values['dydt']
#    checkList = [0.000001 for i in range(len(self.substrates))]
#    confirmList = [True for i in range(len(self.substrates))]
#    for t in roc.keys():
#        testList = [value < checkValue for value, checkValue in zip(roc[t], checkList)]
#        if t == 0:
#            pass
#        elif testList == confirmList:
#            return t
#    return 'Unable to find steady state.'

  def runInteractiveMode(self):
    ratesDictionary = {}
    for s in self.substrates:
      k = s.phosRate
      r = s.dephosRate
      if s.name not in ratesDictionary.keys():
        ratesDictionary[f'k_for_{s.name}'] = k
        ratesDictionary[f'r_for_{s.name}'] = r
      else:
        pass

    for i in self.interactions:
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

    inputDictionary = {}

    for key, value in ratesDictionary.items():
      if value < 0:
        inputDictionary[key] = ipywidgets.FloatSlider(value=value, min=-10.0, max=0.0, step=-0.1, description=key, readout=True)
      else:
        inputDictionary[key] = ipywidgets.FloatSlider(value=value, min=0, max=10.0, step=0.1, description=key, readout=True)

    
    
    

    def adjust(filepath=None, saveWidget=False, resetWidget=False, **parameters):
        for key, value in parameters.items():
        if key[0] == 'k':
          subs = key[-1]
          for s in self.substrates:
            if subs == s.name:
              s.phosRate = value
        elif key[0] == 'r':
          subs = key[-1]
          for s in self.substrates:
            if subs == s.name:
              s.dephosRate = value
        else:
          sub1 = key[0]
          sub2 = key[3]
          for i in self.interactions:
            if i.substrate1 == sub1 and i.substrate2 == sub2:
              i.rate = rate
    # graphIt
        
        

        if saveWidget == True:
            if filepath != None:
                storeIt.saveIt(self, filepath)
                return
            else:
                print("Enter Filepath!")
      
        if resetWidget == True:
            adjust(**ratesDictionary)

    return ipywidgets.interact(adjust, filepath=ipywidgets.Text(value=None,
    placeholder='path/to/file',
    description='Filepath:',
    disabled=False), saveWidget = ipywidgets.ToggleButton(value=False,
    description='Save',
    disabled=False,
    button_style='',
    tooltip='Description',
    icon='check'
), resetWidget=ipywidgets.ToggleButton(value=False,
    description='Reset',
    disabled=False, button_style='', icon='check'), **inputDictionary)

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
    
    self.values['y'][t] = y

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

    self.values['dydt'][t] = dydt

    return dydt

  def networkGraph(self, name):
    ng = graphviz.Digraph(name, format='pdf')
    for interaction in self.interactions:
      n1 = interaction.substrate1.name
      n2 = interaction.substrate2.name
      if interaction.behavior == 'dr':
        ng.edge(n1, n2, color='red')
      else:
        ng.edge(n1, n2, color='green')
    ng.render()
    print(f'Network diagram saved to {name}.pdf!')
