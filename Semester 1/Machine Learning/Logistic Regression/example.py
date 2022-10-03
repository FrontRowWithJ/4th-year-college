from sklearn.linear_model import LogisticRegression
import numpy as np
Xtrain = np.random.uniform(0, 1, 100)
ytrain = np.sign(Xtrain - 0.5)
Xtrain = Xtrain.reshape(-1, 1)
model = LogisticRegression(penalty="none", solver="lbfgs")
model.fit(Xtrain, ytrain)
print("intercept %f, slope %f" % (model.intercept_, model.coef_))
print("y = %fx %s %f" % (model.coef_, "+" if model.intercept_ >= 0 else "-",  abs(model.intercept_)))