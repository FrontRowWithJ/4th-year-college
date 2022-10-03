from sklearn.svm import LinearSVC
model = LinearSVC(C=1.0).fit(Xtrain, ytrain)
print("intercept % f, slope % f" % (model.intercept_, model.coef_))
