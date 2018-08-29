from contextlib import contextmanager
from django.shortcuts import redirect, reverse
from nexaas_id_client.exceptions import SignedOutException


class signed_in:
    __slots__ = ('redirect')

    def __init__(self):
        self.redirect = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        if exc and exc_type is SignedOutException:
            self.redirect = redirect(reverse('nexaas-id-signout'))
            return True  # inhibit raising expected exception
        return exc
