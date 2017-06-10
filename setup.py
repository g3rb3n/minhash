from setuptools import setup

setup(name='minhash',
      version='0.1',
      description='Minhash for text deduplication',
      url='http://github.com/g3rb3n/minhash',
      author='g3rb3n',
      author_email='3grbn3@gmail.com',
      license='MIT',
      packages=['minhash'],
      install_requires=['python-slugify==1.2.1']
      zip_safe=False)