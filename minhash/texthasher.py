import itertools
import slugify
import re

from random import shuffle
from math import pow

_re_concat = re.compile(r'(\w+)(-)(?=\w+)')
_re_ellipsis = re.compile(r'#*\w+(\.{3}|\xe2\x80\xa6)')
_re_http = re.compile(r'http\S*')
_re_mention = re.compile(r'@\w+')
_re_word = re.compile(r'\w+')

# Overwrite slugify regexp to allow for #, -, and _
slugify.REPLACE2_REXP = re.compile(r'[^-#_a-z0-9]+')


class TextHasher(object):

    def __init__(
        self, n_gram_length=3, signature_length=2, number_of_signatures=1,
        alphabet='abcdefghijklmnopqrstuvwxyz0123456789#_ '
    ):
        self.n_gram_length = n_gram_length
        self.signature_length = signature_length
        self.number_of_signatures = number_of_signatures
        self.alphabet = alphabet
        self.build_feature_space()
        self.build_hash_dicts()

    def set_charachter_alphabet(self, chars):
        """
        Set the character alphabet
        """
        self.alphabet = chars
        self.build_feature_space()
        self.build_hash_dicts()

    def build_feature_space(self):
        """
        Build the feature space, a list of all possible features.
        """
        self.feature_space = [
            ''.join(tup) 
            for tup
            in itertools.product(self.alphabet, repeat=self.n_gram_length)
        ]

    def build_hash_dicts(self):
        """
        Build the hash dictionaries.
        For each signature a different ordering of the features is required.
        """
        self.hash_dicts = []
        for i in range(0, self.number_of_signatures):
            self.hash_dicts.append({self.feature_space[idx]: idx
                                   for idx in xrange(len(self.feature_space))})
            shuffle(self.feature_space)

    def slide(self, s, w):
        """
        slide over string
        s : Input string
        w : Feature length
        returns array with all fixed length strings found
        """
        if len(s) < w:
            raise Exception('String "%s" is shorter than %s' % (s, w))
        return [s[i: i + w] for i in xrange(len(s) - w + 1)]

    def clean(self, s):
        """
        Clean up string
        """
        # Remove ellipsis, encode to utf-8, convert to lowercase
        s = _re_ellipsis.sub(lambda x: '', s.encode('utf-8').lower())
        # Remove urls
        s = _re_http.sub(lambda x: '', s)
        # Remove user mentions (i.e., @)
        s = _re_mention.sub(lambda x: '', s)
        # Replace concatenation dash with underscore
        s = _re_concat.sub(r'\1_', s)
        # Slugify, and return
        return slugify.slugify(unicode(s), separator=' ')

    def ensure_length(self, s, l):
        """
        make sure string has a length of size l
        s: string
        l: feature length
        returns string
        """
        return s + ''.join(' ' for i in range(l - len(s)))

    def fill(self, s):
        """
        prepend and append whitespace
        s: string
        returns longer string
        """
        n = self.n_gram_length - 1
        s = ''.join(' ' for i in range(n)) + s + ''.join(' ' for i in range(n))
        return s

    def features(self, s):
        """
        get features for a string
        s: string
        n: feature length
        returns set with features
        """
        s = self.clean(s)
        s = self.fill(s)
        s = self.ensure_length(s, self.n_gram_length)
        return set(self.slide(s, self.n_gram_length))

    def hash_feature_index(self, feature, i):
        """
        get hash index for a feature
        features: feature list
        i: hashDict index
        returns index of feature
        """
        if not feature in self.hash_dicts[i]:
            raise Exception(
                'Feature %s does not exist in feature space' %
                feature)
        return self.hash_dicts[i][feature]


    def hash_features(self, features, i=0):
        """
        get hash for a feature list
        features: feature list
        i: hash dict index
        returns hash as tuple
        """
        hashes = sorted([self.hash_feature_index(feature, i)
                         for feature in features])
        return tuple(hashes[:self.signature_length])

    def hash(self, s, i=0):
        """
        get hash for a string
        s: string
        returns hash as tuple
        """
        features = self.features(s)
        return self.hash_features(features, i)

    def hashes(self, s):
        """
        get hashes for a string
        s: string
        returns all hashes as array of tuples
        """
        features = self.features(s)
        return [
            self.hash_features(features, i)
            for i in range(0, self.number_of_signatures)
        ]
