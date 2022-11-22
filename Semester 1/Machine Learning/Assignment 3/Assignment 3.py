# 1st Data set: # id:5-10-5-0
# 2nd Data set: # id:5--10-5-0


from typing import List, TypedDict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import roc_curve
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import PolynomialFeatures


class Dataset:
    def __init__(self, data) -> None:
        self.x1 = data[:, 0]
        self.x2 = data[:, 1]
        self.x = np.column_stack((self.x1, self.x2))
        self.y = data[:, 2]

    def getData(self, fields: list[str]):
        result = []
        for field in fields:
            if (hasattr(self, field)):
                result.append(self[field])
        return result

    def __iter__(self):
        return DatasetIterator(self)


class DatasetIterator:
    def __init__(self, dataset: Dataset) -> None:
        self._datalist = [dataset.x1, dataset.x2, dataset.x, dataset.y]
        self._index = 0

    def __next__(self):
        if (self._index < len(self._datalist)):
            res = self._datalist[self._index]
            self._index += 1
            return res
        raise StopIteration


def readData() -> tuple[Dataset, Dataset]:
    try:
        file = open("week4.csv", "r")
        lines = file.readlines()
        dataset = -1
        data = [[], []]
        for line in lines:
            if line[0] == "#":
                dataset = dataset + 1
            else:
                data[dataset].append([float(n) for n in line.split(",")])
        return (Dataset(np.array(data[0])), Dataset(np.array(data[1])))
    finally:
        file.close()


def genPolynomialFeatures(features, degree):
    poly = PolynomialFeatures(degree=degree)
    return poly.fit_transform(features)


# First of all plot the training data

def plot_original_data(dataset: Dataset) -> None:
    x1, x2, _, y = dataset
    _, ax = plt.subplots()
    legend = [Line2D([0], [0], color="blue", lw=4, label='+1'),
              Line2D([0], [0], color="green", lw=4, label='-1')]
    blue = [0, 0, 1]
    green = [0, 1, 0]
    c = np.array([blue if val == 1 else green for val in y])
    ax.set_xlabel("x_1")
    ax.set_ylabel("x_2")
    ax.legend(handles=legend, loc="best")
    ax.scatter(x1, x2, marker="o", c=c)
    plt.show()


# plot_original_data(dataset0)

class ConfusionMatrix(TypedDict):
    TN: int
    FP: int
    FN: int
    TP: int


def maxIndex(l: List):
    return max(range(len(l)), key=l.__getitem__)

# 00 = TN
# 01 = FP
# 10 = FN
# 11 = TP


def cross_validate_C(Cs: list, features: list, y: list) -> tuple[float, list[float], list[float]]:
    mean_error = []
    std_error = []
    for C in Cs:
        model = RidgeClassifier(alpha=1 / (2 * C))
        scores = cross_val_score(model, X=features, y=y, cv=5, scoring="f1")
        mean_error.append(np.array(scores).mean())
        std_error.append(np.array(scores).std())
    print('%.4f' % np.array(mean_error).mean())
    plt.errorbar(Cs, mean_error, yerr=std_error)
    plt.xlabel("Cs")
    plt.ylabel("F1 score")
    plt.show()
    #! plot the std error and mean using an error bar
    return maxIndex(mean_error)


def cross_validate_model(degrees: list, Cs: list, dataset: Dataset) -> tuple[int, float]:
    mean_error: list[float] = []
    std_error: list[float] = []
    best_Cs: list[float] = []
    for degree in degrees:
        _, _, x, y = dataset
        poly = PolynomialFeatures(degree=degree)
        features = poly.fit_transform(x)
        C_index = cross_validate_C(Cs, features, y)
        best_Cs.append(Cs[C_index])
        model = RidgeClassifier(alpha=1 / 2 * Cs[C_index])
        scores = cross_val_score(model, X=features, y=y, cv=5, scoring="f1")
        mean_error.append(np.array(scores).mean())
        std_error.append(np.array(scores).std())
    plt.errorbar(degrees, mean_error, yerr=std_error)
    plt.xlabel("Degrees")
    plt.ylabel("F1 Score")
    plt.show()
    best_degree_index = maxIndex(mean_error)
    return (degrees[best_degree_index], best_Cs[best_degree_index])


def cross_validate_k(ks: list, dataset: Dataset) -> int:
    mean_error = []
    std_error = []
    for k in ks:
        _, _, x, y = dataset
        model = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(model, x, y, cv=5, scoring="f1")
        mean_error.append(np.array(scores).mean())
        std_error.append(np.array(scores).std())

    plt.errorbar(ks, mean_error, yerr=std_error)
    plt.xlabel("Ks")
    plt.ylabel("F1 Score")
    plt.show()
    return maxIndex(mean_error)


def plot_roc_curve(ys: list[int], logisticPreds: list[int], kNNPreds: list[int], randomPreds: list[int]):
    fpr, tpr, _ = roc_curve(ys, logisticPreds)
    plt.plot(fpr, tpr, color="orange")
    fpr, tpr, _ = roc_curve(ys, kNNPreds)
    plt.plot(fpr, tpr, color="blue")
    fpr, tpr, _ = roc_curve(ys, randomPreds)
    plt.plot(fpr, tpr, color="red")
    plt.legend(["Logistic Regression", "kNN", "Random"])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True positive Rate")
    plt.show()


def gen_confusion_matrix(ys: list[int], preds: list[int]):
    ys = [1 if y == 1 else 0 for y in ys]
    preds = [1 if pred == 1 else 0 for pred in preds]
    res = [0, 0, 0, 0]
    for y, pred in zip(ys, preds):
        res[(y << 1) | pred] += 1
    return {"TN": res[0], "FP": res[1], "FN": res[2], "TP": res[3]}


def random_preds(l):
    np.random.seed(0)
    return np.array([-1 if n <= 0.5 else 1 for n in np.random.rand(l)])


def do_confusion_matrix(dataset: Dataset, degree: int, C: float, K: int) -> tuple[list[int], list[int], list[int], list[int]]:
    kf = KFold(n_splits=5)
    _, _, x, y = dataset
    polyFeatures = genPolynomialFeatures(x, degree)
    for train, test in kf.split(x):
        model = RidgeClassifier(alpha=1 / (2 * C))
        model.fit(polyFeatures[train], y[train])
        ypredsRidge = model.predict(polyFeatures[test])
        confusionMatrix = gen_confusion_matrix(y[test], ypredsRidge)
        print(confusionMatrix, "Ridge")
        model = KNeighborsClassifier(n_neighbors=K)
        model.fit(polyFeatures[train], y[train])
        ypredsKNN = model.predict(polyFeatures[test])
        confusionMatrix = gen_confusion_matrix(y[test], ypredsKNN)
        print(confusionMatrix, "kNN")
        ypredsRandom = random_preds(len(y[test]))
        confusionMatrix = gen_confusion_matrix(y[test], ypredsRandom)
        print(confusionMatrix, "Random")
        return (y[test], ypredsRidge, ypredsKNN, ypredsRandom)


dataset0, dataset1 = readData()
# foo, _, _ = cross_validate_model(degrees, Cs, dataset0)

# k_index, mean, _ = cross_validate_k(ks, dataset0)
# print(ks[k_index], mean)
# print(foo)


def run_assignment(dataset: Dataset, bests: tuple[int, int, int]):
    Cs = [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]
    ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    degrees = [1, 2, 3, 4, 5, 6]
    best_degree, best_C, = cross_validate_model(degrees, Cs, dataset)

    best_K = ks[cross_validate_k(ks, dataset)]
    print(best_degree, best_C, best_K)
    # best_degree, best_C, best_K = bests
    # print(ks[k_index], mean)
    ys, logisticPreds, kNNPreds, randomPreds = do_confusion_matrix(
        dataset, best_degree, best_C, best_K)
    plot_roc_curve(ys, logisticPreds, kNNPreds, randomPreds)


# Best values for first dataset
# best_degree = 5
# best_C = 1
# best_K = 6
# run_assignment(dataset1, (5, 1, 6))

# Best values for 2nd dataset
# best_degree 1
# best_C = 0.001
# best_K = 8
run_assignment(dataset1, (1, 0.001, 8))
