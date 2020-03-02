import pickle
from nltk.tokenize import word_tokenize, MWETokenizer # multi-word expression
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
from data.clean_data import process_text
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS, TfidfVectorizer


additional_stop_words = [
    'like', 'dont', 'im', 'say', 'did', 'said', 'thats', 'don', 'hes', 'does', 'thing', 'gt', 'sure', 'doesnt',
    'saying', 'youre', 'isnt', 'doing', 'got', 'didnt', 'yeah', 'just', 'yes',
    'right', 'think', 'going', 'want', 'know', 'good',
    'need', 'time', 'point', 'make', 'way', 'really',
    'id', 'ar', 's', 't', 've', 'm', 'shes',
    'c', 'd', 'v', 'actually', 'look', 'maybe', 'though', 'bad', 'came', 'mods', 'things', 'lot', 'let', 'lol', 'tell', 'pretty', 'literally'
    'theyre', 'people',
    '‘', '’', '“'
]
multi_words = [
    ('health','insurance'),
    ('fox', 'news'),
    ('bernie', 'sanders'),
    ('hillary', 'clinton'),
    ('barack', 'obama'),
    ('donald', 'trump'),
    ('joe', 'biden'),
    ('joseph', 'biden'),
    ('mass', 'shooting'),
    ('mass', 'shootings'),
    ('assault', 'weapon'),
    ('assault', 'weapons'),
    ('assault', 'weapons', 'ban'),
    ('sergeant', 'at', 'arms'),
    ('stop', 'and', 'frisk'),
    ('medicare', 'for', 'all'),
    ('public', 'option'),
    ('beat', 'trump'),
    ('articles', 'of', 'impeachment'),
    ('new', 'york'),
    ('hold', 'in', 'contempt'),
    ('quid', 'pro', 'quo')
]
nmf_topic_labels = [
    '2016_election_frustration',
    'impeachment_proceedings',
    'healthcare',
    'primary_candidates',
    'gun_control',
    'election_general_terms',
    'right_wing_media',
    'impeachment',
    'yang_ubi',
    'primary_debates',
    'bloomberg',
    'econ_trump_vs_obama',
    'race_identity',
    'tax_return_ukraine_biden',
    'election_midwest_swing',
    'monetary_policy',
    'rep_dem_comparison',
    'miltary_and_immigration',
#     'none'
]

mwe_tokenizer = MWETokenizer(multi_words)
def complete_tokenizer(x):
    return mwe_tokenizer.tokenize(word_tokenize(x))

stemmer = WordNetLemmatizer()
class StemmedCountVectorizer(CountVectorizer):
  def build_analyzer(self):
      analyzer = super(StemmedCountVectorizer, self).build_analyzer()
      return lambda doc: ([stemmer.lemmatize(w) for w in analyzer(doc)])

def get_topic_label(row):
    topic_weights = row['2016_election_frustration':'miltary_and_immigration']
    primary_topic = nmf_topic_labels[np.argmax(topic_weights)]
    if 'word_count' in row:
      per_word = topic_weights / row['word_count']
      return primary_topic if np.max(per_word) > 0.0003 else 'none'
    else:
      return primary_topic

def label_primary_topic(df):
    df_ = df.copy()
    df_['topic_label'] = df_.apply(get_topic_label, axis=1)
    return df_

def process(df):
    with open('../../data/interim/rDemocrats_CV.pickle', 'rb') as read_file:
      cv_dems = pickle.load(read_file)

    with open('../../data/interim/rDemocrats_nmf.pickle', 'rb') as read_file:
        nmf_dems = pickle.load(read_file)

    data_clean = df.copy()
    data_clean.text = data_clean.text.map(lambda t: process_text(t) if type(t) == str else process_text(' '.join(t)))
    data_cv = cv_dems.transform(data_clean.text)
    data_dtm_raw = pd.DataFrame(data_cv.toarray(), columns=cv_dems.get_feature_names())
    data_dtm_raw.index = data_clean.index

    data_dtm = data_dtm_raw.iloc[:, :-171]

    doc_topic_nmf = nmf_dems.transform(data_dtm)
    results = pd.DataFrame(doc_topic_nmf, columns=nmf_topic_labels)

    return label_primary_topic(results.join(data_clean.reset_index()))
