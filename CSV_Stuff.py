import pandas as pd
import numpy as np
import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation

fields = ["title","id","vote_average","vote_count","release_date","revenue","budget","runtime","genres","cast","director","writers","producers","imdb_rating","imdb_votes"] # Put the info you want here

df = pd.read_csv(r"Data\TMDB_all_movies.csv", skipinitialspace=True, usecols=fields)


#Data cleaning START
df.set_index("id", inplace=True) #Sets the index to be the movies ID

for i in ["vote_average","vote_count","revenue","budget","imdb_rating","imdb_votes"]:
    df[i].fillna(0,inplace=True)
    #This replaces NAN values with in the list to 0

df["release_date"] = pd.to_datetime(df["release_date"])
df.drop_duplicates(inplace = True)

df.dropna(inplace=True)
#Data cleaning END

sns.boxplot(x=df["budget"])


#These colums have numeric datatypes: vote_average, vote_count, revenue, runtime, budget, genres, imdb_rating, imdb_votes

"""datatype list:
    title                   object
    vote_average           float64
    vote_count             float64
    release_date    datetime64[ns]
    revenue                float64
    runtime                float64
    budget                 float64
    genres                  object
    cast                    object
    director                object
    writers                 object
    producers               object
    imdb_rating            float64
    imdb_votes             float64
"""

# print(df.describe().apply(lambda x: x.apply('{0:.5f}'.format))) # Gives some data summary and supresses the "forced" sci notation with lambda magic