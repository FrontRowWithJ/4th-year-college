import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import numpy as np


m = 25
Xtrain = np.linspace(0.0, 1.0, num=m)
ytrain = np.sign(Xtrain-0.5+np.random.normal(0, 0.2, m))
Xtrain = Xtrain.reshape(-1, 1)
model = KNeighborsClassifier(
    n_neighbors=3, weights="uniform").fit(Xtrain, ytrain)
Xtest = np.linspace(0.0, 1.0, num=1000).reshape(-1, 1)
ypred = model.predict(Xtest)
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.plot(Xtest, ypred, color="green")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["predict", "train"])
plt.show()
model = KNeighborsClassifier(
    n_neighbors=7, weights="uniform").fit(Xtrain, ytrain)
ypred = model.predict(Xtest)
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.plot(Xtest, ypred, color="green")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["predict", "train"])
plt.show()
