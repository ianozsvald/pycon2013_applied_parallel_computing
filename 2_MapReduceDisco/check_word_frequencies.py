import argparse
import json
#import pylab
import matplotlib.pyplot as plt

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('--json_file', help='JSON input file (e.g. mapreduceout_wordcount.json)', default="mapreduceout_wordcount.json")
    args = parser.parse_args()

    # read json lines, sort by frequency
    lines = open(args.json_file).readlines()
    pairs = [json.loads(s) for s in lines]
    # sort by second item (frequency), reverse so most frequent comes first
    pairs.sort(key=lambda item: item[1], reverse=True)

    frequencies = [item[1] for item in pairs]
    plt.loglog(frequencies)
    plt.ylabel("Log 10 Frequencies", fontsize=14, fontweight="bold")
    plt.xlabel("Rank", fontsize=14, fontweight="bold")
    plt.grid(True)
    plt.title("Tweet words follow Zipf distribution")
    plt.show()
