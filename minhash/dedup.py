import os.path
from .minhash import MinHash
from datetime import timedelta, datetime
import logging
import json


def inc(d, k):
    if k not in d:
        d[k] = 0
    d[k] = d[k] + 1


class Dedup:

    def __init__(
        self, minhash, filename, max_age=timedelta(
            hours=1), cleanup_interval=timedelta(
            minutes=1)):
        #        super(Dedup, self).__init__()
        self._filename = filename
        self._max_age = max_age
        self._cleanup_interval = cleanup_interval

        self._minhash_dict = {}
        self._last_cleanup = datetime.utcnow() - cleanup_interval
        self._minhash = minhash

        self.load()
        self.cleanup()
        self._stats = {}

        logging.debug('Number of unique hashes: %s' % len(self._minhash_dict))

    def load(self):
        if os.path.isfile(self._filename):
            with open(filename, 'r') as f:
                self._minhash_dict = json.load(f)

    def save(self):
        with open(self._filename, 'w') as f:
            json.dump(self._minhash_dict, f)

    def is_duplicate(self, text, dt):
        self.cleanup_if_needed()

        footprint = tuple(self._minhash.hashes(text))
        if footprint in self._minhash_dict:
            inc(self._stats, 'duplicates')
            return True

        self._minhash_dict[footprint] = dt
        return False

    def get_similars(self, text, dt):
        self.cleanup_if_needed()
        ret = []
        footprint = tuple(self._minhash.hashes(text))
        if footprint in self._minhash_dict:
            inc(self._stats, 'duplicates')
            ret.append(self._minhash_dict[footprint])

        self._minhash_dict[footprint] = dt
        return []

    def cleanup(self):
        min_dt = datetime.utcnow() - self._max_age
        for footprint, dt in self._minhash_dict.iteritems():
            if dt < min_dt:
                del self._minhash_dict[footprint]

    def cleanup_if_needed(self):
        if datetime.utcnow() > self._last_cleanup + self._cleanup_interval:
            self.cleanup()
