import nltk
from sklearn.feature_extraction.text import CountVectorizer

nltk.download("stopwords")
vectorizer = CountVectorizer(stop_words=nltk.corpus.stopwords.words("english"))