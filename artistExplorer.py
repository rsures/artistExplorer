import numpy as np 
import pandas as pd
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import display

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

#authenicate spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

#query about which artists that users like to analyze
music_artists = []
while True:
    name = input("Find which artist you would like to explore. To quit search and see exploration results please enter 'QUIT'. ")
    if name.upper() == 'QUIT':
        break;
    else:
        search_result = sp.search (q=name, type='artist')
        artists= search_result['artists']['items']
        if len (artists) == 0:
            response = input("search returned no results, please try again: ")
            continue;
        else:
            correct_artist = input(f"Did you mean: {artists[0]['name']}? Y or N: ")
            while correct_artist.upper() not in ['Y', 'N']:
                correct_artist = input(f"Did you mean: {artists[0]['name']}? Y or N")
            
            if (correct_artist.upper () == 'Y'):
                music_artists.append (artists[0]['name'])
            else:
                continue;

#get basic user info
def get_artist_info (artists):
    artist_info = {}
    for i, artist in enumerate (music_artists, start=1):
        artist_result = sp.search(q=artist, type="artist")
        info = artist_result['artists']['items'][0]
        case = {
            "name": info ['name'],
            "followers": info['followers']['total'],
            "genres": info['genres'],
            "id": info['id'],
            "popularity": info['popularity'],
            "type": info['type']
        }
        artist_info[f"aritst {i}"] = case
    return artist_info

artist_info = get_artist_info(artists)

#display user info
def display_artist_info (artist_info):
    for i, artist in enumerate(artist_info.keys()):
        print(
            artist,
            "\nName: ", artist_info[artist]['name'],
            "\nFollowers: ", artist_info[artist]['followers'],
            "\nGenre(s): ",artist_info[artist]['genres'],
            "\nPopularity: ",artist_info[artist]['popularity'],
            "\nType: ",artist_info[artist]['type'],
            "\n"
        )


#get all album details
def get_album_info (artist_info):
    for artist in artist_info.keys():
        album_reterival = sp.artist_albums(artist_info[artist]['id'], limit=50)
        albums= album_reterival['items']
        album_detail = [album['name'] for album in albums if len(sp.album_tracks(album['id'])['items']) > 1]
        # album_detail = [album for album in album_detail if ("Explicit Deluxe")]
        album_detail = list(dict.fromkeys(album_detail))
        artist_info[artist]['albums'] = album_detail
        artist_info[artist]['album count'] = len (album_detail)
    return artist_info

artist_info = get_album_info(artist_info)

#get top songs
def get_top_songs (artist_info):
    for artist in artist_info.keys():
        songs_result = sp.artist_top_tracks(artist_info[artist]['id'])
        songs = songs_result['tracks']
        top_songs = [track['name'] for track in songs]
        top_songs_id = [track['id'] for track in songs]
        artist_info[artist]['top tracks'] = dict(zip(top_songs, top_songs_id))
        
    return (artist_info)

#create data drame for artist
artist_info = get_top_songs(artist_info)

artist_df = pd.DataFrame.from_dict(artist_info)
display_artist_info(artist_info)

#create song data frame
def create_song_df (artist_df):
    artists = []
    songs = []
    ids = []
    for col in artist_df.columns: 
        artist_song = [song for song in artist_df[col]['top tracks'].keys()]
        songs = songs + artist_song
        artist_name = [artist_df[col]['name'] for i in artist_df[col]['top tracks'].items()]
        artists = artists + artist_name
        id = [song for song in artist_df[col]['top tracks'].values()]
        ids += id
    
    track_df = pd.DataFrame(data ={"Artist": artists, "Tracks": songs, "Track ID": ids})
    
    return track_df

songs_df = create_song_df (artist_df)

#song analysis
def song_features (songs_df):
    songs = list(songs_df['Track ID'])
    danceability = []
    energy = []
    #key = []
    loudness = []
    #mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    id = []
    
    for song in songs:
        features = sp.audio_features(song)[0]
        danceability.append(features['danceability']),
        energy.append(features['energy']),
        #key.append(features['key']),
        loudness.append(features['loudness']),
        speechiness.append(features['speechiness']),
        acousticness.append(features['acousticness']),
        instrumentalness.append(features['instrumentalness']),
        liveness.append(features['liveness']),
        valence.append(features['valence']),
        tempo.append(features['tempo']),
        id.append(features['id'])
        
    feature_df = pd.DataFrame (
            data = {
                'danceability' : danceability,
                'energy': energy,
                'loudness': loudness,
                'speechiness': speechiness,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness,
                'liveness': liveness,
                'valence': valence,
                'tempo': tempo,
                'id': id
            }
    )
    
    return feature_df

feature_df = song_features(songs_df)

#combine feature information to song df
songs_df = songs_df.merge(feature_df, how='inner', left_on='Track ID', right_on='id')
songs_df.drop(columns=['id'], axis=1, inplace=True)

#apply min-max normalizing for tempo and loudness to reshape feature between 0 and 1
def min_max_norm (values):
    norm_values = []
    min = values.min()
    max = values.max()
    for i in values:
        normalize = ((i - min)/(max-min))
        norm_values.append(normalize)
    return norm_values

songs_df['loudness'] = min_max_norm(songs_df.loudness)
songs_df['tempo'] = min_max_norm(songs_df.tempo)

#create avg of track feature info
overall_song_feature = songs_df.groupby('Artist').mean(numeric_only=True)
