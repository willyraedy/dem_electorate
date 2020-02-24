import pandas as pd
from data.mymongo import get_db

def get_submission_docs_for_subreddit(subreddit, min_num_comments=10, min_num_total_words=500):
  """
  Returns dataset where every document is all the comments for a submission from a subreddit

  Args:
  subreddit: string
  min_num_comments: int (default: 10)
  min_num_total_words: int (default: 500)

  Returns:
  dataframe
  """

  db = get_db()

  # fetch records from mongo and put in pandas
  comments = db.comments.find({'subreddit': subreddit})
  comms = pd.DataFrame.from_dict(comments)
  submissions = db.submissions.find({'subreddit': subreddit})
  subs = pd.DataFrame.from_dict(submissions)

  # filter meaningless comments
  comms = comms[comms.body != '[removed]']

  # merge comments and submissions
  comms['sub_id'] = comms.link_id.map(lambda x: x[3:])
  sub_with_comms = subs.merge(
    comms,
    left_on='id',
    right_on='sub_id',
    suffixes=('_sub', '_comm')
  )

  # filter to top ten comments on submission
  sub_with_comms['comm_rank'] = sub_with_comms.groupby('id_sub')['score_comm'].rank('dense', ascending=False)
  filtered = sub_with_comms[(sub_with_comms.comm_rank <= min_num_comments) & (sub_with_comms.num_comments >= min_num_comments)]

  # group into documents by submission
  to_model = filtered.groupby('id_sub').apply(lambda grp: ' '.join(grp['body'].tolist())).reset_index()
  to_model = to_model.rename(columns={0: 'text'})
  to_model['word_count'] = to_model.text.map(lambda x: len(x.split(' ')))

  # print metric of most frequent poster
  comm_by_freq_user = filtered.groupby('author_comm').body.agg('count').sort_values(ascending=False).iat[0]
  print('Percent of comments by most prolific user:', comm_by_freq_user / filtered.shape[0])

  # filter by min doc size
  return to_model[to_model.word_count >= min_num_total_words]
