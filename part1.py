# Full Name: Alex Lu
# UMID     : 54523810

from tweepy import OAuthHandler, API
import nltk
import json
import sys

ckey = '6nf6MhZyPiMf4rPiEZR5Nt35Y'
csecret = 's4NwW3qNrfnFf9YoCUgWcsSWQgrIW0r6J9AHLWThpL4atkgbIC'
atoken = '299772807-jL6Ihyli3ljudb904ClXzyocfLE1rPiBIMY8sgnf'
asecret = 'HRNM659mB5weC4KsAXZjQbgVrPNfImqh1kzxVYZ9nchbc'


def get_tweets(username, count):

    # Authorize twitter, initialize tweepy
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = API(auth)

    # Initialize a list to hold all the tweets
    new_tweets = api.user_timeline(id=username, count=count)

    return new_tweets


def check_original(tweet):
    if tweet.text.lower().startswith("rt @"):
        return False
    else:
        return True


def check_retweeted(tweets):

    # Initialize the counter
    total_retweeted_tweets = 0

    for tweet in tweets:
        if check_original(tweet):
            total_retweeted_tweets += 1

    return total_retweeted_tweets

def check_times_favorited(tweets):

    total_favorited = 0

    for tweet in tweets:
        if check_original(tweet):
            total_favorited += tweet.favorite_count

    return total_favorited


def check_times_retweeted(tweets):

    total_retweeted = 0

    for tweet in tweets:
        if check_original(tweet):
            total_retweeted += tweet.retweet_count

    return total_retweeted


def tag_tweet(tweets):

    text = ""

    for tweet in tweets:
        text += tweet.text

    words = []

    for word in nltk.word_tokenize(text):
        if not word.startswith("http") and not word.startswith("RT") and not word.endswith("RT") and word[:1].isalpha():
            words.append(word)

    tags = nltk.pos_tag(words)

    vb = dict()
    nn = dict()
    jj = dict()

    for tag in tags:
        if tag[1].startswith('NN'):
            if tag[0] in nn:
                nn[tag[0]] += 1
            else:
                nn[tag[0]] = 1

        elif tag[1].startswith('VB'):
            if tag[0] in vb:
                vb[tag[0]] += 1
            else:
                vb[tag[0]] = 1

        elif tag[1].startswith('JJ'):
            if tag[0] in jj:
                jj[tag[0]] += 1
            else:
                jj[tag[0]] =1

    nn = sorted(nn.items(), key=lambda x: x[1], reverse=True)[:5]
    vb = sorted(vb.items(), key=lambda x: x[1], reverse=True)[:5]
    jj = sorted(jj.items(), key=lambda x: x[1], reverse=True)[:5]

    # print out top 5 verbs
    sys.stdout.write("VERBS:")
    for verb in vb:
        sys.stdout.write(" %s(%d)" % (verb[0], verb[1]))

    # print out top 5 nouns
    sys.stdout.write("\nNOUNS:")
    for noun in nn:
        sys.stdout.write(" %s(%d)" % (noun[0], noun[1]))

    # print out top 5 adjectives
    sys.stdout.write("\nADJECTIVES:")
    for adj in jj:
        sys.stdout.write(" %s(%d)" % (adj[0], adj[1]))

    write_csv(nn)


def write_csv(nn):

    with open('noun_data.csv', 'w', newline='') as file:
        file.write('Noun,Number\n')
        for noun in nn:
            file.write("%s,%s\n" % (noun[0], noun[1]))


if __name__ == '__main__':

    # username, count = input().split()
    username = sys.argv[1]
    count = sys.argv[2]

    sys.stdout.write("USER: %s\n" % username)
    sys.stdout.write("TWEETS ANALYZED: %d\n" % int(count))

    tweets = get_tweets(username, count)
    tag_tweet(tweets)

    sys.stdout.write("\nORIGINAL TWEETS: %d\n" % check_retweeted(tweets))
    sys.stdout.write("TIMES FAVORITED (ORIGINAL TWEETS ONLY): %d\n" % check_times_favorited(tweets))
    sys.stdout.write("TIMES RETWEETED (ORIGINAL TWEETS ONLY): %d\n" % check_times_retweeted(tweets))
