from django.urls import path
from . import views

__all__ = ['urlpatterns']

urlpatterns = [
    path(r'signin/', views.signin, name='pw2-signin'),
    path(r'signout/', views.signout, name='pw2-signout'),
    path(r'callback/', views.callback, name='pw2-callback'),
]
