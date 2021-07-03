# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 19:58:41 2021

@author: Bogdan Tudose
"""
#%% Import Packages
import pandas as pd

#%%
def grabData():
    df = pd.read_csv("imdb/IMDb movies.csv")
    df['actors'] = df['actors'].fillna("n.a.")
    df['country'] = df['country'].fillna("n.a.")
    df = df[df['year'] != "TV Movie 2019"]
    df['date_published'] = pd.to_datetime(df['date_published'])
    df['Year'] = df['date_published'].dt.year
    return df
#%%
df = grabData()
df.columns
df.info()

df2015 = df[df['Year']== 2015]
df2015.to_excel('IMDB/imdb 2015.xlsx')

prod_cos = df2015['production_company'].value_counts()

