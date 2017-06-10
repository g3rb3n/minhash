from os import listdir
from os.path import isfile, join

from minhash.imagehasher import ImageHasher
from minhash.dedup import Dedup

def test_img():
    hasher = ImageHasher()

    path = 'data'

    f = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    d = [hasher.load(i) for i in f]
    f = [hasher.features(i) for i in d]
    h = [hasher.hashes(i) for i in d]

    dd = Dedup(hasher=hasher)
    res = dd.is_duplicate(d[i])
    assert res == False, "Initial image should be unique"
    for i in range(0, len(d)):
        res = dd.is_duplicate(d[i])
        assert res == True, "Similar image should be duplicate"
