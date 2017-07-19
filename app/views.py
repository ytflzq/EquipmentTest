# -*-coding=UTF-8-*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import datetime
from util.database import Database
from django.http import HttpResponse
from util import doXml2
import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




#*************************************Url函数*******************************************************
def index(request):
    name = request.session.get('name',default=None)
    role_id = request.session.get('role_id',default=False)
    templateFile = "index/index.html"
    interfaces = getInterfaces()
    messages = getMessages()
    params={"name":name,"interfaces":interfaces,"messages":messages}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def interfaceEdit(request):
    interface = getInterfaceByName(request.GET['name'])
    templateFile = "index/interfaceEdit.html"
    params={"interface":interface}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def importFile(request):
    templateFile = "index/importFile.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
@csrf_exempt
def uploadFile(request):
    templateFile = "index/success.html"
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        file =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not file:  
            status = "fail"
            params={"status":status}
            return render_to_response(
                templateFile,
                params,
                RequestContext(request)
            )
        destination = open(os.path.join(BASE_DIR,"data",file.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        for chunk in file.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  
        status = "success"
        params={"status":status}
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
@csrf_exempt
def insertMessageGroup(request):
    name = request.POST['name']
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    messages = doXml2.find_nodes(tree, "messages")
    message = doXml2.find_nodes(tree, "messages/message")
    for x in message:
        if x.attrib['name']==name:
            status = "error"
            return HttpResponse(json.dumps(status, ensure_ascii=False))
    for x in messages:
        x.append(doXml2.create_node("message",{"name":name},""))
    tree.write(os.path.join(BASE_DIR, 'data/config.xml'))
    status = "success"
    return HttpResponse(json.dumps(status, ensure_ascii=False))

@csrf_exempt
def insertMessage(request):
    name = request.POST['name']
    messageGroupName = request.POST['messageGroupName']
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    message = doXml2.find_nodes(tree, "messages/message")
    status = "error"
    dit = {"name":name,"id":"1","length":"0","lost":"12","sou_mac":"","des_mac":"","type":"","ip":""}
    for x in message:
        if x.attrib['name']==messageGroupName:
            x.append(doXml2.create_node("mes",dit,""))
            status = "success"
    tree.write(os.path.join(BASE_DIR, 'data/config.xml'))
    
    return HttpResponse(json.dumps(status, ensure_ascii=False))
@csrf_exempt
def interfaceUpdata(request):
    status = 0
    name = request.POST['name']
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    interfaces = doXml2.find_nodes(tree, "interfaces/interface")
    for x in interfaces:
        if x.get("name")==name:
            x = prepareData(x,request.POST)
            status = 1
    tree.write(os.path.join(BASE_DIR, 'data/config.xml'))
    templateFile = "index/interfaceEdit.html"
    interface = getInterfaceByName(request.POST['name'])
    templateFile = "index/interfaceEdit.html"
    params={"interface":interface,"status":status}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )


def rate(request):
    templateFile = "index/rate.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def messageList(request):
    name = request.GET['name']
    result = []
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    message = doXml2.find_nodes(tree, "messages/message")
    for x in message:
        if x.attrib['name']==name:
            for mes in x.iter('mes'):
                print mes.attrib
                result.append(mes.attrib)
            break
    templateFile = "message/messageList.html"
    params={"message":name,"list":result}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def createMessageGroup(request):
    templateFile = "message/createMessageGroup.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def createMessage(request):
    message = request.GET['message']
    templateFile = "message/createMessage.html"
    params={"message":message}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
    pass
def exit(request):
    remark = "注销"
    database = Database()
    database.execute(""" insert into log(type,user_id,remark,time)values(%s,%s,%s,%s)""",[2,request.session['user_id'],remark,datetime.datetime.now()])
    del request.session['name']
    del request.session['user_id']
    return HttpResponseRedirect('/login')  #跳转到index界面  


def step1(request):
    templateFile = "message/step1.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def step2(request):
    templateFile = "message/step2.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def step3(request):
    templateFile = "message/step3.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

def step4(request):
    templateFile = "message/step4.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
#******************************************处理函数**************************************************

def prepareData(node,ditData):
    for  key,value in ditData.items():
        node.set(str(key),str(value))
    return node

def getInterfaces():
    data = []
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    interfaces = doXml2.find_nodes(tree, "interfaces/interface")
    for x in interfaces:
        data.append(x.attrib)
    return data
def getMessages():
    data = []
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    messages = doXml2.find_nodes(tree, "messages/message")
    for x in messages:
        data.append(x.attrib)
    return data
def getInterfaceByName(name):
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    interfaces = doXml2.find_nodes(tree, "interfaces/interface")
    for x in interfaces:
        if x.get("name")==name:
            return x.attrib
    return None
 
