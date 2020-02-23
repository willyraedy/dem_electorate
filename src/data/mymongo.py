from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

def get_db():
  MONGO_PASSWORD = os.environ['MONGO_USER_PASSWORD']
  config = {
    'host': '3.136.156.62:27017',
    'username': 'dem_electorate_user',
    'password': MONGO_PASSWORD,
    'authSource': 'dem_electorate'
  }
  client = MongoClient(**config)
  return client.dem_electorate
