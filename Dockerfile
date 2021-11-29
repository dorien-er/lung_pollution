
# # write some code to build your image
# FROM python:3.8.6-buster

# COPY api /api
# COPY TaxiFareModel /TaxiFareModel
# COPY requirements.txt /requirements.txt
# COPY model.joblib /model.joblib
# COPY le-wagon-data-735-3ea4c8134601.json /credentials.json

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
###############################################################################
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim-buster

# Copy local code to the container image.
ENV APP_HOME /app
ENV PYTHONUNBUFFERED True
WORKDIR $APP_HOME

# Install Python dependencies and Gunicorn
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir gunicorn
RUN groupadd -r app && useradd -r -g app app

# Copy the rest of the codebase into the image
COPY --chown=app:app . ./
USER app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available in Cloud Run.
CMD exec gunicorn --bind :$PORT --log-level info --workers 1 --threads 8 --timeout 0 app:server
