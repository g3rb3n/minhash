import os
import sys
from PIL import Image
import itertools
from random import shuffle
from math import pow
import skimage
import skimage.color
from skimage.feature import corner_fast, corner_peaks
from skimage import io
from skimage.transform import resize
from skimage.transform import rescale
from skimage.color import rgb2gray
from skimage import img_as_ubyte
import numpy as np


class ImageHasher:

    def __init__(
        self,
        n_gram_length=1,
        signature_length=2,
        number_of_signatures=5,
        size=(16, 16),
        bits=3
    ):
        self._size = size
        self.n_gram_length = n_gram_length
        self.number_of_signatures = number_of_signatures
        self.signature_length = signature_length
        self.bits = bits
        self.scale = int(pow(2, 8 - self.bits))
        self.range = int(pow(2, self.bits))
#        print self.scale
#        print self.range
        self.alphabet = [b for b in range(0, self.range)]
        self.build_feature_space()
        self.build_hash_dicts()

    def build_feature_space(self):
        self.feature_space = [
            tuple(tup)
            for tup
            in itertools.product(self.alphabet, repeat=self.n_gram_length)
        ]
#        print self.feature_space

    def build_hash_dicts(self):
        self.hash_dicts = []
        for i in range(0, self.number_of_signatures):
            self.hash_dicts.append({self.feature_space[idx]: idx
                                    for idx in xrange(len(self.feature_space))})
            shuffle(self.feature_space)

    def load(self, filename):
        try:
            #            image = Image.open(filename)
            image = io.imread(filename)
            image = resize(image, self._size, order=0)
            np.swapaxes(image, 0, 2)
#            image = skimage.color.rgb2hsv(image)
#            print image
#            print self._size
#            image = corner_fast(image)
            image = image / self.scale
            dbimage = image * self.scale
            dbimage = rescale(dbimage, 32, order=0)
            io.imsave('debug/' + filename.split('/')[-1], dbimage)
#            print dbimage
#            sys.exit()
            image = img_as_ubyte(image)
#            image = np.clip(image, 0, 3)
#            print image

            return image
        except IOError:
            print "cannot preprocess '%s'" % filename

    def hashes(self, s):
        features = self.features(s, self.n_gram_length)
        return [
            self.hash_features(features, i)
            for i in range(0, self.number_of_signatures)
        ]

    def slide(self, s, w):
        if len(s) < w:
            raise 'String "%s" is shorter than %s' % (s, w)
        return [tuple(s[i: i + w]) for i in xrange(len(s) - w + 1)]

    def features(self, image):
        s = image.ravel()
        return set(self.slide(s, self.n_gram_length))

    def hash_feature_index(self, feature, i):
        """
        get hash index for a feature
        features: feature list
        i: hashDict index
        returns index of feature
        """
        if not feature in self.hash_dicts[i]:
            raise Exception('Feature does not exist in feature space'
                            + str(feature))
        return self.hash_dicts[i][feature]

    def hash_features(self, features, i=0):
        """
        get hash for a feature list
        features: feature list
        i: hashDict index
        returns hash as tuple
        """
        hashes = sorted([self.hash_feature_index(feature, i)
                         for feature in features])
        return tuple(hashes[:self.signature_length])
