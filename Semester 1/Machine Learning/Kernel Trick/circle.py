from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
m = 100
Xtrain = 0.5*np.random.randn(m, 2)
ytrain = np.sign((Xtrain[:, 0]**2+Xtrain[:, 1]**2) -
                 0.5+np.random.normal(0, 0.2, m))
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
xx, yy = np.meshgrid(np.linspace(-1, 1, 50), np.linspace(-1, 1, 50))
Xtest = np.c_[xx.ravel(), yy.ravel()]
ytest = np.sign((xx**2+yy**2)-0.5)
model = SVC(C=1000, kernel="rbf", gamma=1).fit(Xtrain, ytrain)
ypred = model.predict(Xtest)
plt.contour(xx, yy, ypred.reshape(xx.shape),
            c=ypred, cmap=plt.cm.brg, levels=2)
# plt.scatter(xx,yy,marker=".",c=ypred.reshape(xx.shape),cmap=plt.cm.brg)
plt.scatter(Xtrain[:, 0], Xtrain[:, 1], marker="+", c=ytrain, cmap=plt.cm.brg)
plt.xlim((-1, 1))
plt.ylim((-1, 1))
plt.xlabel("input x_1")
plt.ylabel("input x_2")
plt.show()


def gaussian_kernel(distances):
    weights = np.exp(-10*(distances**2))
    return weights


model = KNeighborsClassifier(
    n_neighbors=m, weights=gaussian_kernel).fit(Xtrain, ytrain)
ypred = model.predict(Xtest)
plt.contour(xx, yy, ypred.reshape(xx.shape),
            c=ypred, cmap=plt.cm.brg, levels=2)
plt.scatter(Xtrain[:, 0], Xtrain[:, 1], marker="+", c=ytrain, cmap=plt.cm.brg)
plt.xlim((-1, 1))
plt.ylim((-1, 1))
plt.xlabel("input x_1")
plt.ylabel("input x_2")
plt.show()
