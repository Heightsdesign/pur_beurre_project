from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<user_id>[0-9]+)/$', views.user_page, name='user_page'),
    url(r'^favorites/$', views.favorites_page, name='favorites'),
    url(r'^subscribe/$', views.subscribe_page, name='subscribe'),
    url(r'^connexion/$', views.connexion_page, name='connexion'),
    url(r'^logout/$', views.logout_view, name='logout'),
    ]

