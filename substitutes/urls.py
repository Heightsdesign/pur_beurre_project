from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<product_id>[0-9]+)/$', views.product_detail),
    url(r'^search/$', views.search),

]