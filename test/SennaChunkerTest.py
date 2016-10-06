

import  unittest
import  nltk

from nltk.chunk.regexp import *
from nltk.chunk import  *
from nltk.chunk.util import  *

from nltk.tag import SennaChunkTagger

senna_path = '/Users/bpatel/Downloads/senna'

class SennaChunkerTest(unittest.TestCase):

    def setUp(self):
        self.senna = SennaChunkTagger( senna_path )

    def test_chunker_sent_1(self):
        message = "if i can't let it go out of my mind"

        sent = message.split()
        tagged_sent = self.senna.tag( sent )

        print('----- tagged sent')
        print( tagged_sent)

        chunk_rule = ChunkRule("<.*>+" , 'chunk everything ')
        split_rule = SplitRule("<DT><NN>","<DT><NN>" ,"split successive determiner / noun pairs")
        cp = nltk.RegexpChunkParser( [ split_rule], chunk_label= 'NP')

        chunked_test = cp.parse( tagged_sent )
        print('---- chunked test ')
        print( chunked_test )


if __name__ == '__main__':

    unittest.main(verbosity= 3)