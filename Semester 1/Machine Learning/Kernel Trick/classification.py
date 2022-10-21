from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
m = 25
Xtrain = np.linspace(0.0, 1.0, num=m)
ytrain = np.sign(Xtrain-0.5+np.random.normal(0, 0.2, m))
Xtrain = Xtrain.reshape(-1, 1)


def gaussian_kernel(distances):
    weights = np.exp(-100*(distances**2))
    return weights


model = KNeighborsClassifier(
    n_neighbors=25, weights=gaussian_kernel).fit(Xtrain, ytrain)
Xtest = np.linspace(0.0, 1.0, num=1000).reshape(-1, 1)
ypred = model.predict(Xtest)
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.plot(Xtest, ypred, color="green")
model = SVC(C=1000, kernel="rbf", gamma=50).fit(Xtrain, ytrain)
ypred = model.predict(Xtest)
plt.plot(Xtest, ypred, color="blue")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["kNN", "SVM", "train"])
plt.show()
