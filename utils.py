import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import re
import seaborn as sns
import sqlite3
import warnings
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
warnings.filterwarnings('ignore')

def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    return text

def visualiseSentiment(df):
    sns.set(rc={'figure.figsize': (30, 2)})
    sns.heatmap(pd.DataFrame(df).set_index("Text").T,center=0, annot=True, cmap = "PiYG")
    plt.show()

def getScore(text):
    clean_text = cleanTxt(text)
    analysis = SentimentIntensityAnalyzer()
    dict_score = analysis.polarity_scores(clean_text)
    return dict_score


def vaderPolarity(score, threshold=0.05):
    score = score.get('compound')
    if score >= threshold:
        return 'Positive'
    elif -threshold < score < threshold:
        return 'Neutral'
    else:
        return 'Negative'


def count_regex(pattern, text):
    return len(re.findall(pattern, text))


def loadData():
    conn = sqlite3.connect('../data/USAirlinesTweets.sqlite')
    df = pd.read_sql_query("SELECT tweet_id, airline_sentiment, text FROM Tweets", conn)
    df = df.dropna(subset=['text'])
    df['airline_sentiment'] = df['airline_sentiment'].apply(lambda x: x.capitalize())

    df_ = df.copy()
    df_['count_words'] = df_.apply(lambda x: count_regex(r'\w+', x.text), axis=1)

    def show_dist(df, col):
        print(f'\n Statistics \n')
        print(df.groupby('airline_sentiment')[col].describe())
        print(f'Vocabulary Size {len(set(cleanTxt(" ".join(df.text.values)).split()))}')
        print(f'\n Distribution \n')

        bins = np.arange(df[col].min(), df[col].max() + 1)
        g = sns.FacetGrid(df, col='airline_sentiment', height=5, hue='airline_sentiment', palette="magma")
        g = g.map(sns.distplot, col, kde=True, norm_hist=True, bins=bins)
        plt.show()

    show_dist(df_, 'count_words')
    return df

def vaderNormScoreFunc():
    x = np.linspace(-5,5,100)
    y = x/np.sqrt((x*x) + 15)

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.plot(x,y, 'b')