from django.conf.urls import include, url
from app import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^interfaceEdit$', views.interfaceEdit),
    url(r'^interfaceUpdata$', views.interfaceUpdata),
    url(r'^rate$', views.rate),
     url(r'^exit$', views.exit)
]