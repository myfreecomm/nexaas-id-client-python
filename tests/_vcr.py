import os.path as path
from vcr import VCR
from vcr.request import Request

__all__ = ['vcr']


def before_record(request: Request) -> Request:
    # Do not record test server
    return None if request.port == 3030 else request


vcr = VCR(
    cassette_library_dir=path.join(path.dirname(__file__), 'fixtures'),
    before_record=before_record,
)
