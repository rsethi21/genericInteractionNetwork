import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from networkObj import Network
from interactions import Interaction
from substrate import Substrate
import storeIt

parser = argparse.ArgumentParser(description='Create a cellular pathway mechanism.')

parser.add_argument('-i', '--input', help='input a json file of the configurations of the network', required=True)
parser.add_argument('-o', '--output', help='input a filepath for the output pdf with all output', required=False, default='./output')
parser.add_argument('-s', '--save', help='path to file to save network object', required=False, default='network.pkl')


if __name__ == '__main__':
    args = parser.parse_args()

    # store object
    with open(args.input, 'r') as file:
        inputDict = json.load(file)
    newNetwork = Network('Test Network', inputDict)
    storeIt.saveIt(newNetwork, args.save)
    
    # integrate
    y0 = newNetwork.getInitialValues()
    time = np.linspace(0, 200, 200)
    y = odeint(newNetwork.diffEQs, y0, time)
    # time_steady = newNetwork.findSteadyState()
    # print(time_steady)

    # plot
    plt.figure(figsize=(6,4),dpi=100)
    plt.plot(time,y[:,0],'g-',label='A')
    plt.plot(time,y[:,1],'r-',label='B')
    plt.plot(time,y[:,2],'b-',label='C')
    plt.plot(time,y[:,3],'y-',label='S1')
    plt.tick_params(direction='in',labelsize=12)
    plt.xlabel('Time [mins]',fontsize=12)
    plt.ylabel('Concentration [AU]',fontsize=12)
    plt.legend(loc='right',fontsize=10)
    plt.tight_layout()
    plt.savefig(f'{args.output}.pdf', format='pdf')

    # graph
    newNetwork.networkGraph(args.output)
