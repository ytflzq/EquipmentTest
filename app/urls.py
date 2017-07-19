from django.conf.urls import include, url
from app import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^interfaceEdit$', views.interfaceEdit),
    url(r'^interfaceUpdata$', views.interfaceUpdata),
    url(r'^createMessageGroup$', views.createMessageGroup),
    url(r'^createMessage$', views.createMessage),
    url(r'^insertMessageGroup$', views.insertMessageGroup),
    url(r'^insertMessage$', views.insertMessage),
    url(r'^messageList$', views.messageList),
    url(r'^importFile$', views.importFile),
    url(r'^uploadFile$', views.uploadFile),
    url(r'^step1$', views.step1),
    url(r'^step2$', views.step2),
    url(r'^step3$', views.step3),
    url(r'^step4$', views.step4),
    url(r'^rate$', views.rate),
    url(r'^exit$', views.exit)
]