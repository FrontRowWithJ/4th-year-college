import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import WhitespaceTokenizer, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

nltk.download("punkt")
tokenizer = CountVectorizer().build_tokenizer()
print(tokenizer("Here's example text, isn't it?"))
print(WhitespaceTokenizer().tokenize("Here's example text, isn't it?"))
print(word_tokenize("Here's example text, isn't it?"))
print(tokenizer("likes liking liked"))
print(WhitespaceTokenizer().tokenize("likes liking liked"))
print(word_tokenize("likes liking liked"))
stemmer = PorterStemmer()
tokens = word_tokenize("Here's example text, isn't it?")
stems = [stemmer.stem(token) for token in tokens]
print(stems)
tokens = word_tokenize("likes liking liked likeable")
stems = [stemmer.stem(token) for token in tokens]
print(stems)
