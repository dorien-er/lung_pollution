from google.cloud import storage
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

import joblib

### GCP configuration - - - - - - - - - - - - - - - - - - -

# /!\ you should fill these according to your account

### GCP Project - - - - - - - - - - - - - - - - - - - - - -

# not required here

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'lungpollution-2021-predictonline'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

# train data file location
# /!\ here you need to decide if you are going to train using the provided and uploaded data/train_1k.csv sample file
# or if you want to use the full dataset (you need need to upload it first of course)
BUCKET_TRAIN_DATA_PATH = 'data/AP_Covid_Average.csv'

##### Training  - - - - - - - - - - - - - - - - - - - - - -

# not required here

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'LungPollutionRandomForest'

# model version folder name (where the trained model.joblib file will be stored)
MODEL_VERSION = 'v3'

### GCP AI Platform - - - - - - - - - - - - - - - - - - - -

# not required here

### - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
        scaler = StandardScaler()
        scaler.fit(X_obj)  # Fit scaler to feature
        X_obj = scaler.transform(X_obj)  #Scale
        return X_obj

    def train_model(self, X_obj, y_obj):
        """method that trains the model"""
        rfg = RandomForestRegressor(min_samples_leaf=15,
                            min_samples_split=10,
                            n_estimators=100)
        rfg.fit(X_obj, y_obj)
        print("trained model")
        return rfg

    def upload_model_to_gcp(self):

        client = storage.Client()

        bucket = client.bucket(BUCKET_NAME)

        blob = bucket.blob(STORAGE_LOCATION)

        blob.upload_from_filename('model.joblib')

    def save_model(self, reg):
        """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
        HINTS : use joblib library and google-cloud-storage"""

        # saving the trained model to disk is mandatory to then beeing able to upload it to storage
        # Implement here
        joblib.dump(reg, 'model.joblib')
        print("saved model.joblib locally")

        # Implement here
        trainer.upload_model_to_gcp()
        print(
            f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}"
        )

if __name__ == '__main__':
    # get training data from GCP bucket
    trainer = Trainer()
    X_train, y_train = trainer.get_data()
    X_train = trainer.standard_scale(X_train)

    # train model (locally if this file was called through the run_locally command
    # or on GCP if it was called through the gcp_submit_training, in which case
    # this package is uploaded to GCP before being executed)
    reg = trainer.train_model(X_train, y_train)

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    trainer.save_model(reg)
