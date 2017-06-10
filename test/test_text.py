from minhash.minhash import MinHash
from minhash.jaccard import Jaccard
from minhash.texthasher import TextHasher

def test_compare():
    mh = MinHash(hasher=TextHasher(number_of_signatures=20))
    ja = Jaccard()

    i1 = 'Dit is geen test'
    i2 = 'Dit is een test'

    mh_sim = mh.similarity(i1, i2)
    ja_sim = ja.similarity(i1, i2)

    assert abs(mh_sim - ja_sim) < .2, "similarity difference is too large: %r %r" % (ja_sim, mh_sim)

def test_1():
    mh = MinHash()
    i = 'Dit is een test'
    sim = mh.similarity(i, i) 
    assert sim == 1, "similarity is not 1: %r" % sim

def test_0():
    mh = MinHash()
    i = 'Dit is een test'
    sim = mh.similarity(i, '') 
    assert sim == 0, "similarity is not 0: %r" % sim
