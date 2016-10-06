

import spotipy
from spotipy import  SpotifyException
import spotipy.util as util
import spotipy.oauth2 as oauth2

class SpotifyManager:

    _sm = None
    _scope = None
    _username =None
    _token = None
    _sp  = None
    oauth_obj = None
    tokens = None
    last_playlist_id = None

    def __init__(self, username, client_id, client_secret, redirect_uri):
        self._scope = ' '.join([ 'user-library-read',
                                 'playlist-modify-public',
                                 'playlist-modify-private'
                                 ])
        self._username = username


        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

        self.get_spotify_obj()
        self.get_spotify_oauth_obj()

    @property
    def username(self): return self._username

    def get_spotify_obj(self,token=None):
        self._sp = spotipy.Spotify(auth=token)


    def get_spotify_oauth_obj(self):
        if not self.oauth_obj:
            self.oauth_obj = oauth2.SpotifyOAuth( client_id=self._client_id,
                                 client_secret=self._client_secret,
                                 redirect_uri=self._redirect_uri,
                                 scope=self._scope)
        return self.oauth_obj
    # end point methods

    def search(self, term , type='track', limit=50):
        try:
            response = self._sp.search( "\"%s\""%(term) , limit=limit, type=type)
        except SpotifyException as e:
            print ( e )
            return None

        results = None
        request_url = response['tracks']['href']
        items = response['tracks']['items']

        if not len(items): return None

        for item in items:
            if item['name'].lower() == term.lower():
                return {
                    'name'          : item['name'],
                    'uri'           : item['uri'],
                    'href'          : item['href'],
                    'extern_url'    : item['external_urls']['spotify'],
                    'request_url'   : request_url,
                    'id'            : item['id'],
                    'preview_url'   : item['preview_url'],
                    'popularity'    : item['popularity'],
                    'artist'        : item['artists'][0]['name'],
                    'album'         : item['album']['name']
                }


    # action methods #

    def create_playlist(self, playlist, name='newplaylist'):
        try:
            response = self._sp.user_playlist_create( self.username, name, public=False)
            # @todo should be an playlist object
            self.last_playlist_id = response['id']
            track_ids = [ song['id'] for song in playlist ]
            result = self._sp.user_playlist_add_tracks( self.username, self.last_playlist_id, track_ids)
        except SpotifyException as e:
            print( e )

    def get_playlist(self):
        try:
            response = self._sp.user_playlist( self.username, self.last_playlist_id )
            items = response['tracks']['items']
            playlist = []
            for item in items:
                playlist.append({
                    'name' : item['track']['name'],
                    'href' : item['track']['href'],
                    'id': item['track']['id'],
                    'album' : item['track']['album']['name'],
                    'preview_url': item['track']['preview_url'],
                    'popularity' : item['track']['popularity'],
                    'artists': item['track']['artists'][0]['name'],
                    'external_url' : item['track']['external_urls']['spotify']
                })

            return playlist


        except SpotifyException as e:
            print(e)




    def is_access_token_valid(self):
        pass
    def get_token(self,code):
        self.tokens = self.oauth_obj.get_access_token(code)
        self.get_spotify_obj( self.tokens['access_token'])
        return self.tokens['access_token']

    def get_oauth_url(self):
        auth_url = self.oauth_obj.get_authorize_url()
        return auth_url

    def get_response_url(self,code):
        return self.oauth_obj.parse_response_code( code )