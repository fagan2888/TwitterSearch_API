import TwitterScraper
import mysql.connector
from sqlalchemy import create_engine
import logging as log
from time import sleep
import config

import datetime
import pandas as pd

log.basicConfig(level=log.INFO)

username = config.username
password = config.password
dates = ["2017-12-10", "2017-12-11"]

# set parameters
search_query = "bitcoin"
rate_delay_seconds = 1    # to avoid getting IP address banned
error_delay_seconds = 5
threads = 1

# pull dates at index i and i+1 to set range
for i in range(len(dates) - 1):
    select_tweets_since = datetime.datetime.strptime(dates[i], '%Y-%m-%d')
    select_tweets_until = datetime.datetime.strptime(dates[i+1], '%Y-%m-%d')

    # execute
    print("running search for dates " + dates[i] + " - " + dates[i+1])
    twitSlice = TwitterScraper.TwitterSlicer(rate_delay_seconds, error_delay_seconds, select_tweets_since, select_tweets_until, threads)
    twitSlice.search(search_query)
    twitter_df = twitSlice.df

    # write to mysql database
    print("opening connection...")
    engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306/tweets', echo=False)

    print("writing data...")
    twitter_df.to_sql(name="bitcoin_dec", con=engine, if_exists = 'append', index=False, chunksize=5000)

    print("wrote to db!")
