from abc import ABCMeta
from collections import namedtuple
from datetime import datetime, timedelta
from urllib.parse import parse_qsl, urlencode

__all__ = ['AbstractToken', 'OAuthToken', 'TokenSerializer']


class AbstractToken(metaclass=ABCMeta):

    Base = namedtuple(
        'OAuthToken',
        'access_token refresh_token expires_at',
    )

    @classmethod
    def __subclasshook__(cls, C):
        for attr in cls.Base._fields:
            if not any(attr in B.__dict__ for B in C.__mro__):
                return NotImplemented
        return True


class OAuthToken(AbstractToken.Base):

    def __new__(cls, access_token: str, refresh_token: str = None,
                expires_at: int = -1,
                expires_in: int = -1, **__) -> AbstractToken.Base:
        if expires_at >= 0:
            expires_at = datetime.fromtimestamp(expires_at)
        elif expires_in >= 0:
            expires_at = datetime.now() + timedelta(seconds=expires_in)
        else:
            expires_at = None
        return super().__new__(cls, access_token, refresh_token, expires_at)

    @property
    def expired(self) -> bool:
        return self.expires_at < datetime.now()

AbstractToken.register(OAuthToken)


class TokenSerializer:

    @staticmethod
    def serialize(token: AbstractToken) -> str:
        return urlencode({
            attr: getattr(self, attr)
            for attr in AbstractToken.Base._fields
        })

    @staticmethod
    def deserialize(token: str) -> AbstractToken:
        return OAuthToken(**{
            attr: value
            for attr, value in parse_qsl(token)
            if attr in AbstractToken.Base._fields
        })
