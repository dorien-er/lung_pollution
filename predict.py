import os
from sklearn.preprocessing import StandardScaler

import joblib
import pandas as pd
from google.cloud import storage
from sklearn.metrics import r2_score


PATH_TO_LOCAL_MODEL = 'model.joblib'
BUCKET_TEST_DATA_PATH = 'data/test.csv'
BUCKET_NAME = "lungpollution-2021-predictonline"  # ⚠️ replace with your BUCKET NAME
MODEL_NAME = 'LungPollutionRandomForest'


def get_test_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    df = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TEST_DATA_PATH}")
    X_test = df[[
        'NO2_annualMean', 'NO_annualMean', 'O3_annualMean', 'PM10_annualMean',
        'PM2_5_annualMean', 'fully_vaccinated', 'Population_density'
    ]]
    y_test = df["cases_per_100k"]
    return X_test, y_test

    # def download_model(model_directory="PipelineTest",
    #                    bucket=BUCKET_NAME,
    #                    rm=True):

    #     client = storage.Client().bucket(bucket)

    #     storage_location = 'models/{}/versions/{}/{}'.format(
    #         MODEL_NAME, model_directory, 'model.joblib')
    #     blob = client.blob(storage_location)
    #     blob.download_to_filename('model.joblib')
    #     print("=> pipeline downloaded from storage")
    #     model = joblib.load('model.joblib')
    #     if rm:
    #         os.remove('model.joblib')
    #     return model

def standard_scale(X_obj):
    scaler = StandardScaler()
    scaler.fit(X_obj)  # Fit scaler to feature
    X_obj = scaler.transform(X_obj)  #Scale
    return X_obj


def get_model(path_to_joblib):
    pipeline = joblib.load(path_to_joblib)
    return pipeline

def evaluate_model(y, y_pred):
    R2 = round(r2_score(y, y_pred), 2)
    return R2


# def generate_submission_csv():
#     df_test = get_test_data()
#     pipeline = joblib.load(PATH_TO_LOCAL_MODEL)
#     if "best_estimator_" in dir(pipeline):
#         y_pred = pipeline.best_estimator_.predict(df_test)
#     else:
#         y_pred = pipeline.predict(df_test)
#     df_test["fare_amount"] = y_pred
#     df_sample = df_test[["key", "fare_amount"]]
#     name = f"predictions_test_ex.csv"
#     df_sample.to_csv(name, index=False)
#     print("prediction saved under kaggle format")

if __name__ == '__main__':
    X_test, y_test = get_test_data()
    # ⚠️ in order to push a submission to kaggle you need to use the WHOLE dataset
    #generate_submission_csv()
    X_test = standard_scale(X_test)
    model = get_model('/Users/dorienroosen/code/dorien-er/lung_pollution/model.joblib')
    y_pred = model.predict(X_test)
    R2 = evaluate_model(y_test, y_pred)
    print(R2)
