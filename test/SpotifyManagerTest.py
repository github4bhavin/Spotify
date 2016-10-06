
import SpotifyTest
import unittest

from pprint import  pprint
from Spotify.lib.SpotifyManager import  SpotifyManager
from Spotify.lib.MessageProcessor import  MessageProcessor

config = dict(
    SP_USERNAME = 'spotify4bhavin',
    SP_CLIENT_ID = '445ce73bb6bd4f3d8e1426a875b104bf',
    SP_CLIENT_SECRET = '92ecb83106094c08bffbbcfd65850bc6',
    SP_REDIRECT_URI= 'http://localhost:8888/oauth'
)

class SpotifyManagerTest(unittest.TestCase):

    def setUp(self):
        self.obj = SpotifyManager(
                username=config['SP_USERNAME'],
                client_id=config['SP_CLIENT_ID'],
                client_secret=config['SP_CLIENT_SECRET'],
                redirect_uri=config['SP_REDIRECT_URI']
        )

    def test_search(self):
        mp = MessageProcessor("if i can't let it go out of my mind")
        phrases = mp.get_chunks()

        for phrase in phrases:
            print( " pharse : " + phrase)
            pprint( self.obj.search( phrase ) )

    def test_get_token(self):
        token = self.obj.get_token()
        print( token )

if __name__ == '__main__':
    unittest.main()