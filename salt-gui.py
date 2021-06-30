import json
import sys
import os
import glob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from datetime import datetime

import tkinter as tk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import matplotlib

import numpy as np

total = 100
posCount = 0
neuCount = 0
negCount = 0

# functions
def getSubreddit_analysis():
    # get subreddit from entry box
    s = entry.get()
    os.system("python3 ./URS/urs/Urs.py -r " + s + " h 100 -y")

    # move to json dir
    #path_to_json = '/Programming/Subreddit-AnaLysis-Tool/URS/scrapes/' + datetime.today().strftime('%m-%d-%Y') + '/subreddits/'
    #path_to_json = '/URS/scrapes/' + datetime.today().strftime('%m-%d-%Y') + '/subreddits/'

    path_to_json = '/URS/scrapes/' + '06-28-2021' + '/subreddits/'


    os.chdir(os.getcwd() + path_to_json)
    #os.chdir(path_to_json)

    for filename in glob.glob('*.json'):
        with open(filename) as f:
            posts = json.load(f)

        for post in posts['data']:
            sentence = post['selftext']
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
    
    # plot
    #neg = (negCount/total) * 100
    #neu = (neuCount/total) * 100
    #pos = (posCount/total) * 100

    fig = Figure(figsize = (5, 5), dpi = 100)
    ax = fig.add_subplot(111)

    names = ['negative', 'neutral', 'positive']
    data = [negCount, neuCount, posCount]

    ind = np.arange(3) # x locations for bars
    width = .5
    
    ax.bar(ind, data, width)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window = tk.Tk()
#window.title('S.A.L.T. by Sean Kennedy')
window.title(os.getcwd())
window.geometry("500x500")

# entry box
entry = tk.Entry (window)

# button
quitButton = tk.Button(master=window, text="Quit", command=window.quit)
enterButton = tk.Button(master=window, text="Analyze Subreddit",  command=getSubreddit_analysis)

entry.pack(side=tk.TOP)
enterButton.pack(side=tk.TOP)
quitButton.pack(side=tk.BOTTOM)
#toolbar.pack(side=tk.BOTTOM, fill=tk.X)
#canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window.mainloop()