import pickle

def openNetwork(path):
    with open(path, 'rb') as file:
        n = pickle.load(file)
    return n
    
