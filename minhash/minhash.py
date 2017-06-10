from .texthasher import TextHasher


class MinHash(object):

    def __init__(self, hasher=TextHasher()):
        self.hasher = hasher

    def similarity(self, a, b):
        """
        MinHash similarity
        a: string
        b: string
        returns similarity as float between 0 and 1
        """
        hashesA = self.hasher.hashes(a)
        hashesB = self.hasher.hashes(b)
        similar = 0
        for i in range(0, self.hasher.number_of_signatures):
            if hashesA[i] == hashesB[i]:
                similar += 1
        return pow(
            float(similar) / self.hasher.number_of_signatures,
            1.0 / self.hasher.signature_length
        )
