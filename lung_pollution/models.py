from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR


class Models():

    def __init__(self):
        pass

    def LinReg(self, X, y):
        reg = LinearRegression().fit(X, y)

        return reg.score(X,y)

    def KNN(self, X, y, n_neighbors=2):
        neigh = KNeighborsRegressor(n_neighbors).fit(X,y)

        return neigh.score(X,y)

    def SVR(self, X, y):
        SVR = SVR().fit(X,y)

        return SVR.score(X,y)
