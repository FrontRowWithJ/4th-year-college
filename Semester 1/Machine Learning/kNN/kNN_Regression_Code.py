import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
m = 25
Xtrain = np.linspace(0.0, 1.0, num=m)
ytrain = 10*Xtrain + np.random.normal(0.0, 1.0, m)
Xtrain = Xtrain.reshape(-1, 1)
model = KNeighborsRegressor(
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
model2 = KNeighborsRegressor(
    n_neighbors=7, weights="uniform").fit(Xtrain, ytrain)
ypred2 = model2.predict(Xtest)
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.plot(Xtest, ypred2, color="blue")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["predict", "train"])
plt.show()


def gaussian_kernel100(distances):
    weights = np.exp(-100*(distances**2))
    return weights/np.sum(weights)


def gaussian_kernel1000(distances):
    weights = np.exp(-1000*(distances**2))
    return weights/np.sum(weights)


def gaussian_kernel10000(distances):
    weights = np.exp(-10000*(distances**2))
    return weights/np.sum(weights)


model2 = KNeighborsRegressor(
    n_neighbors=7, weights=gaussian_kernel100).fit(Xtrain, ytrain)
ypred2 = model2.predict(Xtest)
model3 = KNeighborsRegressor(
    n_neighbors=7, weights=gaussian_kernel1000).fit(Xtrain, ytrain)
ypred3 = model3.predict(Xtest)
model4 = KNeighborsRegressor(
    n_neighbors=7, weights=gaussian_kernel10000).fit(Xtrain, ytrain)
ypred4 = model4.predict(Xtest)
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.plot(Xtest, ypred2, color="blue")
plt.plot(Xtest, ypred3, color="orange")
plt.plot(Xtest, ypred4, color="green")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["k=7, sigma=100", "k=7, sigma=1000", "k=7, sigma=10000", "train"])
plt.show()
