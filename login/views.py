# -*-coding=UTF-8-*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from util.database import Database
import os
import json
import datetime

from django.http import HttpResponse
from util import doXml2
import time,datetime,random
import simplejson
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
userpath = os.path.join(BASE_DIR, 'data/user.xml')
configpath = os.path.join(BASE_DIR, 'data/config.xml')
interfacepath = os.path.join(BASE_DIR, 'data/interface_phy.xml')
def login(request):
    templateFile = "login.html"
    params={"mes":""}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def changepwd(request):
    templateFile = "changepwd.html"
    params={"mes":""}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

@csrf_exempt
def login_action(request):
    name = request.POST['name']
    password = request.POST['password']
    # database = Database()
    users = getUsers()
    status = False
    for x in users:
        if x['name'] == name and x['password']==password:
            status = True
            request.session['name'] = name
            request.session['user_id'] = x['id']
            request.session['interface'] = x['interface']
            print x['interface']
            remark ="登录成功"
            # database.execute(""" insert into log(type,user_id,remark,time)values(%s,%s,%s,%s)""",[1,x['id'],remark,datetime.datetime.now()])
            params={"mes":"登录成功"}
            return HttpResponseRedirect('/app')  #跳转到index界面  
    if not status:
        params={"mes":"登录失败"}
        templateFile = "login.html"
        return render_to_response(
            templateFile,
            params,
            RequestContext(request)
        )
@csrf_exempt
def updatepwd(request):
    old = request.POST['old']
    new = request.POST['new']
    name = request.session.get('name',default=None)
    users = getUsers()
    status = False
    for x in users:
        if x['name'] == name and x['password']==old:
            status = True
            savepwd(name,new)
            status = "success"
            return HttpResponse(json.dumps(status, ensure_ascii=False))
    if not status:
        status = "error"
        return HttpResponse(json.dumps(status, ensure_ascii=False))
def bindInterface(request):
    name = request.session.get('name',default=None)
    tree = doXml2.read_xml(interfacepath)
    root = tree.getroot()
    interfaces = tree.findall("./workif/interface")
    result = []
    users = getUsers()
    for x in interfaces:
        ishave = False
        for y in users:
            if y['name'] == name:
                if y["interface"].find(x.attrib['name'])!=-1:
                    ishave = True
                    result.append({"ismy":"true","name":x.attrib['name']})
                    break
                else:
                    continue
            else:
                if y["interface"].find(x.attrib['name'])!=-1:
                    ishave = True
                    result.append({"ismy":"other","name":x.attrib["name"],"userName":y["name"]})
                    break
                else:
                    continue
        if not ishave:
            result.append({"ismy":"false","name":x.attrib['name']})
    # print result
    templateFile = "bindInterface.html"
    params={"interfaces":result}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
@csrf_exempt
def updateInterface(request):
    name = request.session.get('name',default=None)
    interfaces = []
    for  key,value in request.POST.items():
        clearInterface(key)
        interfaces.append(key)
    saveInterface(name,",".join(interfaces))
    request.session['interface'] = ",".join(interfaces)
    status = "success"
    return HttpResponse(json.dumps(status, ensure_ascii=False))
    
def clearInterface(interface):
    tree = doXml2.read_xml(configpath)
    users = doXml2.find_nodes(tree, "users/user")
    for x in users:
        if x.attrib['interface'].find(interface) !=-1:
            interfacelist = x.attrib['interface'].split(",")
            interfacelist.remove(interface)
            x.attrib['interface'] = ",".join(interfacelist)
    tree.write(configpath)
def saveInterface(name,interfaces):
    tree = doXml2.read_xml(configpath)
    users = doXml2.find_nodes(tree, "users/user")
    for x in users:
        if x.attrib['name']==name:
            x.attrib['interface'] = interfaces
    tree.write(configpath)
    pass
def savepwd(name,newstr):
    tree = doXml2.read_xml(configpath)
    users = doXml2.find_nodes(tree, "users/user")
    print users
    for x in users:
        if x.attrib['name'] == name:
            x.attrib['password']=newstr
    tree.write(configpath)
def getUsers():
    data = []
    tree = doXml2.read_xml(configpath)
    users = doXml2.find_nodes(tree, "users/user")
    for x in users:
        data.append(x.attrib)
    return data

def getUserById(id):
    tree = doXml2.read_xml(configpath)
    users = doXml2.find_nodes(tree, "users/user")
    for x in users:
        if x.attrib['id'] == id:
            return x.attrib
    return None
