from requests.exceptions import HTTPError
from requests.models import Response

__all__ = ['SignedOutException']


class SignedOutException(HTTPError):

    @classmethod
    def from_http_error(cls, exc: HTTPError) -> HTTPError:
        error = cls(
            request=exc.request,
            response=exc.response,
        )
        error.__context__ = exc
        return error

    @classmethod
    def check_status(cls, res: Response) -> None:
        try:
            res.raise_for_status()
        except HTTPError as exc:
            if res.status_code == 401:
                raise cls.from_http_error(exc)
            raise
