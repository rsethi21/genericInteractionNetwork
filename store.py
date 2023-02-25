import pickle

def saveIt(obj, outfilepath):
    with open(outfilepath, 'wb') as file:
        pickle.dump(obj, file)
        print(f"{obj.name} successfully saved at {outfilepath}!")
