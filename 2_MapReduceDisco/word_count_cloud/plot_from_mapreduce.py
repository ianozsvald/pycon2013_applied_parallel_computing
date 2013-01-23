import json
import argparse
import numpy as np
from word_cloud import wordcloud
import stopwords

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('json_file', help='JSON input file (e.g. mapreduceout_wordcount.json)')
    args = parser.parse_args()

    sw = set(stopwords.stopwords)
    sw.add('-')
    sw.add('&')
    sw.add('RT')
    sw.add("it's")

    counts_and_words = []
    for line in open(args.json_file):
        word, count = json.loads(line)
        #print word, count
        counts_and_words.append((count, word))

    counts_and_words.sort()
    counts_and_words.reverse()

    words = []
    counts = []
    for count, word in counts_and_words:
        if word.lower() not in sw:
            print word, count
            words.append(word)
            counts.append(count)
        if len(words) == 200:
            break
    words = np.array(words)
    counts = np.array(counts)

    output_filename = "output.png"
    font_path = "/usr/share/fonts/truetype/droid/DroidSansMono.ttf"

    wordcloud.make_wordcloud(words, counts, output_filename, font_path, width=800, height=600)
