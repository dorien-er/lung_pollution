from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler

class Scalers():
''' This file provides a class with the different scalers'''
    def __init__(self, *args, **kwargs):
        pass

    def StandardS(data):
        scaler = StandardScaler()
        return scaler.fit_transform(data)

    def RobustS(data):
        scaler = RobustScaler()
        return scaler.fit_transform(data)

    def MinMaxS(data):
        scaler = MinMaxScaler()
        return scaler.fit_transform(data)
