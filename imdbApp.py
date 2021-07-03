# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 23:00:59 2021

@author: Bogdan Tudose
"""

#%% Import Packages
import pandas as pd
import streamlit as st
import os
os.environ['TZ'] = 'UTC' 

#%% Import File
@st.cache
def grabData():
    df = pd.read_csv("IMDb movies.csv")
    df['actors'] = df['actors'].fillna("n.a.")
    df['country'] = df['country'].fillna("n.a.")
    df = df[df['year'] != "TV Movie 2019"]
    df['date_published'] = pd.to_datetime(df['date_published'])
    df['Year'] = df['date_published'].dt.year
    return df

df = grabData()

#%% Sidebar controls
filterDF = df.copy()

titles = sorted(filterDF['title'].unique())
titleSearch = st.sidebar.multiselect('What movie are you looking for?',titles)
genres = sorted(filterDF['genre'].unique())
genreSearch = st.sidebar.multiselect('What genre are you looking for?',genres)
countries = sorted(filterDF['country'].unique())
countrySearch = st.sidebar.multiselect('What country are you looking for?',countries)

recentMovies = df[df['Year']>2010]
allActors = set(", ".join(recentMovies['actors'].unique()).split(","))
allActors = set(x.strip() for x in allActors)
allActors = list(allActors)
allActors.sort()

actorsPicks = st.sidebar.multiselect('First actor',allActors)
actorSearch = "|".join(actorsPicks)
actorsPicks2 = st.sidebar.multiselect('Second actor',allActors)
actorSearch2 = "|".join(actorsPicks2)


minDur, maxDur= min(df['duration']), max(df['duration'])
d0, d1= st.sidebar.slider("Please select the required duration",minDur,maxDur,(minDur,maxDur))



#Date Filters
minYear, maxYear = min(filterDF['Year']), max(filterDF['Year'])
y0, y1= st.sidebar.slider("Please select the years to analyze",minYear,maxYear,(2000,2019))


#Applying Filters
filterMap = {"title":titleSearch, "genre":genreSearch,"country":countrySearch}
for colName, filterVals in filterMap.items():
    if len(filterVals)>0: 
        filterDF = filterDF[filterDF[colName].isin(filterVals)]

filterDF = filterDF[filterDF['actors'].str.contains(actorSearch, regex=True)]
filterDF = filterDF[filterDF['actors'].str.contains(actorSearch2, regex=True)]
filterDF = filterDF[(filterDF['duration'] >= d0) & (filterDF['duration'] <= d1)]
filterDF = filterDF[(filterDF['Year'] >= y0) & (filterDF['Year'] <= y1)]

st.title("Filter results")
st.write(filterDF)

