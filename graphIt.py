from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# essentially will be a graphing module
def plot(network, saveFile=None, points=None, *names): # come back to points
    if len(names) == 0:
        graph = [(i, s) for s in enumerate(network.substrates)]
    else:
        graph = []
        for i, s in enumerate(network.substrates):
            if s.name in names:
                graph.append((i, s))
    
    y0 = network.getInitialValues()
    time = np.linspace(0, 200, 200)
    y = odeint(network.diffEQs, y0, time)

    plt.figure(figsize=(6,4),dpi=100)
    for tup in graph:
        plt.plot(time,y[:,tup[0]],label=tup[1].name)
    plt.tick_params(direction='in',labelsize=12)
    plt.xlabel('Time [mins]',fontsize=12)
    plt.ylabel('Concentration [AU]',fontsize=12)
    plt.legend(loc='right',fontsize=10)
    plt.tight_layout()
    if saveFile == None:
        plt.show()
    else:
        plt.savefig(f'{saveFile}.pdf', format='pdf')

def diagram(network, saveFile):
    return

def barchart():
    return