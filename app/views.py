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
configpacketpath = os.path.join(BASE_DIR, 'data/configpacket.xml')



#*************************************Url函数*******************************************************
def index(request):
    name = request.session.get('name',default=None)
    role_id = request.session.get('role_id',default=False)
    templateFile = "index/index.html"
    interfaces = getInterfaces()
    packetGroups = getPacketGroups()
    # print packetGroups
    params={"name":name,"interfaces":interfaces,"packetGroups":packetGroups}
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
def insertPacketGroup(request):
    name = request.POST['name']
    tree = doXml2.read_xml(configpacketpath)
    status = "error"
    if name in getPacketGroups():
        return HttpResponse(json.dumps(status, ensure_ascii=False))
    PacketGroup =  createPacketGroupElement(name)
    tree.getroot().append(PacketGroup)
    tree.write(configpacketpath)
    status = "success"
    return HttpResponse(json.dumps(status, ensure_ascii=False))


@csrf_exempt
def insertPacket(request):
    name = request.POST['name']
    packetGroupName = request.POST['messageGroupName']
    tree = doXml2.read_xml(configpacketpath)
    status = "error"
    
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==packetGroupName:
            for PacketItem in PacketGroup.findall("PacketItems/PacketItem"):
                if PacketItem.find("name").text==name:
                    status = "error"
                    return HttpResponse(json.dumps(status, ensure_ascii=False))
    PacketItem =  createPacketElement(name)
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==packetGroupName:
            PacketGroup.find("PacketItems").append(PacketItem)
            status = "success"
    tree.write(configpacketpath)
    # return HttpResponseRedirect('/app/messageList?name='+packetGroupName)  #跳转到index界面 

    return HttpResponse(json.dumps(status, ensure_ascii=False))
@csrf_exempt
def insertEth(request):
    status = saveEth(request.POST)
    status = "success"
    return HttpResponse(json.dumps(status, ensure_ascii=False))

def deletePacket(request):
    name = request.GET['packet']
    packetGroupName = request.GET['messageGroupName']
    tree = doXml2.read_xml(configpacketpath)
    status = "error"
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==packetGroupName:
            print len(PacketGroup.find("./PacketItems"))
            for PacketItem in PacketGroup.find("./PacketItems"):
                print PacketItem
                if PacketItem.find("name").text == name:
                    PacketGroup.find("PacketItems").remove(PacketItem)
                    break
            break
    tree.write(configpacketpath)
    return HttpResponseRedirect('/app/messageList?name='+packetGroupName)  #跳转到index界面 

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
    tree = doXml2.read_xml(configpacketpath)
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==name:
            for PacketItem in PacketGroup.findall("./PacketItems/PacketItem"):
                data = {}
                data['name'] = PacketItem.find('name').text
                data['smac'] = PacketItem.find('items/item/data/smac').text
                data['dmac'] = PacketItem.find('items/item/data/dmac').text
                data['ethtype'] = PacketItem.find('items/item/data/ethtype/value').text
                data['length'] = 0
                data['lostrate'] = PacketItem.find('lostrate').text
                result.append(data)
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


def eth(request):
    packet = request.GET['packet']
    packetGroupName = request.GET['packetGroupName']
    templateFile = "message/eth.html"
    eth=getEth(packet,packetGroupName)
    action = ["Fixed","Increase","Decrease"]
    params={"packetGroupName":packetGroupName,"packet":packet,"eth":eth,"action":action}
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

def getPacketGroups():
    data = []
    print "read xml",configpacketpath
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/configpacket.xml'))
    root = tree.getroot()
    for name in root.findall('./PacketGroup/name'):
        data.append(name.text)
    return data
def getInterfaces():
    data = []
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    interfaces = doXml2.find_nodes(tree, "interfaces/interface")
    for x in interfaces:
        data.append(x.attrib)
    return data
def getInterfaceByName(name):
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    interfaces = doXml2.find_nodes(tree, "interfaces/interface")
    for x in interfaces:
        if x.get("name")==name:
            return x.attrib
    return None
 
def createPacketGroupElement(name):
    PacketGroup =  doXml2.create_node("PacketGroup",{},"")
    name = doXml2.create_node("name",{},name)
    interval = doXml2.create_node("interval",{},"1000")
    cntperitval = doXml2.create_node("cntperitval",{},"0")
    loopcount = doXml2.create_node("loopcount",{},"0")
    incdec = doXml2.create_node("incdec",{},"true")
    PacketItems = doXml2.create_node("PacketItems",{},"")
    PacketGroup.append(name)
    PacketGroup.append(interval)
    PacketGroup.append(cntperitval)
    PacketGroup.append(loopcount)
    PacketGroup.append(incdec)
    PacketGroup.append(PacketItems)
    return PacketGroup

def createPacketElement(name):
    tree = doXml2.read_xml(configpacketpath)
    root = tree.getroot()
    PacketItem = root.find('./PacketGroup/PacketItems/PacketItem')
    name = doXml2.create_node("name",{},name)
    PacketItem.append(name)
    return PacketItem

def saveEth(dic):
    print dic
    tree = doXml2.read_xml(configpacketpath)
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==dic['packetGroupName']:
            for PacketItem in PacketGroup.findall("./PacketItems/PacketItem"):
                if PacketItem.find("name").text==dic["packet"]:
                    #mac
                    PacketItem.find('items/item/data/smac').text = dic["smac"]
                    PacketItem.find('items/item/data/dmac').text = dic["dmac"]
                    if dic["dmacaction"]=="Fixed":
                        PacketItem.find('items/item/data/dmac').attrib["num"] = "0"
                        PacketItem.find('items/item/data/dmac').attrib["loop"] = "0"
                    elif dic["dmacaction"]=="Increase":
                        PacketItem.find('items/item/data/dmac').attrib["num"] = dic["dmacnum"]
                        PacketItem.find('items/item/data/dmac').attrib["loop"] = dic["dmacloop"]
                    else:
                        PacketItem.find('items/item/data/dmac').attrib["num"] = "-"+dic["dmacnum"]
                        PacketItem.find('items/item/data/dmac').attrib["loop"] = "-"+dic["dmacloop"]
                    if dic["smacaction"]=="Fixed":
                        PacketItem.find('items/item/data/smac').attrib["num"] = "0"
                        PacketItem.find('items/item/data/smac').attrib["loop"] = "0"
                    elif dic["smacaction"]=="Increase":
                        PacketItem.find('items/item/data/smac').attrib["num"] = dic["smacnum"]
                        PacketItem.find('items/item/data/smac').attrib["loop"] = dic["smacloop"]
                    else:
                        PacketItem.find('items/item/data/smac').attrib["num"] = "-"+dic["smacnum"]
                        PacketItem.find('items/item/data/smac').attrib["loop"] = "-"+dic["smacloop"]
                    #vlan
                    if dic["havevlan"]=="no":
                        PacketItem.find('items/item/data').remove(PacketItem.find('items/item/data/vlans'))
    tree.write(configpacketpath)
    status = "success"
    pass
def getEth(packet,packetGroupName):
    eth={}
    tree = doXml2.read_xml(configpacketpath)
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==packetGroupName:
            for PacketItem in PacketGroup.findall("./PacketItems/PacketItem"):
                if PacketItem.find("name").text==packet:
                    print 1
                    eth["dmac"] = PacketItem.find('items/item/data/dmac').text == "" and "7A:7A:C0:A8:C8:01" or PacketItem.find('items/item/data/dmac').text
                    eth["dmacnum"] = PacketItem.find('items/item/data/dmac').attrib['num']
                    eth["dmacloop"] = PacketItem.find('items/item/data/dmac').attrib['loop']
                    if int(eth['dmacnum'])==0 and int(eth['dmacloop'])==0:
                        eth["dmacaction"] = "Fixed"
                    elif int(eth['dmacnum']) > 0:
                        eth["dmacaction"] = "Increase"
                    else:
                        eth["dmacaction"] = "Decrease"
                    eth["dmacnum"] = abs(int(eth["dmacnum"]))
                    eth["dmacloop"] = abs(int(eth["dmacloop"]))

                    eth["smac"] = PacketItem.find('items/item/data/smac').text == "" and "7A:7A:C0:A8:C8:01" or PacketItem.find('items/item/data/smac').text
                    eth["smacnum"] = PacketItem.find('items/item/data/smac').attrib['num']
                    eth["smacloop"] = PacketItem.find('items/item/data/smac').attrib['loop']
                    if int(eth['smacnum'])==0 and int(eth['smacloop'])==0:
                        eth["smacaction"] = "Fixed"
                    elif int(eth['smacnum']) > 0:
                        eth["smacaction"] = "Increase"
                    else:
                        eth["smacaction"] = "Decrease"
                    eth["smacnum"] = abs(int(eth["smacnum"]))
                    eth["smacloop"] = abs(int(eth["smacloop"]))
    print eth
    return eth
