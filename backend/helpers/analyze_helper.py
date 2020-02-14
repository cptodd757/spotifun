import config

import pandas as pd 

def analyze_helper(data, df):
    genres_df = pd.DataFrame()
    genres = []
    genres_freqs = []

    #create one-hotted columns and also calculate frequencies
    def one_hot_genres(row):
        for genre in row['genres'].split(', '):
            if genre not in df.columns.values:
                print(genre)
                df[genre] = df['genres'].str.contains(genre)
                #genres_df = genres_df.append({"genre":genre,"proportion":df[genre].mean()})
                genres.append(genre)
                genres_freqs.append(df[genre].mean())
                

        #return row
    df.apply(one_hot_genres,axis=1)
    for i in range(len(genres)):
        genres_df = genres_df.append({"genre":genres[i],"freq":genres_freqs[i]}, ignore_index=True)
        print(genres_df)
    #df.to_csv('one hot genres.csv')
    genres_df = genres_df.sort_values(by='freq',ascending=False)
    print(genres,genres_freqs)
    print(genres_df)

    genres_df.to_csv('charlie genre proportions.csv')

    continuous = ['acousticness','danceability','energy','instrumentalness',
                  'liveness','loudness','speechiness','valence','tempo']

    for col in continuous:
        df[col].hist()
    df.plot()

    #parallel arrays
    freqs = []