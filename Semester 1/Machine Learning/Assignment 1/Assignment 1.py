# id:17--34-17
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

def print_eqation(model: LinearSVC):
  print("y = %f + %fx1 + %fx2" % (model.intercept_, model.coef_[0][0], model.coef_[0][1]))

figureNo = 0
df = pd.read_csv("week2.csv")
x1 = df.iloc[:, 0]
x2 = df.iloc[:, 1]
x = np.column_stack((x1, x2))
y = df.iloc[:, 2]
blue = [0, 0, 1]
green = [0, 1, 0]
red = [1, 0, 0]
yellow = [1, 1, 0]
c0 = np.array([blue if val == 1 else green for val in y])

fig, ax = plt.subplots()

legend_elements = [Line2D([0], [0], color="blue", lw=4, label='real +1'),
                   Line2D([0], [0], color="green", lw=4, label='real -1'),
                   Line2D([0], [0], color="yellow", lw=4, label="pred +1"),
                   Line2D([0], [0], color="red", lw=4, label="pred -1")]

plt.xlabel("x_1")
plt.ylabel("x_2")
plt.legend(handles=legend_elements, loc="best")
plt.scatter(x1, x2, marker="o", c=c0)

# Performing logistic regression
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
model = LogisticRegression(penalty="none", solver="lbfgs")
model.fit(xtrain, ytrain)

o0 = model.intercept_[0]
o1 = model.coef_[0][0]
o2 = model.coef_[0][1]
ypred = model.predict(xtest)

c1 = np.array([yellow if val == 1 else red for val in ypred])
xtest0 = xtest[:, 0]
xtest1 = xtest[:, 1]

plt.scatter(xtest0, xtest1, marker="+", c=c1)


def plot_decision_boundary(coef_, intercept_, plt):
    o = coef_[0]
    m = -o[0] / o[1]
    c = -(intercept_[0]) / o[1]
    x = np.linspace(-1, 1)
    y = m * x + c
    plt.plot(x, y, 'b-', label="Decision Boundary")


plot_decision_boundary(model.coef_, model.intercept_, plt)
# fig.canvas.manager.set_window_title("Figure " + str(figureNo))
# figureNo += 1
print_eqation(model)
# plt.show()

Cs = [0.001, 0.01, 0.1, 1, 10, 100]
for C in Cs:
    model = LinearSVC(C=C, max_iter=10000 if C ==
                      100 else 1000).fit(xtrain, ytrain)
    preds = model.predict(xtest)
    xtest0 = xtest[:, 0]
    xtest1 = xtest[:, 1]
    c0 = np.array([blue if val == 1 else green for val in ytest])
    c1 = np.array([yellow if val == 1 else red for val in ypred])
    plt.clf()
    fig, ax = plt.subplots()
    plt.xlabel("x_1")
    plt.ylabel("x_2")
    plt.legend(handles=legend_elements, loc="best")
    plt.scatter(xtest0, xtest1, marker="o", c=c0)
    plt.scatter(xtest0, xtest1, marker="+", c=c1)
    plot_decision_boundary(model.coef_, model.intercept_, plt)
    
    fig.canvas.manager.set_window_title("Figure " + str(figureNo))
    figureNo += 1
    # plt.show()
    print_eqation(model)


newX = [[l[0], l[1], l[0] * l[0], l[1] * l[1]] for l in x]
xtrain, xtest, ytrain, ytest = train_test_split(newX, y, test_size=0.2)
model = LogisticRegression(penalty="none", solver="lbfgs")
model.fit(xtrain, ytrain)
preds = model.predict(xtest)


c0 = np.array([blue if val == 1 else green for val in ytest])
c1 = np.array([yellow if val == 1 else red for val in ypred])
plt.clf()
fig, ax = plt.subplots()
plt.xlabel("x_1")
plt.ylabel("x_2")
xtest0 = [l[0] for l in xtest]
xtest1 = [l[1] for l in xtest]
plt.legend(handles=legend_elements, loc="best")
plt.scatter(xtest0, xtest1, marker="o", c=c0)
plt.scatter(xtest0, xtest1, marker="+", c=c1)
fig.canvas.manager.set_window_title("Figure " + str(figureNo))
figureNo += 1
# plt.show()
# print_eqation(model)


