# id:21-21-21
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
import numpy as np
from math import ceil


df = pd.read_csv("week3.csv")
x1 = df.iloc[:, 0]
x2 = df.iloc[:, 1]
x = np.column_stack((x1, x2))
y = df.iloc[:, 2]


def show_3D_scatter_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x1, x2, y)
    plt.xlabel("x_1")
    plt.ylabel("x_2")
    ax.set_zlabel("Y")
    plt.show()


grid_width = ceil(max(x1)) * 2.5
poly = PolynomialFeatures(degree=5)
new_features = poly.fit_transform(x)
Cs = [1, 10, 25, 100, 125, 250, 500, 625, 1000]
xtest = []
grid = np.linspace(-grid_width, grid_width)
for i in grid:
    for j in grid:
        xtest.append([i, j])
xtest = np.array(xtest)
xtest_new_features = poly.fit_transform(xtest)


def plot_model(gen_model, title):
    plt.xlabel("x_1")
    plt.ylabel("x_2")
    colors = ["brown", "olive", "teal", "navy", "cyan", "red", "green", "yellow", "magenta"]
    legends = [[Line2D([0], [0], color=color, lw=4, label=C)] for color, C in zip(colors, Cs)]

    for color, C, legend, i in zip(colors, Cs, legends, range(len(Cs))):
        fig = plt.figure()
        fig.canvas.manager.set_window_title(title + str(i))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlabel("x_1")
        ax.set_ylabel("x_2")
        ax.set_zlabel("y")
        model = gen_model(alpha=1/(2*C))
        model.fit(new_features, y)
        preds = model.predict(xtest_new_features)
        ax.plot_trisurf(xtest[:, 0], xtest[:, 1], Z=preds, color=color)
        plt.legend(handles=legend, loc="best")
        plt.show()


def cross_validate_C(gen_model):
    mean_error = []
    std_error = []
    for C in Cs:
        model = gen_model(alpha=1/(2*C))
        temp = []
        kf = KFold(n_splits=5)
        for train, test in kf.split(new_features):
            model.fit(new_features[train], y[train])
            ypreds = model.predict(new_features[test])
            temp.append(mean_squared_error(y[test], ypreds))
        mean_error.append(np.array(temp).mean())
        std_error.append(np.array(temp).std())
    plt.errorbar(Cs, mean_error, yerr=std_error)
    plt.xlabel("Cs")
    plt.ylabel("Mean Square Error")
    plt.show()




# un comment the functions to use them

# cross_validate_C(gen_model=Lasso)

# cross_validate_C(gen_model=Ridge)

plot_model(gen_model=Lasso, title="Lasso Plot")

# plot_model(gen_model=Ridge, title="Ridge Plot")

# show_3D_scatter_plot()
