import matplotlib.pyplot as plt
plt.rc("font", size=18)
plt.rcParams["figure.constrained_layout.use"] = True
plt.scatter(Xtrain, ytrain, color="red", marker="+")
plt.scatter(Xtrain, ypred, color="green", marker="+")
plt.xlabel("input x")
plt.ylabel("output y")
plt.legend(["train", "predict"])
plt.show()
