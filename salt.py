import json
import sys
import os
import subprocess
import glob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

total = 0
negCount = 0
neuCount = 0 
posCount = 0

# command line arguments for subreddits to analyze
n = len(sys.argv)
for i in range(1,n):
    os.system("python3 ./URS/urs/Urs.py -r " + sys.argv[i] + " h 10 -y")


def sentiment_score(sentence):
    global total
    total = total + 1

    analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = analyzer.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05 :
        global posCount
        posCount = posCount + 1

    elif sentiment_dict['compound'] <= -0.05 :
        global negCount
        negCount = negCount + 1

    else :
        global neuCount
        neuCount = neuCount + 1

def subreddit_score(subreddit):
    print(subreddit, " was rated as ", (negCount/total)*100, "% Negative")
    print(subreddit, " was rated as ", (neuCount/total)*100, "% Neutral")
    print(subreddit, " was rated as ", (posCount/total)*100, "% Positive")

path_to_json = 'URS/scrapes/06-28-2021/subreddits/'
os.chdir(path_to_json)

for filename in glob.glob('*.json'):
    with open(filename) as f:
        posts = json.load(f)

    for post in posts['data']:
        sentence = post['selftext']
        sentiment_score(sentence)
    
    subreddit_score(posts['scrape_settings']['subreddit'])