import pandas as pd
import numpy as np
import json


def load_covid():
    covid_df = pd.read_csv('./raw_data/RKI_corona_landskreise.csv')
    return covid_df


def preproc_covid(covid_df):
    #1 Keep only relevant features
    covid_df = covid_df[[
        'BL', 'county', 'EWZ', 'Shape__Area', 'death_rate', 'cases', 'deaths',
        'cases_per_100k'
    ]]

    #2 Merge Berlin Counties
    # Pollution data-set considers Berlin as 1 county,
    # whereas Covid dataset considers 11 counties within Berlin.
    # Collapse 11 counties in Covid dataset into one to match pollution dataset.
    berlin = covid_df[covid_df["BL"] == 'Berlin']

    ## Sum relevant features
    berlin_sum = berlin[['Shape__Area', 'cases', 'deaths', 'EWZ']].sum()

    ## Average relevant features
    berlin_average = berlin[['death_rate', 'cases_per_100k']].mean()

    covid_df['county'][399] = 'Berlin'
    covid_df['cases'][399] = berlin_sum.cases
    covid_df['Shape__Area'][399] = berlin_sum.Shape__Area
    covid_df['EWZ'][399] = berlin_sum.EWZ
    covid_df['deaths'][399] = berlin_sum.deaths
    covid_df['death_rate'][399] = berlin_average.death_rate
    covid_df['cases_per_100k'][399] = berlin_average.cases_per_100k

    covid_df.drop(
        index=[400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410],
        axis=0,
        inplace=True)

    return covid_df

def feat_eng_covid(covid_df):
    #1 Create deaths per 100k feature
    ### EWZ is einwohnerzahl is population count
    covid_df[
        'deaths_per_100k'] = covid_df['deaths'] / covid_df['EWZ'] * 100_000

    #2 Create Population Density features
    covid_df['Population_density'] = covid_df['EWZ'] / covid_df[
        'Shape__Area'] * 1_000_000

    #3 Create vaccination rate feature
    ### Map vaccinationrate per bundesland to the dataset
    d = {
        'Berlin': 0.688,
        'Rheinland-Pfalz': 0.678,
        'Bayern': 0.663,
        'Baden-Württemberg': 0.662,
        'Thüringen': 0.621,
        'Sachsen-Anhalt': 0.645,
        'Niedersachsen': 0.699,
        'Brandenburg': 0.617,
        'Sachsen': 0.578,
        'Hessen': 0.672,
        'Nordrhein-Westfalen': 0.715,
        'Schleswig-Holstein': 0.725,
        'Mecklenburg-Vorpommern': 0.665,
        'Saarland': 0.746,
        'Bremen': 0.797,
        'Hamburg': 0.738
    }

    covid_df['Fully_vaccinated'] = covid_df['BL'].map(d)
    return covid_df

def load_pollution():
    pollution_df = pd.read_csv('./raw_data/APexpose.csv',
                               sep=';',
                               decimal='.',
                               encoding='Windows-1252')
    return pollution_df

def preproc_pollution(pollution_df):
    #1 Keep only 'average' scenario
    ## 3 scenarios (rural, urban, average): average combines rural and urban > keep only average
    pollution_df = pollution_df[pollution_df.scenario == 'average']

    ## Some funny characters present in county names of APExpose dataset
    ## Replace those characters with equivalent German character to match Covid dataset and be able to merge
    pollution_df['county'] = pollution_df['county'].apply(lambda x: x.replace('Ÿ','ü'))
    pollution_df['county'] = pollution_df['county'].apply(lambda x: x.replace('š','ö'))
    pollution_df['county'] = pollution_df['county'].apply(lambda x: x.replace('§','ß'))
    pollution_df['county'] = pollution_df['county'].apply(lambda x: x.replace('Š','ä'))

    #3 Match counties to Covid
    ## Counties were present during 2010-2019 (pollution dataset),
    ## but were later merged and are therefore not present in covid dataset (2021)
    pollution_df = pollution_df[pollution_df.county != 'Eisenach']
    pollution_df = pollution_df[pollution_df.county != 'Osterode am Harz']

    #4 Keep relevant features only
    pollution_df = pollution_df[[
        'county', 'year', 'NO2_annualMean', 'NO2_hrOver200', 'NO_annualMean',
        'O3_annualMean', 'O3_daysOver120', 'O3_dailyMaxAnnualMean',
        'O3_dailyHourlyMax', 'O3_daily8HrMax', 'PM10_annualMean',
        'PM10_daysOver50', 'PM2.5_annualMean'
    ]]

    #4 Sort per county and year
    pollution_df.sort_values(['county', 'year'],
                             axis=0,
                             ascending=True,
                             inplace=True,
                             ignore_index=True)

    return pollution_df

def load_save_geojson():
    url = 'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/1_sehr_hoch.geo.json'
    dfObj = pd.read_json(url)
    list_ids = []
    list_counties = []

    for i in range(len(dfObj['features'])):
        list_ids.append(dfObj["features"][i]["id"])
        list_counties.append(dfObj["features"][i]["properties"]["NAME_3"])

    geo_df = pd.DataFrame(list(zip(list_ids, list_counties)),
            columns=['Id', 'County'])
    geo_df.to_csv('./lung_pollution/data/geoJSON.csv', encoding='utf-8-sig')


def merge_covid_pollution(covid_df, pollution_df):
    merge_df = pollution_df.merge(covid_df, how='inner', on='county')
    merge_df = merge_df.rename(
        columns={'PM2.5_annualMean': 'PM2_5_annualMean'})
    merge_df = merge_df[[
        'county', 'year', 'NO2_annualMean', 'NO2_hrOver200', 'NO_annualMean',
        'O3_annualMean', 'O3_daysOver120', 'O3_dailyMaxAnnualMean',
        'O3_dailyHourlyMax', 'O3_daily8HrMax', 'PM10_annualMean',
        'PM2_5_annualMean', 'cases_per_100k', 'deaths_per_100k',
        'Population_density', 'Fully_vaccinated'
    ]]
    merge_df.to_csv('./lung_pollution/data/covid_pollution.csv',
                    encoding='utf-8-sig')

if __name__ == '__main__':
    covid_df = load_covid()
    covid_df = preproc_covid(covid_df)
    covid_df = feat_eng_covid(covid_df)

    pollution_df = load_pollution()
    pollution_df = preproc_pollution(pollution_df)

    load_save_geojson()

    merge_covid_pollution(covid_df, pollution_df)
