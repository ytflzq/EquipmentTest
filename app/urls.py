from django.conf.urls import include, url
from app import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^rate$', views.rate),
    url(r'^getRate$', views.getRate),
    url(r'^importFile$', views.importFile),
    url(r'^uploadFile$', views.uploadFile),
    url(r'^allIndex$', views.allIndex),
    url(r'^getAllRate$', views.getAllRate),
    
    url(r'^startRun$', views.startRun),
    url(r'^stopRun$', views.stopRun),
    url(r'^configApplication$', views.configApplication),
    url(r'^doConfigApplication$', views.doConfigApplication),
    url(r'^showConfigApplication$', views.showConfigApplication),
    url(r'^getConfigApplicationResult$', views.getConfigApplicationResult),
    url(r'^showHistory$', views.showHistory),
    url(r'^deleteHistory$', views.deleteHistory),
    url(r'^configHistory$', views.configHistory),



    # url(r'^interfaceEdit$', views.interfaceEdit),
    # url(r'^interfaceUpdata$', views.interfaceUpdata),
    # url(r'^createMessageGroup$', views.createMessageGroup),
    # url(r'^createMessage$', views.createMessage),
    # # url(r'^insertMessageGroup$', views.insertMessageGroup),
    # url(r'^insertPacketGroup$', views.insertPacketGroup),
    # url(r'^insertMessage$', views.insertPacket),
    # url(r'^insertEth$', views.insertEth),
    # url(r'^insertEthStep2$', views.insertEthStep2),
    # url(r'^deletePacket$', views.deletePacket),
    # url(r'^deletePacketGroup$', views.deletePacketGroup),
    # url(r'^messageList$', views.messageList),
    # url(r'^downloadFile$', views.downloadFile),
    # url(r'^eth$', views.eth),
    # url(r'^arp$', views.arp),
    # url(r'^step2$', views.step2),
    # url(r'^step3$', views.step3),
    # url(r'^step4$', views.step4),
    
    url(r'^exit$', views.exit)



]