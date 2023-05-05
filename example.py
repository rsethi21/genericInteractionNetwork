import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import pandas
from geneticalgorithm import geneticalgorithm as ga
import json

def simulation_fn(y,t,K):
  Akt, pAkt, pPTEN, PTEN, PIP2, PIP3, PI3K, GSK3B, pGSK3B, LPS, HDACi, cNFkB, nNFkB, TNF, phagocytosisM2, microspheres = y

## rate constants:

  k1 = K[0]
  k2 = K[1]
  k3 = K[2]
  k4 = K[3]
  k5 = K[4]
  k6 = K[5]
  k7 = K[6]
  k8 = K[7]
  k9 = K[8]
  k10 = K[9]
  k11 = K[10]
  k12 = K[11]
  k13 = K[12]
  k14 = K[13]
  k15 = K[14]
  k16 = K[15]
  i1 = K[16]
  i2 = K[17]
  i3 = K[18]
  i4 = K[19]
  Km = K[20]
  n = K[21]

## Differential Equations: ask which one is more accurate
  
  dPI3Kdt = k3 - k4*PI3K + i4*microspheres

  dPIP2dt = k6*PIP3 - k5*PIP2*PI3K*((Km**n)/(Km**n + PTEN**n))
  dPIP3dt = k5*PIP2*PI3K*((Km**n)/(Km**n+ PTEN**n)) - k6*PIP3

  dAktdt = k2*pAkt - k1*((PIP3**2)/(1 + PIP3**2))*Akt
  dpAktdt = k1*(((PIP3**2)/(1 + PIP3**2)))*Akt - k2*pAkt

  dPTENdt = k7*pPTEN*pAkt - k8*PTEN*GSK3B + i1*LPS
  dpPTENdt = k8*PTEN*GSK3B - k7*pPTEN*pAkt

  dGSK3Bdt = k9*pGSK3B - k10*GSK3B*pAkt + i2*HDACi
  dpGSK3Bdt = k10*GSK3B*pAkt - k9*pGSK3B

  dcNFkBdt = k11*nNFkB*pAkt - k12*cNFkB - i3*LPS
  dnNFkBdt = k12*cNFkB - k11*nNFkB*pAkt + i3*LPS

  dTNFdt = k13*nNFkB - k14*TNF

  dphagodt = k15*pAkt - k16*phagocytosisM2

  dLPSdt = 0
  dHDACidt = 0
  dmicrospheresdt = 0

  if 100 <= t < 280:
    dLPSdt = 1 - LPS
  elif t < 100:
    dLPSdt = 0
  else:
    dLPSdt = -LPS

  if 160 <= t < 280:
    dHDACidt = 1 - HDACi
  elif t < 160:
    dHDACidt = 0
  else:
    dHDACidt = -HDACi

  # if 300 <= t < 305:
  #   dmicrospheresdt = 1 - microspheres
  # elif t < 120:
  #   dmicrospheresdt = 0
  # else:
  #   dmicrospheresdt = -microspheres

  dydt = [dAktdt, dpAktdt, dpPTENdt, dPTENdt, dPIP2dt, dPIP3dt, dPI3Kdt, dGSK3Bdt, dpGSK3Bdt, dLPSdt, dHDACidt, dcNFkBdt, dnNFkBdt, dTNFdt, dphagodt, dmicrospheresdt]
  return dydt

def predictions(simulation_fn, K):
  time = np.linspace(0,500, 1000)
  yi = [1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
  y = odeint(simulation_fn, yi, time, args=(K,))
  avg = sum(y[50:75, :])/float(75-50)
  newy = y
  newy[:, 0:9] = newy[:, 0:9]/avg[0:9]
  newy[:, 11:15] = newy[:, 11:15]/avg[11:15]
  return newy

def obj_fn(X):
  expl_data = json.load(open("expl_data (1).json"))
  cost = 0
  pred = predictions(simulation_fn, X)
  for proteinID, information in expl_data.items():
    for time, value in information.items():
      cost += (pred[int(time), int(proteinID)] - float(value))**2
  return cost

if __name__ == "__main__":
    varbound = np.array([[0.01,10]]*20 + [[0.01, 1]]+ [[1, 10]])

    algorithm_param = {'max_num_iteration': 10000,\
                   'population_size':100,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv': None}

    model=ga(function=obj_fn,\
            dimension=22,\
            variable_type_mixed=np.array([['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['real'], ['int']]),\
            variable_boundaries=varbound,\
            algorithm_parameters=algorithm_param)

    model.run()
