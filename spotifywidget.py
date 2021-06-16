import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import json
# %config InlineBackend.figure_format ='retina'
# import spotipy
# import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy import oauth2
import random
from functools import reduce
import requests
# from spotify.spotify_creds import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER, SPOTIFY_REDIRECT_URI
import streamlit as st
import streamlit.components.v1 as components
import datetime as dt

##Functions
def select_playlist(feeling):
    happiness = 'https://open.spotify.com/embed/playlist/556ICk4gRzDknRfWGeQ3x1'
    sadness = 'https://open.spotify.com/embed/playlist/0dRxDrR1PfZMlVbfnuBRbR'
    anger = 'https://open.spotify.com/embed/playlist/7FjP7MbRgFYFdv5avuhiBI'
    fear = 'https://open.spotify.com/embed/playlist/6EF56fuiUgN2GOMVZIiXpq'
    love = 'https://open.spotify.com/embed/playlist/73KuPUAtOecLDAetRn80TW'
    neutral = 'https://open.spotify.com/embed/playlist/5pSdjjPHbXpbqFJGf31Ksn'
    d= {'happy':happiness, 'sadness':sadness, 'love':love, 
        'anger':anger, 'neutral':neutral, 'fear': fear}
    mood = d[feeling]
    return components.html(
        f"""
        <iframe src={mood} width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
        """,
        height=800,
    )

# # ID and password
# cid = SPOTIFY_CLIENT_ID
# secret = SPOTIFY_CLIENT_SECRET
# username = SPOTIFY_USER
# uri = SPOTIFY_REDIRECT_URI
# scope = 'user-read-private user-read-email playlist-modify-public user-read-playback-state user-read-currently-playing user-modify-playback-state'
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
#                                                client_secret=secret,
#                                                redirect_uri=uri,
#                                                scope=scope))
def spotify_authentification():
    """
    Api authentification using requests
    """
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': cid,
        'client_secret': secret,
    })
    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    return headers

def select_playlist(feeling):
        happiness = 'https://open.spotify.com/embed/playlist/556ICk4gRzDknRfWGeQ3x1'
        sadness = 'https://open.spotify.com/embed/playlist/0dRxDrR1PfZMlVbfnuBRbR'
        anger = 'https://open.spotify.com/embed/playlist/7FjP7MbRgFYFdv5avuhiBI'
        fear = 'https://open.spotify.com/embed/playlist/6EF56fuiUgN2GOMVZIiXpq'
        love = 'https://open.spotify.com/embed/playlist/73KuPUAtOecLDAetRn80TW'
        neutral = 'https://open.spotify.com/embed/playlist/5pSdjjPHbXpbqFJGf31Ksn'

        d= {'happy':happiness, 'sadness':sadness, 'love':love, 
            'anger':anger, 'neutral':neutral, 'fear': fear}

        mood = d[feeling]

        return components.html(
            f"""
            <iframe src={mood} width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            """,
            height=800,
        )


def artist_track_features(artist='Bicep'):
    """
    This function will provide us with a dataframe with all sounds of an artist 
    and their underlying features.
    Inputs :
    artist = <Name of the artist>
    Outputs :
    > Dataframe containing the sounds of an artist
    """
    # Fetch artist tracks
    d = {}
    track_results = sp.search(q=artist, type='track',limit=50)
    for i, t in enumerate(track_results['tracks']['items']):
        track_id = t['id']
        if track_id not in d:
            d[track_id] = {'artist_feature' : t['artists'][0]['name'],
                           'query' : artist,
                           'track_name' : t['name'],
                           'popularity': t['popularity']}    
            d[track_id].update(sp.audio_features(d.keys())[i])
            # add genres
            headers = spotify_authentification()
            BASE_URL = 'https://api.spotify.com/v1/'
            re = requests.get(BASE_URL + 'tracks/' + track_id, headers=headers).json()
            if re != None :
                layer = requests.get(re['artists'][0]['href'], headers=headers).json()
                if 'genres' in layer.keys():
                    d[track_id].update({'genres':layer['genres']})
                else :
                    d[track_id].update({'genres':'None'})
    return pd.DataFrame.from_dict(d, orient='index')

# Playlist class
class Playlists:
    
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        
    def get_artist_tracks(self):
        headers = spotify_authentification()
        BASE_URL = 'https://api.spotify.com/v1/'
        re = requests.get(BASE_URL + 'playlists/' + self.playlist_id + '/tracks', headers=headers).json()
        artistTrack = {}
        for i, n in enumerate(re.get('items')):
            artist = re.get('items')[i].get('track').get('album').get('artists')[0].get('name')
            album_name = re.get('items')[i].get('track').get('album').get('name')
            release_date = re.get('items')[i].get('track').get('album').get('release_date')
            duration_ms = re.get('items')[i].get('track').get('duration_ms')
            explicit = re.get('items')[i].get('track').get('explicit')
            track = re.get('items')[i].get('track').get('name')
            popularity = re.get('items')[i].get('track').get('popularity')
            artistTrack[artist] = {'track_name': track, 
                                   'release_date': release_date, 
                                   'duration':duration_ms,
                                   'explicit': explicit,
                                   'album_name': album_name,
                                   'popularity': popularity}
        playlist_dataframe = pd.DataFrame.from_dict(artistTrack, 
                                      orient='index', 
                                      columns=['track_name', 
                                        'release_date',
                                        'duration',
                                        'explicit',
                                        'album_name',
                                        'popularity'])
        playlist_dataframe['release_date']=pd.to_datetime(playlist_dataframe['release_date'])
        playlist_dataframe['duration']=pd.to_timedelta(playlist_dataframe['duration'], unit='ms')
        playlist_dataframe.reset_index(inplace=True)
        playlist_dataframe.rename(columns={'index':'artist'}, inplace=True)
        return playlist_dataframe
    
    def user_playlist_reorder_tracks(
        self,
        user,
        playlist_id,
        range_start,
        insert_before,
        range_length=1,
        snapshot_id=None,
    ):
        """ Reorder tracks in a playlist
            Parameters:
                - user - the id of the user
                - playlist_id - the id of the playlist
                - range_start - the position of the first track to be reordered
                - range_length - optional the number of tracks to be reordered
                                 (default: 1)
                - insert_before - the position where the tracks should be
                                  inserted
                - snapshot_id - optional playlist's snapshot ID
        """
        warnings.warn(
            "You should use `playlist_reorder_items(playlist_id, ...)` instead",
            DeprecationWarning,
        )
        return self.playlist_reorder_items(playlist_id, range_start,
                                           insert_before, range_length,
                                           snapshot_id)
    
    def playlist_shuffle(playlist_URL):
    # need to put the last track on the 4th parameter
        return sp.user_playlist_reorder_tracks('keir20', playlist_URL, 0, random.rand())
    #sp.user_playlist_reorder_tracks('keir20', 'https://open.spotify.com/playlist/2Zbn1h9DY5rJagR2NjeRxR', 0, 37)
    
    def get_playlist_url(self):
        headers = spotify_authentification()
        BASE_URL = 'https://api.spotify.com/v1/'
        re = requests.get(BASE_URL + 'playlists/' + self.playlist_id + '/tracks', headers=headers).json()
        playlist_code = re.get('href').split('/')[5]
        #return f'spotify:track:{playlist_code}'
        return f'https://open.spotify.com/playlist/{playlist_code}'
    
    def playlist_selection_url(self, feeling):
        happiness = 'https://open.spotify.com/embed/playlist/556ICk4gRzDknRfWGeQ3x1'
        sadness = 'https://open.spotify.com/embed/playlist/0dRxDrR1PfZMlVbfnuBRbR'
        anger = 'https://open.spotify.com/embed/playlist/7FjP7MbRgFYFdv5avuhiBI'
        fear = 'https://open.spotify.com/embed/playlist/6EF56fuiUgN2GOMVZIiXpq'
        love = 'https://open.spotify.com/embed/playlist/73KuPUAtOecLDAetRn80TW'
        neutral = 'https://open.spotify.com/embed/playlist/5pSdjjPHbXpbqFJGf31Ksn'
        
        d= {'happy':happiness, 'sadness':sadness, 'love':love, 
        'anger':anger, 'neutral':neutral, 'fear': fear}
        mood = d[feeling]
        
        return mood
        
    
# Playback class

class Playback:
    
    def currently_playing():
        track = sp.current_user_playing_track()
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']
        if artist != "":
            return f"Currently playing {artist} - {track}"
    
    def start_playback(playlist_url):
        return sp.start_playback(context_uri=playlist_url)
        # The below one works with playlists.
        #return sp.start_playback(context_uri='https://open.spotify.com/playlist/37i9dQZF1DWV5sGFwUJeqR?si=c02dd0f6cdfe4206')
        # The below one works with tracks.
        #return sp.start_playback(uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])
        
# User class
class User:
    def user_id():
        sp.trace = True
        user_info = sp.user(username)
        return f"User: {user_info.get('display_name')}" 
    
    def user_followers():
        sp.trace = True
        user_info = sp.user(username)
        followers = user_info.get('followers').get('total')
        return f"Followers: {followers}"
    
    def user_info():
        sp.trace = True
        user_info = sp.user(username)
        user = user_info.get('display_name')
        followers = user_info.get('followers').get('total')
        return f"User: {user} Followers: {followers}"
