import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy import misc
import pandas
from geneticalgorithm2 import geneticalgorithm2 as ga
import json
import argparse


parser = argparse.ArgumentParser(description='Fit function using genetic algorithm')
parser.add_argument('-d', '--data', help='filepath to json file containing fit data', required=True)


def simulation_fn(y,t,K,lps=[True, 1, 250, 430],hdaci=[True, 1, 310, 430]):
    Akt, pAkt, pPTEN, PTEN, PIP2, PIP3, PI3K, GSK3B, pGSK3B, LPS, HDACi, cNFkB, nNFkB, TNF, phagocytosisM2, microspheres = y

    ## rate constants:

    k1 = K[0]
    k2 = K[1]
    k5 = K[2]
    k6 = K[3]
    k7 = K[4]
    k8 = K[5]
    k9 = K[6]
    k10 = K[7]
    k11 = K[8]
    k12 = K[9]
    k13 = K[10]
    k14 = K[11]
    k15 = K[12]
    k16 = K[13]
    i1 = K[14]
    i2 = K[14]
    i3 = K[14]
    i4 = K[14]
    Km = K[15]
    n = K[16]
    k3 = 1
    k4 = 1

    ## Differential Equations: ask which one is more accurate
    
    dPI3Kdt = k3-k4*PI3K+i4*microspheres

    dPIP2dt = k6*PIP3 - k5*PIP2*PI3K*((Km**n)/(Km**n + PTEN**n))
    dPIP3dt = k5*PIP2*PI3K*((Km**n)/(Km**n+ PTEN**n)) - k6*PIP3

    dAktdt = k2*pAkt - k1*((PIP3**2)/(1 + PIP3**2))*Akt
    dpAktdt = k1*(((PIP3**2)/(1 + PIP3**2)))*Akt - k2*pAkt

    dPTENdt = k7*pPTEN - k8*PTEN*GSK3B + i1*LPS
    dpPTENdt = k8*PTEN*GSK3B - k7*pPTEN

    dGSK3Bdt = k9*pGSK3B - k10*GSK3B*pAkt + i2*HDACi
    dpGSK3Bdt = k10*GSK3B*pAkt - k9*pGSK3B

    dcNFkBdt = k11*nNFkB*pAkt - k12*cNFkB - i3*LPS
    dnNFkBdt = k12*cNFkB - k11*nNFkB*pAkt + i3*LPS

    dTNFdt = k13*nNFkB - k14*TNF

    dphagodt = k15*pAkt - k16*phagocytosisM2

    dLPSdt = 0
    dHDACidt = 0
    dmicrospheresdt = 0
    
    if lps[0]:
        if lps[2] <= t < lps[3]:
            dLPSdt = lps[1] - LPS
        elif t < lps[2]:
            dLPSdt = 0
        else:
            dLPSdt = -LPS

    if hdaci[0]:
        if hdaci[2] <= t < hdaci[3]:
            dHDACidt = hdaci[1] - HDACi
        elif t < hdaci[2]:
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

def findSteadyState(arr, times):
    def f(t):
        return arr[t, :]

    steadyTime = 240

    for time in times:
        deriv = misc.derivative(f, time, dx = 1)
        if [d < 10**-10 for d in deriv] == [True for d in deriv]:
            steadyTime = time
        break
    
    return steadyTime

def predictions(simulation_fn, K):
    time = np.linspace(0, 10000, 100000)
    
    yi = [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    y = odeint(simulation_fn, yi, time, args=(K, (False, 1.0, 250, 430), (False, 1.0, 310, 430)))
    steady = list(y[findSteadyState(y, [i for i in range(0, 9999)]), :])
    newy = odeint(simulation_fn, steady, time, args=(K, (True, 1.0, 250, 430), (True, 1.0, 310, 430)))

    newy[:, 0:9] = newy[:, 0:9]/steady[0:9]
    newy[:, 11:15] = newy[:, 11:15]/steady[11:15]
    
    return newy

def obj_fn(X):
    expl_data = data
    cost = 0
    count = 0
    pred = predictions(simulation_fn, X)
    for proteinID, information in expl_data.items():
        for time, value in information.items():
            cost += (pred[int(time), int(proteinID)] - float(value))**2
            count += 1

    return float(cost)/count

if __name__ == '__main__':

    args = parser.parse_args()

    varbound = np.array([[0.001,.1]]*15 + [[0.0001, .01]]+ [[1, 8]])
    
    algorithm_param = {'max_num_iteration': 1000,\
                    'population_size':100,\
                    'mutation_probability':0.1,\
                    'elit_ratio': 0.01,\
                    'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                    'crossover_type':'uniform',\
                    'max_iteration_without_improv': 150}
    
    with open(args.data, 'r') as file:
        data = json.load(file)
    
    model=ga(function=obj_fn,\
            dimension=17,\
            variable_type_mixed=('real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'real', 'int'),\
            variable_boundaries=varbound,\
            algorithm_parameters=algorithm_param)
    
    model.run(set_function=ga.set_function_multiprocess(obj_fn, n_jobs=4))