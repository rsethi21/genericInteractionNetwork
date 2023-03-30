from interactions import Interaction
from substrate import Protein
from substrate import Enzyme
from substrate import Influence
import storeIt
import graphIt
import modifyIt
import pdb
import graphviz
import ipywidgets
import pdb

class Network:
  def __init__(self, name, networkDictionary):
    self.name = name
    self.substrates = self.processSubstrates(networkDictionary)
    self.interactions = self.processInteractions(networkDictionary)
    self.expressions = self.rateExpressions()
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
    # fix this in terms of new labels
    ratesDictionary = {}
    for s in self.substrates:
      if s.substrateType == 'enzyme':
        k = s.phosRate
        r = s.dephosRate
        if s.name not in ratesDictionary.keys():
          ratesDictionary[f'k_for_{s.name}'] = k
          ratesDictionary[f'r_for_{s.name}'] = r
        else:
          pass
      elif s.substrateType == 'protein':
        k = s.transRate
        r = s.degradRate
        if s.name not in ratesDictionary.keys():
          ratesDictionary[f'k_for_{s.name}'] = k
          ratesDictionary[f'r_for_{s.name}'] = r
      elif s.substrateType == 'stimulus':
        i = s.initialValue
        m = s.maxValue
        start = s.timeStart
        end = s.timeEnd
        if s.name not in ratesDictionary.keys():
          ratesDictionary[f'max_for_{s.name}'] = m
          ratesDictionary[f'initial_for_{s.name}'] = i
          ratesDictionary[f'start_for_{s.name}'] = start
          ratesDictionary[f'end_for_{s.name}'] = end

    for i in self.interactions:
      rate = i.rate
      if rate == None:
        continue
      else:
        if rate < 0:
          identity = f'rate for {i.substrate1.name}-|{i.substrate2.name}'
        else:
          identity = f'rate for {i.substrate1.name}->{i.substrate2.name}'
        if identity not in ratesDictionary.keys():
          ratesDictionary[identity] = rate
        else:
          pass

    inputDictionary = {}

    for key, value in ratesDictionary.items():
      if key[0:2] == 'k_' or key[0:2] == 'r_' or key.startswith('rate') == True:
        if value < 0:
          inputDictionary[key] = ipywidgets.FloatSlider(value=value, min=-10.0, max=0.0, step=-0.1, description=key, readout=True)
        else:
          inputDictionary[key] = ipywidgets.FloatSlider(value=value, min=0, max=10.0, step=0.1, description=key, readout=True)
      else:
        inputDictionary[key] = ipywidgets.FloatText(value=value, description=key)

    def adjust(filepath=None, saveWidget=False, resetWidget=False, graphWidget=False, **parameters):
        if resetWidget == True:
          parameters = ratesDictionary
          print("Parameters reset in network!")

        for key, value in parameters.items():
          if key[0:2] == 'k_':
            subs = key[key.rindex('_')+1:]
            for s in self.substrates:
              if subs == s.name:
                try:
                  s.phosRate = value
                except:
                  s.transRate = value
          elif key[0:2] == 'r_':
            subs = key[key.rindex('_')+1:]
            for s in self.substrates:
              if subs == s.name:
                try:
                  s.dephosRate = value
                except:
                  s.degradRate = value
          elif key.startswith('rate') == True:
            index1 = key.find('for ')
            index2 = key.find('-')
            sub1 = key[index1+4:index2]
            sub2 = key[index2+2:]
            for i in self.interactions:
              if i.substrate1 == sub1 and i.substrate2 == sub2:
                i.rate = rate
          else:
            # add the stimulus stuff to this
            index = key.rindex('_')
            index2 = key.index('_')
            subs = key[index+1:]
            for s in self.substrates:
              if subs == s.name:
                item = key[:index2]
                if item == 'max':
                  s.maxValue = value
                elif item == 'initial':
                  s.initialValue = value
                elif item == 'start':
                  s.timeStart = value
                elif item == 'end':
                  s.timeEnd = value

        if graphWidget == True:
          graphIt.plot(self)
          print(ratesDictionary)
    # graphIt
        
        if saveWidget == True:
            if filepath != None:
                storeIt.saveIt(self, filepath)
                return
            else:
                print("Enter Filepath!")

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
    disabled=False, button_style='', icon='check'), graphWidget=ipywidgets.ToggleButton(value=False,
    description='Graph',
    disabled=False, button_style='', icon='check'), **inputDictionary)

  def processSubstrates(self, nd):
    substrates = []
    for substrateName in nd.keys():
      if nd[substrateName]['tag'] == 'enzyme':
        
        try:
          k = nd[substrateName]['phosRate']
        except:
          k = 1.0
        try:
          r = nd[substrateName]['dephosRate']
        except:
          r = -0.1
        substrate = Enzyme(substrateName, initialValue=nd[substrateName]['initialValue'], phosRate=k, dephosRate=r)
        substrates.append(substrate)
      elif nd[substrateName]['tag'] == 'stimulus':
        substrate = Influence(substrateName, initialValue=nd[substrateName]['initialValue'], maxValue=nd[substrateName]['maxValue'], timeStart=nd[substrateName]['timeStart'], timeEnd=nd[substrateName]['timeEnd'])
        substrates.append(substrate)
      elif nd[substrateName]['tag'] == 'protein':
        try:
          k = nd[substrateName]['transRate']
        except:
          k = 1.0
        try:
          r = nd[substrateName]['degradRate']
        except:
          r = -0.1
        substrate = Protein(substrateName, initialValue=nd[substrateName]['initialValue'], degradRate=r, transRate=k)
        substrates.append(substrate)
      else:
        print('Not a possible substrate. Make sure tags are all lower-case.')
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


  def rateExpressions(self):
    
    interactionDictionary = {f'{substrate.name}':[] for substrate in self.substrates}
    
    for interaction in self.interactions:
      interactionDictionary[interaction.substrate2.name].append(interaction)
    
    dydt = []
    
    for substrateName in interactionDictionary.keys():
      sub = [s for s in self.substrates if s.name == substrateName][0]
      
      if sub.substrateType == 'enzyme':
      # change this to create the rate for the opposite inactivate form
        positiveRate = "k"
        negativeRate = f"r{sub.name}"
        additionalRate = ""
        # otherFormRate = {}
        for interaction in interactionDictionary[substrateName]:
          if interaction.behavior == 'ur':
            if interaction.rate == None:
              positiveRate += interaction.substrate1.name
            else:
              additionalRate += f"s{interaction.substrate1.name}"
          elif interaction.behavior == 'dr':
            if interaction.rate == None:
              negativeRate += interaction.substrate1.name
            else:
              additionalRate += f"d{interaction.substrate1.name}"
          else:
            pass
        if additionalRate != "":
            dydt.append(f"d{sub.name}/dt = {positiveRate} + {negativeRate} + {additionalRate}")
        else:
            dydt.append(f"d{sub.name}/dt = {positiveRate} + {negativeRate}")

      elif sub.substrateType == 'protein':
        positiveRate = "k"
        negativeRate = f"r{sub.name}"
        additionalRate = ""
        for interaction in interactionDictionary[substrateName]:
          if interaction.behavior == 'ur':
            if interaction.rate == None:
              positiveRate += interaction.substrate1.name
            else:
              additionalRate += f"s{interaction.substrate1.name}"
          elif interaction.behavior == 'dr':
            if interaction.rate == None:
              negativeRate += interaction.substrate1.name
            else:
              additionalRate += f"d{interaction.substrate1.name}"
          else:
            pass
        if additionalRate != "":
            dydt.append(f"d{sub.name}/dt = {positiveRate} + {negativeRate} + {additionalRate}")
        else:
            dydt.append(f"d{sub.name}/dt = {positiveRate} + {negativeRate}")
      
      else:
        dydt.append(f"d{sub.name}/dt = 0")

    return dydt


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
      
      if sub.substrateType == 'enzyme':
      # change this to create the rate for the opposite inactivate form
        positiveRate = sub.phosRate
        negativeRate = sub.dephosRate*sub.currentValue
        additionalRate = 0
        # otherFormRate = {}
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

      elif sub.substrateType == 'protein':
        positiveRate = sub.transRate
        negativeRate = sub.degradRate*sub.currentValue
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

  def networkGraph(self, name, directory):
    ng = graphviz.Digraph(name, format='pdf')
    for interaction in self.interactions:
      n1 = interaction.substrate1.name
      n2 = interaction.substrate2.name
      if interaction.behavior == 'dr':
        ng.edge(n1, n2, color='red')
      else:
        ng.edge(n1, n2, color='green')
    ng.render(directory=directory)
    print(f'Network diagram saved to {directory}!')



 # try:
          # fix this to incorporate opposite enzyme
          #   if substrateName == nd[substrateName]['active'][0]:
          #     form = 'active'
          #     substrate = Enzyme(substrateName, otherFormName=nd[substrateName]['inactive'][0], initialValue=nd[substrateName]['active'][1], phosRate=k, dephosRate=r, form=form)
          #     substrate2 = Enzyme(nd[substrateName]['inactive'][0], otherFormName=substrateName, initialValue=nd[substrateName]['inactive'][1], phosRate=-1*r, dephosRate=-1*k, form='inactive')
          #     substrates.append(substrate, substrate2)
          #   else:
          #     form = 'inactive'
          #     substrate = Enzyme(substrateName, otherFormName=nd[substrateName]['active'][0], initialValue=nd[substrateName]['initialValue'], phosRate=k, dephosRate=r, form=form)
          #     substrate2 = Enzyme(nd[substrateName]['active'][0], otherFormName=substrateName, initialValue=nd[substrateName]['active'][1], phosRate=-1*r, dephosRate=-1*k, form='active')
          #     substrates.append(substrate, substrate2)
          # except:
          #   form = None
