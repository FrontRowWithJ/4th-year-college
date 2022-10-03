from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
X = np.arange(0, 1, 0.05).reshape(-1, 1)
y = 10*X + np.random.normal(0.0, 1.0, X.size).reshape(-1, 1)
for i in range(6):
    test_size = min(.2 * i + .1, 1)
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=test_size)
    model = LinearRegression().fit(Xtrain, ytrain)
    ypred = model.predict(Xtest)
    print("intercept %f, slope %f, square error %f, test_size %f" %
          (model.intercept_, model.coef_, mean_squared_error(ytest, ypred), test_size))
