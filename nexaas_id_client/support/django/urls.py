from django.urls import path
from . import views

__all__ = ['urlpatterns']

urlpatterns = [
    path(r'signin/', views.signin, name='nexaas-id-signin'),
    path(r'signout/', views.signout, name='nexaas-id-signout'),
    path(r'callback/', views.callback, name='nexaas-id-callback'),
]
