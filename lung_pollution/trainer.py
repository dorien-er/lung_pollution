from google.cloud import storage
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

import joblib

### GCP configuration - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'lungpollution-2021-predictonline'
BUCKET_TRAIN_DATA_PATH = 'data/AP_Covid_Average.csv'
MODEL_NAME = 'LungPollutionRandomForest'
MODEL_VERSION = 'v3'
EXPERIMENT_NAME = "final_experiment"
STORAGE_LOCATION = 'models/lungpollution/model.joblib'

class Trainer():

    def __init__(self):
        pass

    def get_data(self):
        """method to get the training data (or a portion of it) from google cloud bucket"""
        df = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
        df.drop(columns=['Unnamed: 0'], inplace = True)
        df = df.rename(columns={"PM2.5_annualMean": "PM2_5_annualMean", "Fully vaccinated": "Fully_vaccinated", "Population density": "Population_density"})
        df.sort_values(['year'], axis=0, ascending=False,inplace=True,ignore_index=True)
        df= df[0:400]
        self.X = df[[
            'NO2_annualMean', 'NO_annualMean', 'O3_annualMean',
            'PM2_5_annualMean', 'fully_vaccinated', 'Population_density'
        ]]
        self.y = df["cases_per_100k"]
        return self.X, self.y

    def standard_scale(self, X_obj):
        """method that scales the data"""
        scaler = StandardScaler().fit(X_obj)
        return scaler

    def train_model(self, X_obj, y_obj):
        """method that trains the model"""
        rfg = RandomForestRegressor(min_samples_leaf=15,
                            min_samples_split=10,
                            n_estimators=100)
        rfg.fit(X_obj, y_obj)
        print("trained model")
        return rfg

    def upload_model_to_gcp(self):
        """method that uploads the model to gcp"""
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(STORAGE_LOCATION)
        blob.upload_from_filename('model.joblib')

    def upload_scaler_to_gcp(self):
        """method that uploads the scaler to gcp"""

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(STORAGE_LOCATION)
        blob.upload_from_filename('scaler.joblib')

    def save_model(self, reg):
        """method that saves the model into a .joblib file and uploads it on Google Storage /models folder"""

        # saving the trained model to disk is mandatory to then beeing able to upload it to storage
        joblib.dump(reg, 'model.joblib')
        print("saved model.joblib locally")
        # upload to gcp
        trainer.upload_model_to_gcp()
        print(
            f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}"
        )

    def save_scaler(self, scaler):
        """method that saves the scaler into a .joblib file and uploads it on Google Storage /models folder"""

        # saving the scaler to disk is mandatory to then beeing able to upload it to storage
        joblib.dump(scaler, 'scaler.joblib')
        print("saved scaler.joblib locally")
        # upload to gcp
        trainer.upload_scaler_to_gcp()
        print(
            f"uploaded scaler.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}"
        )


if __name__ == '__main__':
    # get training data from GCP bucket
    trainer = Trainer()
    X_train, y_train = trainer.get_data()

    # fit scaler to the training data
    scaler = trainer.standard_scale(X_train)

    # save the fitted scaler to GCP bucket
    trainer.save_scaler(scaler)

    # transform training data with fitted scaler
    X_train = scaler.transform(X_train)

    # train model
    reg = trainer.train_model(X_train, y_train)

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    trainer.save_model(reg)
