from sklearn.feature_extraction.text import CountVectorizer

docs = ["This is the first document.",
        "This is the second second document.",
        "And the third one.",
        "Is this the first document?"]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)
print(vectorizer.get_feature_names())
print(X.toarray())
