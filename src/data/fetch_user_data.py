from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import pickle

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

db = get_db()

res = db.comments.aggregate_raw_batches([
    {
        '$group': {
            '_id': {'author': '$author'},
            'num_comments': {'$sum': 1},
            'total_comment_length': {'$sum': { "$strLenCP": "$body" }},
            'text': {'$push': '$body'},
            'total_comment_score': {'$sum': '$score'},
            'best_comment_score': {'$max': '$score'},
            'worst_comment_score': {'$min': '$score'},
            'number_neg_score_comments': {
                '$sum': {
                    '$cond': {
                        'if': {'$lt': ['$score', 0] },
                        'then': 1,
                        'else': 0
                    }
                }
            },
            'number_pos_score_comments': {
                '$sum': {
                    '$cond': {
                        'if': {'$gt': ['$score', 0] },
                        'then': 1,
                        'else': 0
                    }
                }
            },
            'total_neg_score': {
                '$sum': {
                    '$cond': {
                        'if': {'$lt': ['$score', 0] },
                        'then': '$score',
                        'else': 0
                    }
                }
            },
            'total_pos_score': {
                '$sum': {
                    '$cond': {
                        'if': {'$gt': ['$score', 0] },
                        'then': '$score',
                        'else': 0
                    }
                }
            },
            'num_comments_politics': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'politics']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_political_discussion': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'PoliticalDiscussion']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_democrats': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'democrats']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_warren': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'ElizabethWarren']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_pete': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'Pete_Buttigieg']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_biden': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'JoeBiden']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_sanders': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'SandersForPresident']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_bloomberg': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'PresidentBloomberg']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
            'num_comments_klob': {
                '$sum': {
                    '$cond': {
                        'if': {'$eq': ['$subreddit', 'BaemyKlobaechar']},
                        'then': 1,
                        'else': 0,
                    }
                }
            },
        }
    },
    {'$match': {'num_comments': {'$gt': 20}}},
    {'$out': 'user_comments'}
], allowDiskUse=True)
