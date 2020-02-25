import re
import string

def process_text(text):
    '''Make text lowercase, remove punctuation, remove words containing numbers, remove links.'''
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\w*http\w*|\w*www\w*', '', text)
    text = re.sub('\n', '', text)
#     text = text.encode('ascii', 'ignore').decode('ascii')
    return text
