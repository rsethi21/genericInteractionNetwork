from networkObj import Network
import argparse

parser = argparse.ArgumentParser(description="open a network object stored in pickle format")
parser.add_argument('-i', '--input', help='path to pickle file', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    n = Network.readNetworkObject(args.input)
    print(n.getInitialValues())
