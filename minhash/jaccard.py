from .texthasher import TextHasher


class Jaccard(object):

    def __init__(self, hasher=TextHasher()):
        self.hasher = hasher

    def similarity(self, a, b):
        """
        Jaccard similarity
        a: string
        b: string
        returns similarity as float between 0 and 1
        """
        setA = self.hasher.features(a)
        setB = self.hasher.features(b)
        union = setA | setB
        intersection = setA & setB
        return float(len(intersection)) / len(union)
