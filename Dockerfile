FROM python:3.8.12-buster

COPY api /api
COPY lung_pollution /lung_pollution
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt
COPY /Users/dorienroosen/code/dorien-er/gcp/wagon-bootcamp-332015-e30a9a58d666.json /credentials.json
COPY predict.py /predict.py

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
