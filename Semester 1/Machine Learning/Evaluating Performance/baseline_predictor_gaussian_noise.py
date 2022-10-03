import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import numpy as np
import numpy as np
X = np.arange(0, 1, 0.01).reshape(-1, 1)
y = np.random.normal(0.0, 1.0, X.size).reshape(-1, 1)
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)
Xtrain_poly = PolynomialFeatures(6).fit_transform(Xtrain)
Xtest_poly = PolynomialFeatures(6).fit_transform(Xtest)
X_poly = PolynomialFeatures(6).fit_transform(X)
model = LinearRegression().fit(Xtrain_poly, ytrain)
ypred = model.predict(Xtest_poly)
dummy = DummyRegressor(strategy="mean").fit(Xtrain_poly, ytrain)
ydummy = dummy.predict(Xtest_poly)
print("square error %f %f"% (mean_squared_error(ytest, ypred), mean_squared_error(ytest, ydummy)))
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.scatter(Xtest, ytest, color="black")
ypred = model.predict(X_poly)
plt.plot(X, ypred, color="blue", linewidth=3)
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["predictions", "training data"])
plt.show()
