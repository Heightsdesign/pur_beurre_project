from django.conf.urls import url
from . import views
from django.urls import path

app_name = "substitutes"

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^search/$", views.search, name="search"),
    url(r"^(?P<product_id>[0-9]+)/$", views.product_detail, name="detail"),
    url(r"^legal$", views.legal_mentions, name="legal_mentions"),
    path('sentry-debug/', views.trigger_error),
]
