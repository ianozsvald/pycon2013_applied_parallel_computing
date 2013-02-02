import json
from disco.core import Job, result_iterator
from disco.func import chain_reader, sum_combiner
import ttp

# Usage:
# $ python count_tweet_words.py

OUTPUT_FILENAME = "mapreduceout_wordcount.json"


def get_username_tweet(line):
    """Extract username and tweet from csv-encoded line"""
    j = json.loads(line)
    username = j['username']
    tweet = j['tweet']

    return username, tweet


def get_users(tweet):
    """Return list of @users found in tweet"""
    parser = ttp.Parser()
    result = parser.parse(tweet)
    return result.users



def map(line, params):
    tweeter, tweet = count_tweet_words_6.get_username_tweet(line)
    # return each word in the tweet (to count frequency of each term)
    for user_reply in count_tweet_words_6.get_users(tweet):
        yield (tweeter, user_reply), 1




def reduce(iter, params):
    from disco.util import kvgroup
    for word, counts in kvgroup(sorted(iter)):
        yield word, sum(counts)


if __name__ == '__main__':
    #input_filename = "./tweet_data/tweets_357.json"
    #input_filename = "./tweet_data/tweets_859157.json"
    #input_filename = "/media/3TBStorage/tweets_all.json"

    # we need a fully qualified file name for the server
    #fully_qualified_path = os.path.realpath(input_filename)
    #input = [fully_qualified_path]

    #input = ["tag://data:tweets357"]
    input = ["tag://data:tweets859157xa"]

    # import this module so pickle knows what to send to workers
    import count_tweet_words_6
    print dir(count_tweet_words_6)

    job = Job().run(input=input,
                    map=map,
                    map_reader=chain_reader,
                    reduce=reduce,
                    combiner=sum_combiner)

    out = open(OUTPUT_FILENAME, 'w')
    for word, count in result_iterator(job.wait(show=True)):
        #print(word, count)
        out.write(json.dumps([word, count]) + '\n')
