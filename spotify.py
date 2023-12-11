import requests
import spotipy
import os


class Spotify:
    def __init__(self):
        self.ENDPOINT = "https://api.spotify.com/v1/users/" + os.environ["SPOTIFY_USER"]
        self.PL_ENDPOINT = self.ENDPOINT + "/playlists"
        self.SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
        spotify = spotipy.oauth2.SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                   client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                                   redirect_uri="http://example.com",
                                                   scope="playlist-modify-private")

        self.access_token = spotify.get_access_token()
        self.token = {"Authorization": f"Bearer {self.access_token['access_token']}"}

    def create_playlist(self, playlist_name):
        # Create a playlist

        params = {
            "name": playlist_name,
            "public": False
            }

        response = requests.post(self.PL_ENDPOINT, headers=self.token, json=params)
        response.raise_for_status()
        playlist_id = response.json()["id"]

        return playlist_id

    def get_playlists(self):
        # data = {
        #     "limit": "40"
        # }
        response = requests.get(self.PL_ENDPOINT, headers=self.token)
        #response.raise_for_status()
        playlist_data = response.json()["items"]

        playlist_names = []
        for playlist in playlist_data:
            playlist_names.append(playlist["name"])

        print(playlist_names)
        print(len(playlist_names))

    def search_items(self, track, artist, year):
        params = {
            "q": f"{track} {year} {artist}",
            "type": "track",
            "limit": 1
        }

        response = requests.get(self.SEARCH_ENDPOINT, headers=self.token, params=params)
        response.raise_for_status()

        if response.json()["tracks"]["total"] != 0:
            song_uri = response.json()["tracks"]["items"][0]["uri"]
            return song_uri
        else:
            print(f"track:{track} year:{year} artist:{artist} was not found")
            return None

    def add_items_to_playlist(self, track_uri, playlist_id):
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        data = {
            "uris": track_uri
        }
        response = requests.post(url=endpoint, headers=self.token, params=data)
        response.raise_for_status()
        #print(response.text)
