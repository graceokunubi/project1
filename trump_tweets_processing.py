# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import numpy as np 
from datetime import datetime

def create_date_col(df):
    """
    cleaning up datetime to just carry month and year, dropping date and timestamp
    """
    df.reset_index(inplace=True)
    df.index = pd.to_datetime(df["year"].apply(str) +"-"+ df["month"].apply(str))
    df.drop(columns=["year","month"], inplace=True)

"""trump ratings"""

df = pd.read_csv(r'approval_polllist.csv')

df["enddate"] = pd.to_datetime(df["enddate"])
df["month"] = df["enddate"].dt.month
df["year"] = df["enddate"].dt.year

subset = df[(df["year"]>=2016) & (df["year"]<=2020)]
subset.index = np.arange(len(subset))

sub_pivot_a = subset.pivot_table(index=["year","month"], columns="pollster",values="adjusted_approve", aggfunc="mean")
create_date_col(sub_pivot_a)
sub_pivot_a["max"] = sub_pivot_a.max(axis=1)
sub_pivot_a["min"] = sub_pivot_a.min(axis=1)
sub_pivot_a["mean"] = sub_pivot_a.mean(axis=1)      

"""trump tweets"""

tweets = pd.read_csv(r'trump_tweets.csv')
tweets["date"] = tweets["date"].apply(lambda x: datetime.utcfromtimestamp(int(x)/1000))
tweets["date_only"] = pd.to_datetime(tweets["date"].dt.date)
tweets["month"] = tweets["date"].dt.month
tweets["year"] = tweets["date"].dt.year

tweet_pivot = tweets.pivot_table(index=["year","month"], values="retweets", aggfunc="count")
create_date_col(tweet_pivot)

"""concat dataframes and output for d3.js"""

together_df = pd.concat([sub_pivot_a,tweet_pivot], axis=1)
together_df = together_df[together_df.columns[-4:]] #keep only rating statistics and # of tweets
together_df = together_df.dropna().reset_index()
together_df.rename(columns={"index":"Date"}, inplace=True)
together_df["Date"] = together_df["Date"].apply(str) #we want date instead of unixtime in json
together_df.columns=["Date","adjusted_approve_max","adjusted_approve_min","adjusted_approve_mean","tweet_count"]
together_df.to_json(r'trump_processed_data.json', orient="records")


### Sources: 
#referenced pandas documentation and stack overflow to help figure out various syntax and 
#functions used in this script. 