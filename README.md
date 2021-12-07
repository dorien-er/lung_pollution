# Lung Pollution
Analyzing the impact of air pollutions, vaccination rate and population density on CoViD-19 cases in germany

## Table of contents
* [About](#about)
* [The looks of the website](#the-looks-of-the-website)
* [Data analysis](#data-analysis)
* [Startup the project](#startup-the-project)
* [Install](#install)

## About
In this project, we'll analyze the impact of air pollutions on CoViD-19 cases in germany, and also to check if there is also connection between the vaccination rate, population density of each county and CoViD-19 cases.

## The looks of the website
Check out how the website looks like, here is the link [lung-pollution](https://rising-method-332408.ew.r.appspot.com/)
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/rifqi-frontend-15/lung_pollution/data/images/intro.gif" width="768"  />
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/rifqi-frontend-15/lung_pollution/data/images/dataviz.gif" width="768"  />
<p align="center"><img src="https://github.com/dorien-er/lung_pollution/blob/rifqi-frontend-15/lung_pollution/data/images/predictor.gif" width="768"  />

## Data analysis
- Document here the project: lung_pollution
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

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
