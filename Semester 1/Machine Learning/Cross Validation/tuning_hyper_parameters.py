import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.linear_model import Ridge
import numpy as np

x = np.arange(0, 1, 0.05).reshape(-1, 1)
y = 10*x + np.random.normal(0.0, 1.0, x.size).reshape(-1, 1)

mean_error = []
std_error = []
Ci_range = [0.1, 0.5, 1, 5, 10, 50, 100]
for Ci in Ci_range:
    model = Ridge(alpha=1/(2*Ci))
    temp = []
    kf = KFold(n_splits=5)
    for train, test in kf.split(x):
        model.fit(x[train], y[train])
        ypred = model.predict(x[test])
        temp.append(mean_squared_error(y[test], ypred))
    mean_error.append(np.array(temp).mean())
    std_error.append(np.array(temp).std())
plt.errorbar(Ci_range, mean_error, yerr=std_error)
plt.xlabel("Ci")
plt.ylabel("Mean square error")
plt.xlim((0, 100))
plt.show()
