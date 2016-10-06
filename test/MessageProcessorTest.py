
import os
import SpotifyTest
import unittest

import nltk

from pprint import  pprint
from nltk.corpus import  conll2000, brown

from Spotify.lib.MessageProcessor import MessageProcessor, MyUnigramChunker


os.environ['NLTK_DATA'] = '/Users/bpatel/Developement/Projects/PythonProjects/Spotify/nltk_data'

class MessageProcessorTest(unittest.TestCase):

    def setUp(self):
        self.obj = MessageProcessor(msg="if i can't let it go out of my mind")

    def test_message_chunking(self):
        print( self.obj.get_chunks() )


class MyUnigramChunkerTest(unittest.TestCase):

    def setUp(self):
        self.msg="if i can't let it go out of my mind"
        train = conll2000.chunked_sents(chunk_types=['NP'])
        self.obj = MyUnigramChunker( train= train )

    def _test_parse(self):
        test  = conll2000.chunked_sents(chunk_types=['NP'])
        print( self.obj.evaluate( test ))

        wtokens = nltk.word_tokenize( self.msg )
        print ( wtokens )

        pos_tags = nltk.pos_tag( wtokens )

        print( pos_tags )

        tagged_pos_tags = self.obj._trained_tagger.tag( wtokens )

        print( tagged_pos_tags )

        print( test )


    def _test_parse(self):
        print( 'test parse')

        test = conll2000.chunked_sents('test.txt',chunk_types=['NP'])

        wtokens = nltk.word_tokenize(self.msg)
        print (wtokens)

        pos_tags = nltk.pos_tag(wtokens)

        print(pos_tags)

        ttokens = [ t for (p, t) in pos_tags ]

        tagged_pos_tags = self.obj._trained_tagger.tag(ttokens)

        print(tagged_pos_tags)


    def test_nested_chunker(self):
        wtokens = nltk.word_tokenize(self.msg)
        print (wtokens)

        pos_tags = nltk.pos_tag(wtokens)

        print(pos_tags)


        grammar = r"""
            NP: {<IN><NNS><MD><RB>}
            PP: {<VB><PRP><VB>}
            VP: {<IN><IN><PRP.><NN>}
            CLAUSE: {<NP><VP>}
        """
        cp = nltk.RegexpParser(grammar)
        res = cp.parse(pos_tags)

        print("--- test next chuning ---")

        for sent in res:
            print( t)
            print(sent )
            print( len(sent ))
            sent = [ w for w, t in sent ]
            print( ' '.join(sent) )

        print("--- test nest chuning ---")


    def test_nested_chunker_2(self):
        msg = 'I see the King of glory Coming on the clouds of fire'
        wtokens = nltk.word_tokenize( msg )
        print (wtokens)

        pos_tags = nltk.pos_tag(wtokens)

        print(pos_tags)

        grammar = r"""
            NP: {<IN><NNS><MD><RB>}
            PP: {<VB><PRP><VB>}
            VP: {<IN><IN><PRP.><NN>}
            CLAUSE: {<NP><VP>}
        """
        cp = nltk.RegexpParser(grammar)
        res = cp.parse(pos_tags)

        print("--- test next chuning 2---")

        for sent in res:
            print(sent)
            print( len( sent ))
            if len(sent)>1:
                for (w,t) in sent:
                    print( w , t )
            #sent = [w for w, t in sent]
            #print(' '.join(sent))

        print("--- test next chuning 2---")

if __name__ == '__main__':
    unittest.main(verbosity=3)