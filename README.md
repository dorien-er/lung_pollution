# Lung Pollution
AI/ML project to analyze of the impact of air pollution, vaccination rate and population density on CoViD-19 cases in Germany.

## Table of contents
* [About](#about)
* [The website](#the-website)
* [Data analysis](#data-analysis)
* [Startup the project](#startup-the-project)
* [Install](#install)

## About
In this project, we build an interactive web app to visualize and analyze the impact of air pollution on CoViD-19 cases in Germany. We also analyze the impact of additional disease modulators, such as vaccination rate and population density, on CoViD-19 cases in German counties.

## The website
Check out our website: [lung-pollution](https://lung-pollution.xyz/)
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/master/lung_pollution/data/images/intro.gif" width="768"  />
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/master/lung_pollution/data/images/dataviz.gif" width="768"  />
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/master/lung_pollution/data/images/predictor.gif" width="768"  />

## Data analysis
* Datasets and sources:
  - Air pollution at the German county level, from 2010 - 2019 (Caseiro, A., von Schneidemesser, E. APExpose_DE, an air quality exposure dataset for Germany 2010–2019. Sci Data 8, 287 (2021). [Link](https://doi.org/10.1038/s41597-021-01068-6)
  - CoViD-19 statistics at the German county level. [Link](https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0/explore?location=51.836196%2C12.460149%2C7.00&showTable=true)

* Type of analysis: machine learning using SciKit-Learn, RandomForestRegressor


## Install

Clone the project:

```bash
mkdir lung_pollution && cd "$_";
git clone git@github.com:dorien-er/lung_pollution.git;
cd lung_pollution
  
```

Create a new virtual environment (opt.):

```bash
pyenv virtualenv lung_pollution;
pyenv local lung_pollution
```

Install the project:

```bash
pip install -e .
```

Functionality test to run web app on local host:

```bash
lung_pollution-run
```
