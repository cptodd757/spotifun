import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('charlie_liked_songs_verbose.csv')
continuous = ['acousticness','danceability','energy','instrumentalness',
                  'liveness','loudness','speechiness','valence','tempo']

for col in continuous:
    plt.figure()
    plt.hist(df[col])
    plt.xlabel(col)
    plt.ylabel('count')
plt.show()