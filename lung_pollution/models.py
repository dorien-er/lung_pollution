from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import Ridge, Lasso, LinearRegression, ElasticNet
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from xgboost import XGBRegressor

from sklearn.model_selection import cross_validate
import pandas as pd

class Models():

    def __init__(self, file_name = '../lung_pollution/data/covid_pollution_complete.csv'):
        self.file_name = file_name

    def load_data(self):
        df_covid_AP = pd.read_csv(self.file_name )
        df_covid_AP.drop(columns=['Column1'], inplace = True)
        df_covid_AP.sort_values(['year'], axis=0, ascending=False,inplace=True,ignore_index=True)
        self.df = df_covid_AP[0:400]
        return self.df

    ##### Scaling
    def standard_scale(self, X_obj):
        scaler = StandardScaler()
        scaler.fit(X_obj)  # Fit scaler to feature
        X_obj = scaler.transform(X_obj)  #Scale
        return X_obj

    ##### Model
    def regression(self, X_obj, y_obj, model):
        model = model.fit(X_obj,y_obj)
        cv_results_model = cross_validate(model, X_obj, y_obj, cv=5,
                                scoring='r2'
                                )
        model = model.fit(X_obj, y_obj)
        model.score(X_obj, y_obj)
        return [model.score(X_obj, y_obj), cv_results_model['test_score'].mean()]

if __name__ == '__main__':
    model = Models()
    df_covid_AP_2019 = model.load_data()
    X_obj = df_covid_AP_2019[[
        'NO2_totMean', 'NO_totMean', 'O3_totMean','PM2_5_totMean',
        'fully_vaccinated', 'Population_density']]
    y_obj = df_covid_AP_2019['cases_per_100k']
    model_list = [
        LinearRegression(),
        Ridge(),
        Lasso(),
        ElasticNet(),
        KNeighborsRegressor(n_neighbors=4, weights='distance', leaf_size=10, p=1),
        SVR(),
        AdaBoostRegressor(n_estimators=10, learning_rate= 1.2),
        RandomForestRegressor(min_samples_leaf=15,
                              min_samples_split=10,
                              n_estimators = 100),
        XGBRegressor(max_depth=10, n_estimators=100, learning_rate=0.1)]
    score_list = [[0,0]]
    for i in model_list:
        score_list.append(model.regression(X_obj, y_obj, i))
    data = pd.DataFrame(score_list)
    data.to_csv('score_list_new.csv', index=False, header=False)
