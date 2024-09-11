from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from dataclasses import dataclass
import dataclasses
import spotipy
import os
import json

load_dotenv()

config = {
    "spotify": {
        "id": os.environ.get("SPOTIFY_CLIENT_ID"),
        "secret": os.environ.get("SPOTIFY_CLIENT_SECRET"),
    },
}

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=config["spotify"]["id"],
        client_secret=config["spotify"]["secret"],
    )
)


@dataclass
class Artist:
    name: str
    id: str


@dataclass
class Image:
    url: str
    height: int
    width: int


@dataclass
class Album:
    name: str
    id: str
    artists: list[Artist]
    images: list[Image]


@dataclass
class Song:
    name: str
    id: str
    track_number: int
    album: Album
    artists: list[Artist]


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def serialize_artist(artist) -> Artist:
    return Artist(artist["name"], artist["id"])


def serialize_image(image) -> Image:
    return Image(image["url"], image["height"], image["width"])


def serialize_album(album) -> Album:
    return Album(
        album["name"],
        album["id"],
        list(map(lambda artist: serialize_artist(artist), album["artists"])),
        list(map(lambda image: serialize_image(image), album["images"])),
    )


def serialize_track(track):
    return Song(
        track["name"],
        track["id"],
        track["track_number"],
        serialize_album(track["album"]),
        list(map(lambda artist: serialize_artist(artist), track["artists"])),
    )


def spotify_search(q: str) -> list[Song]:
    results = sp.search(q, limit=6)
    if not results:
        return []

    songs = []
    track_data = results["tracks"]["items"]
    for track in track_data:
        songs.append(serialize_track(track))

    return songs
    # print(json.dumps(songs, indent=4, cls=EnhancedJSONEncoder))
