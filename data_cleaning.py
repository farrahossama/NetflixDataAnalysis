import pandas as pd
import numpy as np


## Reading the CSV file
df=pd.read_csv('netflix_titles.csv')


#Inspecting the file to know what needs cleaning
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum())

## Dropping duplicates
df.drop_duplicates(inplace=True)

# Filling null values for large data and dropping rows for small null data
df['director'].fillna("Not Specified",inplace=True)
df['cast'].fillna("Not Specified",inplace=True)
df['country'].fillna("Not Specified",inplace=True)
df.dropna(subset=['date_added', 'rating','duration'], inplace=True)

# Converting date_added from string to date
df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'])

# Splitting movies from TV shows using seasons and minutes
df[['duration_int', 'duration_type']] = df['duration'].str.extract(r'(\d+)\s*(\w+)')
df['duration_int'] = pd.to_numeric(df['duration_int'])


# converting show_id to integer after removing the s 
df['show_id'] = df['show_id'].str.replace('s', '', regex=False).astype(int)

# inspecting the cleaned data
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.isnull().sum())

# making the countries table and the unique countries table
df['country'] = df['country'].str.split(',\s*')  
df_country = df[['show_id', 'country']].explode('country')

unique_country = pd.DataFrame(df_country['country'].unique(), columns=['country'])
unique_country['country_id'] = range(1, len(unique_country) + 1)
df_country = df_country.merge(unique_country, on='country')

# making the genres table and the unique genres table
df['listed_in'] = df['listed_in'].str.split(',\s*')  
df_genres = df[['show_id', 'listed_in']].explode('listed_in').rename(columns={'listed_in': 'genre'})

unique_genres = pd.DataFrame(df_genres['genre'].unique(), columns=['genre'])
unique_genres['genre_id'] = range(1, len(unique_genres) + 1)
df_genres = df_genres.merge(unique_genres, on='genre')

# making the director table and the unique directors table
df['director'] = df['director'].str.split(',\s*')  
df_director = df[['show_id', 'director']].explode('director')

unique_director = pd.DataFrame(df_director['director'].unique(), columns=['director'])
unique_director['director_id'] = range(1, len(unique_director) + 1)
df_director = df_director.merge(unique_director, on='director')


# dropping the not needed columns for the database
df=df.drop(columns=['director', 'cast','country','listed_in','description','duration'])
df_country=df_country.drop(columns=['country'])
df_director=df_director.drop(columns=['director'])
df_genres=df_genres.drop(columns=['genre'])


# exporting to csv
df.to_csv('netflix_cleaned.csv', index=False)
df_genres.to_csv('netflix_genres.csv', index=False)
unique_genres.to_csv('netflix_genres_unique.csv', index=False)
df_country.to_csv('netflix_country.csv', index=False)
unique_country.to_csv('netflix_country_unique.csv', index=False)
df_director.to_csv('netflix_director.csv', index=False)
unique_director.to_csv('netflix_director_unique.csv', index=False)
