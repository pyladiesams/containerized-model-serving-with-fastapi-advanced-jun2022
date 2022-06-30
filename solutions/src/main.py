from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse

from src.class_definitions import Term, Song, PredOut
from src.spotify import MusicModel

from spotipy.client import SpotifyException

from typing import List

description = """
Spotify: receive Spotify songs based on your very own personal music taste

"""

tags_metadata = [
    {
        "name": "most_listened",
        "description": "Shows your 50 most listened songs for the given term.",
    },
    {
        "name": "show_playlist",
        "description": "Shows the songs in the given playlist.",
    },
    {
        "name": "predict",
        "description": "Predicts which song from the given playlist is \
            most similar to one of your top songs.",
    },
]


music_model = MusicModel()

app = FastAPI(description=description, openapi_tags=tags_metadata)


@app.get("/")
def root():

    return {"message": f"Welcome to the Spotify Music app! "
                       f"{music_model.auth_msg}"}


@app.get(
    "/most_listened",
    tags=["most_listened"],
    summary="Shows your most listened songs",
    response_model=List[Song],
)
def get_most_listened_songs(term: Term = Query("short_term"), limit: int = 50, debug: bool = False):
    """ """
    user_tracks = music_model.read_user_tracks(term)[:limit]

    if debug:
        return HTMLResponse(
            content=user_tracks[["name", "artists"]].to_html(), status_code=200
        )
    return user_tracks[["name", "artists"]].to_dict(orient="records")


@app.get(
    "/show_playlist",
    tags=["show_playlist"],
    summary="Shows songs for the given playlist",
    response_model=List[Song],
)
def get_songs_from_playlist(
    playlist_id: str = "37i9dQZF1DXb5BKLTO7ULa",
    debug: bool = False,
):
    """ """
    try:
        tracks = music_model.read_tracks(playlist_id)
    except SpotifyException:
        raise HTTPException(status_code=404, detail="Playlist id not found")

    if debug:
        return HTMLResponse(
            content=tracks[["name", "artists"]].to_html(), status_code=200
        )

    return tracks[["name", "artists"]].to_dict(orient="records")


@app.get(
    "/predict",
    tags=["predict"],
    summary="Shows a prediction based on your music and given playlist",
    response_model=PredOut,
)
def get_prediction(
    term: Term = Query("short_term"),
    playlist_id: str = "37i9dQZF1DXb5BKLTO7ULa",
):

    return music_model.predict(term=term, playlist_id=playlist_id)
