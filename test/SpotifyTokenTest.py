import sys, os
import spotipy
import spotipy.util as util


# set env vars

os.environ['SPOTIPY_CLIENT_ID'    ] = '445ce73bb6bd4f3d8e1426a875b104bf'
os.environ['SPOTIPY_CLIENT_SECRET'] = '92ecb83106094c08bffbbcfd65850bc6'
os.environ['SPOTIPY_REDIRECT_URI' ] = 'http://localhost:8888/oauth'

_DEFAULT_USERNAME = 'sportify4bhavin'


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name'])


if __name__ == '__main__':
    username = _DEFAULT_USERNAME

    print( username )
    token = util.prompt_for_user_token(username)
    print( token )

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print
                print playlist['name']
                print '  total tracks', playlist['tracks']['total']
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print "Can't get token for", username