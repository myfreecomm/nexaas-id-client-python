import os.path as path
from vcr import VCR

__all__ = ['vcr']


vcr = VCR(cassette_library_dir=path.join(path.dirname(__file__), 'fixtures'))
