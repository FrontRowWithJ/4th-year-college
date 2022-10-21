import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.kernel_ridge import KernelRidge
import numpy as np
m = 25
Xtrain = np.linspace(0.0, 1.0, num=m)
ytrain = 10*Xtrain + np.random.normal(0.0, 1.0, m)
Xtrain = Xtrain.reshape(-1, 1)
C = 10
model = KernelRidge(alpha=1.0/C, kernel="rbf", gamma=10).fit(Xtrain, ytrain)
Xtest = np.linspace(0.0, 1.0, num=1000).reshape(-1, 1)
ypred = model.predict(Xtest)


def gaussian_kernel(distances):
    weights = np.exp(-100*(distances**2))
    return weights


model2 = KNeighborsRegressor(
    n_neighbors=m, weights=gaussian_kernel).fit(Xtrain, ytrain)
ypred2 = model2.predict(Xtest)
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.plot(Xtest, ypred, color="green")
plt.plot(Xtest, ypred2, color="blue")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["Kernel Ridge Regression", "kNN", "train"])
plt.show()
