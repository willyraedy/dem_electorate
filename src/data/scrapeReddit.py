import praw
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import datetime

CLIENT_SECRET = os.getenv("REDDIT_API_SECRET")
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit_api_wrapper = praw.Reddit(client_id=CLIENT_ID,
                                 client_secret=CLIENT_SECRET,
                                 password=PASSWORD, user_agent='script:metis-project:v0.0.1 (by /u/wilburRay)',
                                 username='wilburRay')

import time


def get_all(subreddit, start_utc, end_utc):
  assert start_utc > end_utc, 'Scrapes backwards so start_utc must be larger than end_utc'

  curr_utc = start_utc
  comments = []
  submissions = []

  while curr_utc > end_utc:
    # get comments
    res_comm = requests.get(f'https://api.pushshift.io/reddit/search/comment/?sort=desc&subreddit=politics&limit=500&before={curr_utc}')
    new_comm_data = res_comm.json()['data']
    comments = comments + new_comm_data
    next_utc = new_comm_data[-1]['created_utc']

    # get submissions from same range as comments
    res_sub = requests.get(f'https://api.pushshift.io/reddit/search/submission/?sort=desc&subreddit=politics&limit=500&before={curr_utc}&after={next_utc}')
    new_sub_data = res_sub.json()['data']
    submissions = submissions + new_sub_data

    curr_utc = next_utc
    time.sleep(1)

  comm_to_insert = [x for x in comments if int(x['created_utc']) > end_utc]
  sub_to_insert = [x for x in submissions if int(x['created_utc']) > end_utc]

  # insert into mongo
  return comm_to_insert, sub_to_insert


# 67039 -> correct number in last day
now = 1582067386
curr_utc = now
end_time = now - (24 * 60 * 60)
