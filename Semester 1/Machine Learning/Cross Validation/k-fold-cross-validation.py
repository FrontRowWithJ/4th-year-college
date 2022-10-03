from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np

x = np.arange(0, 1, 0.05).reshape(-1, 1)
y = 10*x + np.random.normal(0.0, 1.0, x.size).reshape(-1, 1)

scores = cross_val_score(model, x, y, cv=5, scoring="neg_mean_squared_error")
print(scores)
print("Accuracy: %0.2f(+ /- %0.2f)" % (scores.mean(), scores.std()))
kf = KFold(n_splits=5)
for train, test in kf.split(x):
    model = LinearRegression().fit(x[train], y[train])
    ypred = model.predict(x[test])
    print("intercept % f, slope % f, square error % f" %
          (model.intercept_, model.coef_, mean_squared_error(y[test], ypred)))