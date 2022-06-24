from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from src.spotify import read_tracks, read_user_tracks, fit_model, predict

description = """
Spotify: insights in your music taste

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
        "description": "Predicts which song from the given playlist is most similar to one of your top songs.",
    },
]


app = FastAPI(debug=True, description=description, openapi_tags=tags_metadata)


@app.get("/")
def root():
    return {"message": "Welcome to the spotify clustering app! Please check the terminal whether you need to login."}


@app.get(
    "/most_listened/1.1.0",
    tags=["most_listened"],
    summary="Shows your 50 most listened songs",
    # response_model=List[PredOut],
)
def get_most_listened_songs(term: str = Query("short_term")):
    """

    """
    user_tracks = read_user_tracks(term)

    return HTMLResponse(content=user_tracks[['name', 'artists']].to_html(), status_code=200)


@app.get(
    "/show_playlist/1.1.0",
    tags=["show_playlist"],
    summary="Shows songs for the given playlist",
    # response_model=List[PredOut],
)
def get_most_listened_songs(playlist_id: str,):
    """

    """
    tracks = read_tracks(playlist_id)

    return HTMLResponse(content=tracks[['name', 'artists']].to_html(), status_code=200)


@app.get(
    "/predict/1.1.0",
    tags=["predict"],
    summary="Shows a prediction based on your music and given playlist",
    # response_model=str,
)
def get_prediction(term: str = Query("short_term"), playlist_id: str = "37i9dQZF1DXb5BKLTO7ULa"):

    tracks=read_tracks(playlist_id)
    user_tracks=read_user_tracks(term)

    nn = fit_model(tracks)

    return predict(nn, user_tracks, tracks)
