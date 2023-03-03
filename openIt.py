import pickle

def openNetwork(path):
    with open(path, 'rb') as file:
        n = pickle.load(path)
    return n
    
