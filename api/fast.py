from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# http://127.0.0.1:8000/predict?NO=4.7&NO2=4.8&PM2_5=21.3&O3=46.2&vax=0.71&density=230.118

@app.get("/")
def index():
    return {"this": "is a test"}

@app.get("/predict")
def predict(NO,
            NO2,
            PM2_5,
            O3,
            vax,
            density):

    X_test = pd.DataFrame(dict(NO=[float(NO)],
                               NO2 = [float(NO2)],
                               PM2_5 = [float(PM2_5)],
                               O3 = [float(O3)],
                               vax = [float(vax)],
                               density = [float(density)]))

    scaler = joblib.load('scaler.joblib')
    X_test = scaler.transform(X_test)
    model = joblib.load('model.joblib')
    results = model.predict(X_test)
    pred = float(results[0])
    return dict(prediction=pred)
