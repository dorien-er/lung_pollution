import joblib
from termcolor import colored
from dataviz import DataViz

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor
from sklearn.svm import SVR

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler


class Pipe():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y
        # # for MLFlow
        # self.experiment_name = EXPERIMENT_NAME

    # def set_experiment_name(self, experiment_name):
    #     '''defines the experiment name for MLFlow'''
    #     self.experiment_name = experiment_name

    def set_pipeline(self, scaler=StandardScaler(), model=KNeighborsRegressor(n_neighbors=2)):
        self.pipeline = Pipeline([('scaler', scaler),
                                  ('model', model)])

    def run(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)

    def evaluate(self):
        return self.run().score(self.X,self.y)

    def save_model_locally(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, 'model.joblib')
        print(colored("model.joblib saved locally", "green"))

if __name__ == "__main__":
    p1 = DataViz()
    df = p1.load_data()

    X = df[['NO2_annualMean', 'NO_annualMean', 'O3_annualMean', 'PM10_annualMean','PM2_5_annualMean', 'Fully_vaccinated', 'Population_density']]
    y = df[['deaths_per_100k']]

    pipe = Pipe(X,y)
    pipe.run()
    R_squared = pipe.evaluate()
    print(f"R_squared: {R_squared}")
    pipe.save_model_locally()
