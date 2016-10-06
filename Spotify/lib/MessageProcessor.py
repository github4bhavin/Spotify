
import nltk
import os

from nltk.chunk import  *
from nltk.chunk.regexp import  *
from nltk.chunk.util import  *

from pprint import  pprint

os.environ['NLTK_DATA'] = '/Users/bpatel/Developement/Projects/PythonProjects/Spotify/nltk_data'

class MessageProcessor(object):

    def __init__(self, msg):
        self._msg = msg

    @property
    def msg(self): return self._msg

    def get_chunks(self):
        """
        :return: phrases[]
        """
        phrases = []
        chunk_rule  = ChunkRule("<.*>+", "chung everything")

        chunk_merge     = MergeRule("<NN>","<IN>", "merge noun and subordinates")
        chunk_merge2    = MergeRule("<PRP>","<RB><VBP>", "merge proper noun and adverb")
        chunk_merge3    = MergeRule("<VBP>","<PRP>", "personal pronoun and verb")
        chunk_merge4    = MergeRule("<DT|RP>","<NN|DT>", "determiner and nound together")

        chunk_split     = SplitRule('<VBP|VB|NN>','<VB|IN|NN>', 'split with ending verbe')
        chunk_split2    = SplitRule('<RB>','<VBP>', 'split adverb and verb')

        # create a regexp chunk parser
        cp = nltk.RegexpChunkParser([
            chunk_rule ,
            chunk_split,
            chunk_merge, chunk_merge2, chunk_merge3, chunk_merge4
        ],chunk_label='VP')

        parsed_chunks = cp.parse(  nltk.pos_tag( self.msg.split() ) )

        print( parsed_chunks)

        for tag_tree in parsed_chunks:
            phrases.append( ' '.join( [ w for w, l in tag_tree.leaves() ] ) )

        return phrases