# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* lung_pollution/*.py

black:
	@black scripts/* lung_pollution/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr lung_pollution-*.dist-info
	@rm -fr lung_pollution.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

##---------------------------------------------------------
##			Setting up Google Cloud project
##---------------------------------------------------------
PROJECT_ID="rising-method-332408"
BUCKET_NAME=lungpollution2021
REGION=europe-west1

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}
run_api:
	uvicorn api.fast:app --reload

	##==================================================
##				Uploading dataset to the cloud
##==================================================

# path to the file to upload to GCP (the path to the file should be absolute or should match the directory where the make command is ran)
# replace with your local path to the `dataset.csv,jpeg` and make sure to put the path between quotes
#LOCAL_PATH="<path to file or folder>"

# bucket directory in which to store the uploaded file (`data` is an arbitrary name that we choose to use)
#BUCKET_FOLDER=data
BUCKET_FOLDER=upload

# will store the packages uploaded to GCP for the training
BUCKET_TRAINING_FOLDER = trainings

# name for the uploaded file inside of the bucket (we choose not to rename the file that we upload)
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

upload_data:
    # @gsutil cp train_1k.csv gs://wagon-ml-my-bucket-name/data/train_1k.csv
	@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

# --scale-tier custom \
# --master-machine-type n1-highcpu-16 \
# --worker-machine-type n1-highcpu-16 \
# --parameter-server-machine-type n1-highmem-8 \
# --worker-count 2 \
# --parameter-server-count 3
