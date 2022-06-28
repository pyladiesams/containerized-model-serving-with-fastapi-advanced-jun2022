import pandas as pd
import os

from typing import Dict, List

from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

import spotipy as sp


class MusicModel:
    def __init__(self):

        self.redirect_uri = "http://localhost:9000"
        self.scope = "playlist-modify-public user-library-read user-follow-read \
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
        self.auth_msg = self.authenticate()

    def authenticate(self) -> str:
        """ Authenticates the user using the client_id and client_secret
        in the environment variables.

        :return: Message whether authentication was successful.
        """
        try:
            self.spt = sp.Spotify(
                auth_manager=sp.oauth2.SpotifyOAuth(
                    redirect_uri=self.redirect_uri, scope=self.scope, open_browser=False
                )
            )
            self.read_user_tracks(term="short_term")

            return "Successfully connected to the Spotify API."

        except sp.oauth2.SpotifyOauthError:
            self.spt = None

            return "Not able to authenticate, continue with default data."


    def read_user_tracks(self, term: str) -> pd.DataFrame:
        """ Returns the top tracks of a user when the user is authenticated.
        Otherwise returns the default user_tracks from the data folder.


        :param term: Top user tracks based on the 'short_term', 'medium_term', 'long_term'
        :return: Dataframe containing top songs.
        """
        file = f"data/user_tracks_{term}.csv"

        if os.path.isfile(file):
            return pd.read_csv(file)

        if self.spt:
            user_tracks = self.get_top_user_tracks(term)
            user_tracks.to_csv(file)
            return user_tracks

        return pd.read_csv("./data/user_tracks.csv")

    def read_tracks(self, playlist_id: str) -> pd.DataFrame:
        """ Returns the tracks of the given playlist if the user is authenticated.
        Otherwise returns the default tracks from the data folder.

        :param playlist_id: Spotify playlist id.
        :return: Dataframe containing tracks from a given playlist.
        """
        file = f"data/tracks_{playlist_id}.csv"

        if os.path.isfile(file):
            return pd.read_csv(file)

        if self.spt:
            tracks = self.get_tracks(playlist_id)
            tracks.to_csv(file)
            return tracks

        return pd.read_csv("./data/tracks.csv")

    def _get_features(self, track_ids: List[str]) -> pd.DataFrame:
        """ Returns the audio features of a given list of tracks.

        :param track_ids: List of Spotify track id's.
        :return: Dataframe containing audio features.
        """
        features = self.spt.audio_features(track_ids)

        return pd.DataFrame(features)[self.selected_features]

    def _parse_artist_names(self, artists):
        """ Parses the artists names.

        :param artists: List of artist information
        :return: Artist names as string, separated by ', '.
        """
        names = []
        for artist in artists:
            names.append(artist["name"])

        return ", ".join(names)

    def get_tracks(self, playlist_id: str = "4hOKQuZbraPDIfaGbM3lKI") -> pd.DataFrame:
        """ Returns the tracks of a given playlist.

        :param playlist_id: Spotify playlist id.
        :return: Dataframe containing songs plus audio features.
        """
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
        """ Returns the top user tracks.

        :param term: Top user tracks based on the 'short_term', 'medium_term', 'long_term'
        :return: Dataframe containing top songs plus audio features.
        """
        top_user_tracks = self.spt.current_user_top_tracks(time_range=term
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

    def fit_model(self, X: pd.DataFrame) -> Pipeline:
        """ Fits a nearest neighbour model on the given dataset, using the
        selected features.

        :param X:
        :return: Fitted model.
        """
        class NN(NearestNeighbors):
            def predict(self, X):
                return self.kneighbors(X)

        pipeline = Pipeline([("scaler", MinMaxScaler()), ("nn", NN(n_neighbors=1))])
        return pipeline.fit(X[self.selected_features])

    def predict(self, playlist_id: str, term: str) -> Dict:
        """ Returns the most similar song from the given playlist given the top user songs.

        :param playlist_id: Spotify playlist id.
        :param term: Top user tracks based on the 'short_term', 'medium_term', 'long_term
        :return: Dictionary with the most similar song from the top user song and playlist.
        """
        tracks = self.read_tracks(playlist_id)
        user_tracks = self.read_user_tracks(term)

        nn = self.fit_model(tracks)

        distance, indices = nn.predict(user_tracks[self.selected_features])
        df = pd.DataFrame(
            {"distance": [x[0] for x in distance], "track_id": [x[0] for x in indices]}
        )
        prediction = df.sort_values("distance").reset_index()

        top_match = prediction.iloc[0]

        return {
            "favourite_song": f"{' - '.join(user_tracks.iloc[int(top_match['index'])][['name', 'artists']].values)}",
            "most_similar_song": f"{' - '.join(tracks.iloc[int(top_match['track_id'])][['name', 'artists']].values)}",
            "distance": top_match['distance']
        }


if __name__ == "__main__":
    music_model = MusicModel()

    print(
        music_model.read_user_tracks("short_term")[["name", "artists"]].iloc[0].values
    )
