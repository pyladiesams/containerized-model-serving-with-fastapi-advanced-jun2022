import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

import spotipy as sp

_MAX_NUMBERS = 50


class MusicModel:
    def __init__(self):

        redirect_uri = "http://localhost:9000"
        scope = "playlist-modify-public user-library-read user-follow-read \
            user-top-read playlist-read-private user-read-recently-played"

        self.selected_features = [
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
        ]

        self.spt = self.authenticate(redirect_uri, scope)

    def authenticate(self, redirect_uri, scope):

        try:
            self.spt = sp.Spotify(
                auth_manager=sp.oauth2.SpotifyOAuth(
                    redirect_uri=redirect_uri, scope=scope, open_browser=False
                )
            )
            self.read_user_tracks(term="short_term")
            print("Successfully connected to the Spotify API.")
            return self.spt

        except sp.oauth2.SpotifyOauthError:
            print("Not able to authenticate, continue with default data.")

        return None

    def read_user_tracks(self, term: str):

        file = f"data/user_tracks_{term}.csv"

        if os.path.isfile(file):
            return pd.read_csv(file)

        if self.spt:
            user_tracks = self.get_top_user_tracks(term)
            user_tracks.to_csv(file)
            return user_tracks

        return pd.read_csv("./data/user_tracks.csv")

    def read_tracks(self, playlist_id):

        file = f"data/tracks_{playlist_id}.csv"

        if os.path.isfile(file):
            return pd.read_csv(file)

        if self.spt:
            tracks = self.get_tracks(playlist_id)
            tracks.to_csv(file)
            return tracks

        return pd.read_csv("./data/tracks.csv")

    def _get_features(self, track_ids):

        features = self.spt.audio_features(track_ids)

        return pd.DataFrame(features)[self.selected_features]

    def _parse_artist_names(self, artists):
        names = []
        for artist in artists:
            names.append(artist["name"])

        return ", ".join(names)

    def get_tracks(self, playlist_id: str = "4hOKQuZbraPDIfaGbM3lKI"):

        playlist = self.spt.playlist(playlist_id)

        tracks = pd.DataFrame(
            [
                {
                    "id": i["track"]["id"],
                    "name": i["track"]["name"],
                    "artists": self._parse_artist_names(i["track"]["artists"]),
                }
                for i in playlist["tracks"]["items"]
            ]
        )

        return (
            self._get_features(tracks["id"])
            .assign(name=tracks["name"])
            .assign(artists=tracks["artists"])
        )

    def get_top_user_tracks(self, term: str):

        top_user_tracks = self.spt.current_user_top_tracks(
            limit=_MAX_NUMBERS, time_range=term
        )["items"]

        tracks = pd.DataFrame(
            [
                {
                    "id": i["id"],
                    "name": i["name"],
                    "artists": self._parse_artist_names(i["artists"]),
                }
                for i in top_user_tracks
            ],
        )

        return (
            self._get_features(tracks["id"])
            .assign(name=tracks["name"])
            .assign(artists=tracks["artists"])
        )

    def fit_model(self, X):
        class NN(NearestNeighbors):
            def predict(self, X):
                return self.kneighbors(X)

        pipeline = Pipeline([("scaler", MinMaxScaler()), ("nn", NN(n_neighbors=1))])
        return pipeline.fit(X[self.selected_features])

    def predict(self, nn, user_tracks, tracks):

        distance, indices = nn.predict(user_tracks[self.selected_features])
        df = pd.DataFrame(
            {"distance": [x[0] for x in distance], "track_id": [x[0] for x in indices]}
        )
        prediction = df.sort_values("distance").reset_index()

        top_match = prediction.iloc[0]

        return {
            "favourite_song": f"{' - '.join(user_tracks.iloc[int(top_match['index'])][['name', 'artists']].values)}",
            "most_similar_song": f"{' - '.join(tracks.iloc[int(top_match['track_id'])][['name', 'artists']].values)}",
        }


if __name__ == "__main__":
    music_model = MusicModel()
    print(
        music_model.read_user_tracks("short_term")[["name", "artists"]].iloc[0].values
    )
