
import os
import SpotifyTest
import unittest

import nltk

from pprint import  pprint
from nltk.corpus import  conll2000, brown

from nltk.chunk import  *
from nltk.chunk.util import  *
from nltk.chunk.regexp import *


os.environ['NLTK_DATA'] = '/Users/bpatel/Developement/Projects/PythonProjects/Spotify/nltk_data'

class RegexpChunkerTest(unittest.TestCase):

    def setUp(self):

        self.msg1 = "if i can't let it go out of my mind"
        self.msg2 = "I never see you anymore come out the door it's like you've gone away"
        self.msg3 = "about a thing"

    def get_pos_tokens(self, msg):
        wtokens = msg.split()
        print (wtokens)

        pos_tags = nltk.pos_tag(wtokens)

        print(pos_tags)
        return pos_tags

    def test_nested_chunker_2(self):

        """
            1. can never split in proper noun (PRP)
            2.
        :return:
        """

        chunk_rule = ChunkRule("<.*>+", "chung everything")

        chunk_merge = MergeRule("<NN>","<IN>", "merge noun and subordinates")
        chunk_merge2 = MergeRule("<PRP>","<RB><VBP>", "merge proper noun and adverb")
        chunk_merge3 = MergeRule("<VBP>","<PRP>", "personal pronoun and verb")
        chunk_merge4 = MergeRule("<DT|RP>","<NN|DT>", "determiner and nound together")

        chunk_split = SplitRule('<VBP|VB|NN>','<VB|IN|NN>', 'split with ending verbe')
        chunk_split2 = SplitRule('<RB>','<VBP>', 'split adverb and verb')

        cp = nltk.RegexpChunkParser([
            chunk_rule ,
            chunk_split,
            chunk_merge, chunk_merge2, chunk_merge3, chunk_merge4
        ],chunk_label='VP')


        res = cp.parse( self.get_pos_tokens( self.msg1 ) )
        print(cp)
        for r in res:
            print( ' '.join( [ w for w, l in r.leaves() ] ) )

        res = cp.parse( self.get_pos_tokens( self.msg2 ) )
        print( res )

        for r in res:
            print( ' '.join( [ w for w, l in r.leaves() ] ) )

        res = cp.parse(self.get_pos_tokens(self.msg3))
        print(res)

        for r in res:
            print(' '.join([w for w, l in r.leaves()]))


if __name__ == '__main__':
    unittest.main(verbosity=3)