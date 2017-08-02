from django.conf.urls import include, url
from login import views
urlpatterns = [
    url(r'^$', views.login),
    url(r'^login_action$', views.login_action),
    url(r'^changepwd$', views.changepwd),
    url(r'^updatepwd$', views.updatepwd),
    url(r'^bindInterface$', views.bindInterface),
    url(r'^updateInterface$', views.updateInterface),
]