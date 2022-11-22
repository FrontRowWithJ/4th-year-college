from sklearn.metrics import roc_curve
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
X = np.arange(0, 1, 0.01).reshape(-1, 1)
y = np.random.normal(0.0, 1.0, X.size).reshape(-1, 1)
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)
model = LinearSVC(C=1.0).fit(Xtrain, ytrain)
fpr, tpr, _ = roc_curve(ytest, model.decision_function(Xtest))
plt.plot(fpr, tpr)
plt.xlabel("False positive rate")
plt.ylabel("True positive rate")
plt.plot([0, 1], [0, 1], color="green", linestyle="--")
plt.show()
