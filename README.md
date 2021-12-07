# Lung Pollution
Assessment of the impact of air pollution, vaccination rate and population density on CoViD-19 cases in Germany.

## Table of contents
* [About](#about)
* [The website](#the-website)
* [Data analysis](#data-analysis)
* [Startup the project](#startup-the-project)
* [Install](#install)

## About
In this project, we analyze the impact of air pollution on CoViD-19 cases at the county-level in Germany. We also analyze the impact of  additional disease modulators, such as vaccination rate and population density, on CoViD-19 cases in German counties.

## The website
Check out our website: [lung-pollution](https://rising-method-332408.ew.r.appspot.com/)
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/master/lung_pollution/data/images/intro.gif" width="768"  />
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/master/lung_pollution/data/images/dataviz.gif" width="768"  />
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/master/lung_pollution/data/images/predictor.gif" width="768"  />

## Data analysis
- Datasets and sources:
  -- Air pollution at the German county level, from 2010 - 2019 (Caseiro, A., von Schneidemesser, E. APExpose_DE, an air quality exposure dataset for Germany 2010–2019. Sci Data 8, 287 (2021). https://doi.org/10.1038/s41597-021-01068-6)
  --  CoViD-19 statistics at the German county level (https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0/explore?location=51.836196%2C12.460149%2C7.00&showTable=true)

- Type of analysis: machine learning using SciKit-Learn, RandomForestRegressor

## Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for lung_pollution in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/lung_pollution`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "lung_pollution"
git remote add origin git@github.com:{group}/lung_pollution.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
lung_pollution-run
```

## Install

Go to `https://github.com/{group}/lung_pollution` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/lung_pollution.git
cd lung_pollution
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
lung_pollution-run
```
