import argparse
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from networkObj import Network
from interactions import Interaction
from substrate import Substrate
import storeIt
import openIt

parser = argparse.ArugmentParser(description='change the values of substrates or interactions')
parser.add_argument('-i', '-input', help='input pickle file path', required=True)

# essentially can edit any of the substrate or interaction object attributes
