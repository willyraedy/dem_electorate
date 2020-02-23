from dotenv import load_dotenv
load_dotenv()
import os
import requests
import datetime
import time
from pymongo import MongoClient
import numpy as np

MONGO_PASSWORD = os.environ['MONGO_USER_PASSWORD']

config = {
  'host': '3.20.206.120:27017',
  'username': 'dem_electorate_user',
  'password': MONGO_PASSWORD,
  'authSource': 'dem_electorate'
}

db = MongoClient(**config).dem_electorate

def get_all(subreddit, start_utc, end_utc):
  assert start_utc > end_utc, 'Scrapes backwards so start_utc must be larger than end_utc'

  curr_utc = start_utc
  retries = 0
  while curr_utc > end_utc:
    try:
      days_scraped = (start_utc - curr_utc) / (60 * 60 * 24)
      if (days_scraped % 5 < 0.1):
        print('Days scraped:', days_scraped)
      # get comments
      res_comm = requests.get(f'https://api.pushshift.io/reddit/search/comment/?sort=desc&subreddit={subreddit}&limit=500&before={curr_utc}')
      comments = res_comm.json()['data']
      next_utc = comments[-1]['created_utc']

      # get submissions from same range as comments
      res_sub = requests.get(f'https://api.pushshift.io/reddit/search/submission/?sort=desc&subreddit={subreddit}&limit=500&before={curr_utc}&after={next_utc}')
      submissions = res_sub.json()['data']

      comm_to_insert = [x for x in comments if int(x['created_utc']) > end_utc]
      sub_to_insert = [x for x in submissions if int(x['created_utc']) > end_utc]
      if comments:
        db.comments.insert_many(comm_to_insert)
      if submissions:
        db.submissions.insert_many(sub_to_insert)

      curr_utc = next_utc
      time.sleep(0.3)
    except Exception as e:
      print(e)
      retries += 1
      if retries > 3:
        raise e
