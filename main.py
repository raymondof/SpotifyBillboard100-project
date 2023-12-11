from spotify import Spotify
from billboard import BillBoard

spotify = Spotify()
billboard = BillBoard()

#TODO: get old playlists to see if the playlist with the name already exists
#spotify.get_playlists()

# Ask user for date to search for most popular songs of the day
time = input("What period of time you would like to travel to? Input in YYYY-MM-DD format: ")
#time = "2015-06-24"

# Extract the year from the provided time string
year = int(time.split("-")[0])
# Calculate the playlist year range by subtracting 5 from the extracted year and adding 5 to it
playlist_year = f"{year - 5}-{year + 5}"

# Returns dictionary "track_name": "artist_name"
track_list = billboard.get_songs(time)

# Create Spotify playlist with given name and time
playlist_name = f"{time} Billboard 100"
playlist_id = spotify.create_playlist(playlist_name)

# Iterate song and artist in the track_list. "Search_items" returns none if track is not found.
# If None is returned, will search again with "track:", "artist:" and "year:" keywords.
for song, artist in track_list.items():
    track_uri = spotify.search_items(track=song, artist=artist, year=playlist_year)
    if track_uri is None:
        track_uri = spotify.search_items(track=f"track:{song}", artist=f"artist:{artist}", year=f"year:{playlist_year}")
        if track_uri is not None:
            spotify.add_items_to_playlist(track_uri, playlist_id)
    else:
        spotify.add_items_to_playlist(track_uri, playlist_id)
