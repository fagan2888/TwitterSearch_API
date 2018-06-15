import TwitterScraper
import mysql.connector
from sqlalchemy import create_engine
import logging as log
import config

import datetime
import pandas as pd

log.basicConfig(level=log.INFO)

username = config.username
password = config.password

engine = create_engine('mysql+mysqlconnector://' + username + ':' + password + '@twitterdata.ckmmf3gk0i4d.us-east-2.rds.amazonaws.com:3306', echo=False)

# set parameters
search_query = "bitcoin"
rate_delay_seconds = 0
error_delay_seconds = 5
select_tweets_since = datetime.datetime.strptime("2017-08-01", '%Y-%m-%d')
select_tweets_until = datetime.datetime.strptime("2017-08-02", '%Y-%m-%d')
threads = 1

# execute
twitSlice = TwitterScraper.TwitterSlicer(rate_delay_seconds, error_delay_seconds, select_tweets_since, select_tweets_until, threads)
twitSlice.search(search_query)
twitter_df = twitSlice.df
twitter_df.to_sql(name="btcTwitter_August", con=engine, if_exists = 'append', index=False)

print("TwitterSearch collected %i" % twit.counter)
print("TwitterSlicer collected %i" % twitSlice.counter)