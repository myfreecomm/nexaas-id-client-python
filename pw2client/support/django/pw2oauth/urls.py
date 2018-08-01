from django.conf.urls import patterns, url
from .views import signin, callback

__all__ = ['urlpatterns']

urlpatterns = patterns(
    '',
    url(r'^signin', signin, name='pw2signin'),
    url(r'^callback', callback, name='pw2callback'),
)
