import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

import spotipy as sp

redirect_uri='http://localhost:9000'
scope = 'playlist-modify-public user-library-read user-follow-read user-top-read playlist-read-private user-read-recently-played'

spt = sp.Spotify(auth_manager=sp.oauth2.SpotifyOAuth(redirect_uri=redirect_uri, scope=scope, open_browser=False))

selected_features = ['danceability', 'energy', 'loudness', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

def main():
    tracks = get_tracks()
    nn = fit_model(tracks[selected_features])

    user_tracks = get_top_user_tracks()
    prediction = predict(nn, user_tracks)

    print(f"Based on your favourite song '{', '.join(user_tracks.iloc[prediction['index'][0]][['name', 'artists']].values)}' "
    f"the song with the most similar audio features is '{', '.join(tracks.iloc[prediction['closest'][0]][['name', 'artists']].values)}'")


def read_user_tracks(term: str):

    file = f'data/user_tracks_{term}.csv'

    if os.path.isfile(file):
        return pd.read_csv(file)

    if os.environ.get('SPOTIPY_CLIENT_ID') and os.environ.get('SPOTIPY_CLIENT_SECRET'):

        user_tracks=get_top_user_tracks(term)
        user_tracks.to_csv(file)
        return user_tracks

    return pd.read_csv('./data/user_tracks.csv')


def read_tracks(playlist_id):

    file = f'data/tracks_{playlist_id}.csv'

    if os.path.isfile(file):
        return pd.read_csv(file)

    if os.environ.get('SPOTIPY_CLIENT_ID') and os.environ.get('SPOTIPY_CLIENT_SECRET'):
        tracks=get_tracks(playlist_id)
        tracks.to_csv(file)
        return tracks

    return pd.read_csv('./data/tracks.csv')

        
def _get_features(track_ids):
    
    features = spt.audio_features(track_ids)

    return pd.DataFrame(features)[selected_features]

        
def _parse_artist_names(artists):
    names = []
    for artist in artists:
        names.append(artist['name'])

    return ", ".join(names)


def get_tracks(playlist_id: str="4hOKQuZbraPDIfaGbM3lKI"):
    playlist = spt.playlist(playlist_id)

    tracks = pd.DataFrame([{'id': i['track']['id'], 
                            'name': i['track']['name'],
                            'artists': _parse_artist_names(i['track']['artists'])
                           } for i in playlist['tracks']['items']])
                
    return _get_features(tracks['id']).assign(name=tracks['name']).assign(artists=tracks['artists'])


def get_top_user_tracks(term: str):
    top_user_tracks = spt.current_user_top_tracks(limit=50, time_range=term)['items']

    tracks = pd.DataFrame([{'id': i['id'], 
                            'name': i['name'],
                            'artists': _parse_artist_names(i['artists'])} 
                           for i in top_user_tracks],
                            )
    
    return _get_features(tracks['id']).assign(name=tracks['name']).assign(artists=tracks['artists'])


def fit_model(X):

    class NN(NearestNeighbors):
        def predict(self, X):
            return self.kneighbors(X)
    
    pipeline=Pipeline([('scaler', MinMaxScaler()), 
                        ('nn', NN(n_neighbors=1))])
    return pipeline.fit(X[selected_features])


def predict(nn, user_tracks, tracks):

    distance, indices = nn.predict(user_tracks[selected_features])
    df = pd.DataFrame({'distance': [x[0] for x in distance], 'track_id': [x[0] for x in indices]})
    prediction = df.sort_values('distance').reset_index()

    top_match = prediction.iloc[0]

    return(
        f"Based on your favourite song "
        f"'{', '.join(user_tracks.iloc[int(top_match['index'])][['name', 'artists']].values)}' "
        f"the song with the most similar audio features is "
        f"'{', '.join(tracks.iloc[int(top_match['track_id'])][['name', 'artists']].values)}'")
