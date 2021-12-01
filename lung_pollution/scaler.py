import pandas as pd

from sklearn.preprocessing import StandardScaler

import joblib

BUCKET_NAME = 'lungpollution-2021-predictonline'
BUCKET_TRAIN_DATA_PATH = 'data/AP_Covid_Average.csv'

class Scaler():

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
        return self.X

    def standard_scale(self, X_obj):
        scaler = StandardScaler().fit(X_obj)
        return scaler

    def save_model(self, reg):
        """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
        HINTS : use joblib library and google-cloud-storage"""

        # saving the trained model to disk is mandatory to then beeing able to upload it to storage
        # Implement here
        joblib.dump(reg, 'scaler.joblib')
        print("saved scaler.joblib locally")

if __name__ == '__main__':
    # get training data from GCP bucket
    sc = Scaler()
    X = sc.get_data()
    scaler = sc.standard_scale(X)

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    sc.save_model(scaler)
