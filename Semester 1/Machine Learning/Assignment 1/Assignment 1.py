# id:17--34-17 
from cgitb import handler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
df = pd.read_csv("week2.csv")
x1 = df.iloc[:, 0]
x2 = df.iloc[:, 1]
x = np.column_stack((x1, x2))
y = df.iloc[:, 2]
blue = [0, 0, 1]
green = [0, 1, 0]
c = np.array([blue if val == 1 else green for val in y])


fig, ax = plt.subplots()
legend_elements = [Line2D([0], [0], color='b', lw=4, label='+1'), Line2D(
    [0], [0], color='g', lw=4, label='-1')]

plt.xlabel("x_1")
plt.ylabel("x_2")
plt.legend(handles=legend_elements, loc="best")
plt.scatter(x1, x2, marker="+", c=c)
plt.show()
