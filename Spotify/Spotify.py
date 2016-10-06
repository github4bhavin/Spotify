
import  logging
from lib.MessageProcessor import  MessageProcessor
from lib.SpotifyManager import  SpotifyManager

from flask import Flask , render_template, request , session, redirect

app = Flask(__name__)

app.config.update( dict(
    SP_USERNAME = 'sportify4bhavin',
    SP_CLIENT_ID = '',
    SP_CLIENT_SECRET = '',
    SP_REDIRECT_URI= 'http://localhost:8888/oauth'
))

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

MAX_RETRIES = 5

@app.route('/' , methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/playlist', methods=['GET','POST'])
def playlist():

    print ( request.form.values() )
    if not len(request.form.values()):
        return redirect("/", code=302)

    msg = request.form['search-message']
    app.logger.info( msg )

    # get playlist after every possible resolution of msg
    playlist = get_playlist(msg=msg , retries= MAX_RETRIES, final_playlist=[])

    session['playlist'] = playlist
    session['msg'] = msg

    print('---playlist in plylist request')
    print( playlist)

    return   render_template('playlist.html', playlist = playlist, search_message = msg)


@app.route('/createPlaylist', methods=['GET','POST'])
def createPlaylist():
    sp = get_spotify_manager()
    oauth_url = sp.get_oauth_url()
    oauth_url = oauth_url.replace('https:','')
    return render_template('spotify_grant.html', oauth_url =oauth_url)


@app.route('/oauth', methods=['GET','POST'])
def oauth_token():
    sp = get_spotify_manager()

    token = sp.get_token( request.args['code'])

    sp.create_playlist( session['playlist'], name= session['msg'] )
    playlist = sp.get_playlist()

    print( '-- playlist after create ---')
    print( playlist )
    return render_template('show_playlist.html', playlist= playlist)

# helpers

def get_playlist(msg, retries=MAX_RETRIES , final_playlist=[]):
    """
        @todo:
        retries to use the different grammer
    :param msg:
    :param retries:
    :param final_playlist:
    :return:
    """
    print( retries )
    # if no more retires left then return the last computed result
    if retries == 0:
        print("[warn] - unable to get phrases for (%s)..." %(msg))
        return final_playlist

    phrases = get_phrases(msg)

    # if this is the last retri then split the works
    # there is so much we can do
    if retries == MAX_RETRIES -1 :
        print("[info] - last retry to get the phrases (%s) ..." %(msg))

        # preety stupid was to keep spliting in half and see if we get teh phrases back
        phrases = msg.split(' ',2)


    playlist = get_playlist_from_spotify( phrases )

    # check if we received songs for every term
    # if not then refactor the terms if possible and get songs again
    # order is imp
    for phrase in phrases:
        if playlist[ phrase ]:
            final_playlist.append( playlist[phrase] )
        else:
            # if we dont have a track for the term
            get_playlist( msg=phrase , retries=retries - 1, final_playlist=final_playlist )
    return final_playlist

def get_phrases(msg=None):
    if not msg:
        return None

    mp = MessageProcessor( msg=msg )
    phrases = mp.get_chunks()
    app.logger.info( phrases )
    return phrases


def get_playlist_from_spotify(phrases):
    sp = get_spotify_manager()
    playlist = {}

    # get songs from spotify
    for phrase in phrases:
        song = sp.search( term=phrase )
        playlist[phrase] = song if song else None
    return playlist

def get_spotify_manager():
    return SpotifyManager(
        username        = app.config['SP_USERNAME'],
        client_id       = app.config['SP_CLIENT_ID'],
        client_secret   = app.config['SP_CLIENT_SECRET'],
        redirect_uri    = app.config['SP_REDIRECT_URI']
    )