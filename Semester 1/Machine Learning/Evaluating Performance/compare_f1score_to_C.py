#! /bin/python3.9

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
import numpy as np

X = np.arange(0, 1, 0.01).reshape(-1, 1)
y = np.random.normal(0.0, 1.0, X.size).reshape(-1, 1)
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)
model = LinearSVC(C=1.0).fit(Xtrain, ytrain)
preds = model.predict(Xtest)
print(confusion_matrix(ytest, preds))
print(classification_report(ytest, preds))
dummy = DummyClassifier(strategy="most_frequent").fit(Xtrain, ytrain)
ydummy = dummy.predict(Xtest)
print(confusion_matrix(ytest, ydummy))
print(classification_report(ytest, ydummy))
mean_error = []
std_error = []
Ci_range = [0.01, 0.1, 1, 5, 10, 25, 50, 100]
for Ci in Ci_range:
    model = LinearSVC(C=Ci)
    scores = cross_val_score(model, X, y, cv=5, scoring="f1")
    mean_error.append(np.array(scores).mean())
    std_error.append(np.array(scores).std())
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.errorbar(Ci_range, mean_error, yerr=std_error, linewidth=3)
plt.xlabel("Ci")
plt.ylabel("F1 Score")
plt.show()
