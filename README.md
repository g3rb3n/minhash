## Synopsis
A deduplication tool based on minhash.

See: https://en.wikipedia.org/wiki/MinHash


## Example
```python
from minhash.dedup import Dedup 
dedup = Dedup()
res = dedup.is_duplicate('This is a test')      # returns False
res = dedup.is_duplicate('This is a test')      # returns True
res = dedup.is_duplicate('This is a test2')     # returns True most of the time
res = dedup.is_duplicate('Something different') # returns False
```


## Installation
```sh
pip install .
```


## Tests
```sh
nosetest
```


## License
MIT
