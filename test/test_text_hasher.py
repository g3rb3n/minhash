import os.path
from minhash.texthasher import TextHasher

def test_features():
    s = TextHasher(n_gram_length=3)
    i = '123'
    f = s.features(i)
    assert len(f) == 5, "number of features is wrong: %i %s" % (len(f), f)

def test_fill():
    s = TextHasher(n_gram_length=3)
    i = '123'
    s = s.fill(i)
    assert len(s) == 7, "fill is wrong: %i %s" % (len(s), s)
