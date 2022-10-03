from sklearn.linear_model import LinearRegression
import numpy as np
Xtrain = np.arange(0, 1, 0.01).reshape(-1, 1)
ytrain = 10*Xtrain + np.random.normal(0.0, 1.0, 100).reshape(-1, 1)
model = LinearRegression().fit(Xtrain, ytrain)
print(model.intercept_, model.coef_)
