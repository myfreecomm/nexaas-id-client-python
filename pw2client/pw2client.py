from collections import namedtuple
import re
from typing import Union
from urllib.parse import ParseResult, urlencode, urlparse
from uuid import UUID
import dateutil.parser
import requests
from .oauth_client import PW2OAuthClient

__all__ = ['PW2Client']


ClientProps = namedtuple('ClientProps', 'access_token id secret server')


class PW2Client:
    __slots__ = (
        '__internal_tuple',
        '_personal_info',
        '_professional_info',
        '_emails',
        '_contacts',
    )

    @classmethod
    def from_oauth(cls, access_token: str, *,
                   client: PW2OAuthClient) -> 'PW2Client':
        return cls(
            access_token=access_token,
            id=client.id,
            secret=client.secret,
            server=client.server,
        )

    def __init__(self, access_token: str, *,
                 id: str = None, secret: str = None,
                 server: Union[str, ParseResult] = None):
        server = server if isinstance(server, ParseResult) \
            else urlparse(server or 'http://localhost:3000/')
        server = server._replace(
            query=urlencode({'access_token': access_token}),
        )
        self.__internal_tuple = ClientProps(access_token, id, secret, server)
        self.reset()

    def __get_response(self, path) -> dict:
        res = requests.get(self.server._replace(path=path).geturl())
        res.raise_for_status()
        return res.json(object_hook=_json_decode)

    @property
    def access_token(self):
        return self.__internal_tuple.access_token

    @property
    def id(self):
        return self.__internal_tuple.id

    @property
    def secret(self):
        return self.__internal_tuple.secret

    @property
    def server(self):
        return self.__internal_tuple.server

    @property
    def personal_info(self):
        if self._personal_info is None:
            info = self.__get_response(path='/api/v1/profile')
            self._personal_info = _build_tuple('PersonalInfo', **info)
        return self._personal_info

    @property
    def professional_info(self):
        if self._professional_info is None:
            info = self.__get_response(
                path='/api/v1/profile/professional_info'
            )
            self._professional_info = _build_tuple('ProfessionalInfo', **info)
        return self._professional_info

    @property
    def emails(self):
        if self._emails is None:
            info = self.__get_response(path='/api/v1/profile/emails')
            self._emails = _build_tuple('Emails', **info)
        return self._emails

    @property
    def contacts(self):
        if self._contacts is None:
            info = self.__get_response(path='/api/v1/profile/contacts')
            self._contacts = _build_tuple('Contacts', **info)
        return self._contacts

    def reset(self):
        self._personal_info = None
        self._professional_info = None
        self._emails = None
        self._contacts = None


def _build_tuple(_class_name: str, **info) -> tuple:
    info_class = namedtuple(_class_name, info.keys())
    return info_class(**info)


def _json_decode(value):
    if isinstance(value, str):
        if _is_date(value):
            return dateutil.parser.parse(value).date()
        if _is_datetime(value):
            return dateutil.parser.parse(value)
        if _is_uuid(value):
            return UUID(value)

    elif isinstance(value, list):
        return [_json_decode(e) for e in value]

    elif isinstance(value, dict):
        return {k: _json_decode(v) for k, v in value.items()}

    return value


def _is_date(value):
    return re.match(r'^\d{4}-\d\d-\d\d$', value) is not None


def _is_datetime(value):
    return re.match(
        r'^\d{4}-\d\d-\d\d'
        r'[T ]\d\d:\d\d:\d\d(\.\d{3})?'
        r'([A-Z]{1,5}|GMT[+-]\d+)?$',
        value,
    ) is not None


def _is_uuid(value):
    return re.match(
        r'^[0-9a-f]{8}-'
        r'[0-9a-f]{4}-'
        r'[0-9a-f]{4}-'
        r'[0-9a-f]{4}-'
        r'[0-9a-f]{12}$',
        value,
    ) is not None