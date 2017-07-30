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
demopath = os.path.join(BASE_DIR, 'data/demo.xml')



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
            for PacketItem in PacketGroup.find("./PacketItems"):
                if PacketItem.find("name").text == name:
                    PacketGroup.find("PacketItems").remove(PacketItem)
                    break
            break
    tree.write(configpacketpath)
    return HttpResponseRedirect('/app/messageList?name='+packetGroupName)  #跳转到index界面 
def deletePacketGroup(request):
    packetGroupName = request.GET['messageGroupName']
    tree = doXml2.read_xml(configpacketpath)
    status = "error"
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==packetGroupName:
            root.remove(PacketGroup)
            break
    tree.write(configpacketpath)
    return HttpResponseRedirect('/app')  #跳转到index界面 

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
    interface = request.GET['name']
    templateFile = "index/rate.html"
    params={"interface":interface}
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
    havevlan =[{"key":"no","text":"No Vlan"},{"key":"svlan","text":"Single Vlan"},{"key":"dvlan","text":"Double Vlan"}]
    pri =[{"key":"0","text":"0(Best Effort)"},{"key":"1","text":"1(Background)"},{"key":"2","text":"2(Spare)"},{"key":"3","text":"3(Excellent Effort)"},\
    {"key":"4","text":"4(Controlled Load)"},{"key":"5","text":"5(Video,小于100ms latency)"},{"key":"6","text":"6(Video,小于10ms latency)"},{"key":"7","text":"7(Network Control)"}]
    vlantype = ["0x8100","0x88a8","0x9100","0x9200"]
    
    params={"packetGroupName":packetGroupName,"packet":packet,"eth":eth,"action":action,"havevlan":havevlan,"pri":pri,"vlantype":vlantype}
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
    tree = doXml2.read_xml(demopath)
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
                    for vlans in PacketItem.findall('items/item/data/vlans'):
                        PacketItem.find('items/item/data').remove(vlans)
                    vlans = creaeVlanNode(dic)
                    PacketItem.find('items/item/data').append(vlans)
                    #type
                    PacketItem.find('items/item/data/ethtype/value').text = dic["ethtype"]
                    PacketItem.find('items/item/data/ethtype/value').text = dic["ethtype"]
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
                    #mac
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

                    #vlan
                    if len(PacketItem.findall('items/item/data/vlans'))==0:
                        eth["havevlan"] = "no"
                    else:
                        if len(PacketItem.findall('items/item/data/vlans/vlan'))==1:
                            eth["havevlan"] = "svlan"
                            eth["svlantype"] = PacketItem.find('items/item/data/vlans/vlan/type').text
                            eth["svlanpri"] = PacketItem.find('items/item/data/vlans/vlan/data/pri').text
                            eth["svlancfi"] = PacketItem.find('items/item/data/vlans/vlan/data/cfi').text
                            eth["svlan"] = PacketItem.find('items/item/data/vlans/vlan/data/id').text
                            eth["svlannum"] = PacketItem.find('items/item/data/vlans/vlan/data').attrib['num']
                            eth["svlanloop"] = PacketItem.find('items/item/data/vlans/vlan/data').attrib['loop']
                            if int(eth['svlannum'])==0 and int(eth['svlanloop'])==0:
                                eth["svlanaction"] = "Fixed"
                            elif int(eth['svlannum']) > 0:
                                eth["svlanaction"] = "Increase"
                            else:
                                eth["svlanaction"] = "Decrease"
                            eth["svlannum"] = abs(int(eth["svlannum"]))
                            eth["svlanloop"] = abs(int(eth["svlanloop"]))
                        else:
                            eth["havevlan"] = "dvlan"
                            eth["morevlans"] = PacketItem.find('items/item/data/vlans/morevlans').text

                            eth["svlantype"] = PacketItem.find('items/item/data/vlans/vlan/type').text
                            eth["svlanpri"] = PacketItem.find('items/item/data/vlans/vlan/data/pri').text
                            eth["svlancfi"] = PacketItem.find('items/item/data/vlans/vlan/data/cfi').text
                            eth["svlan"] = PacketItem.find('items/item/data/vlans/vlan/data/id').text
                            eth["svlannum"] = PacketItem.find('items/item/data/vlans/vlan/data').attrib['num']
                            eth["svlanloop"] = PacketItem.find('items/item/data/vlans/vlan/data').attrib['loop']
                            if int(eth['svlannum'])==0 and int(eth['svlanloop'])==0:
                                eth["svlanaction"] = "Fixed"
                            elif int(eth['svlannum']) > 0:
                                eth["svlanaction"] = "Increase"
                            else:
                                eth["svlanaction"] = "Decrease"
                            eth["svlannum"] = abs(int(eth["svlannum"]))
                            eth["svlanloop"] = abs(int(eth["svlanloop"]))

                            eth["dvlantype"] = PacketItem.findall('items/item/data/vlans/vlan/type')[1].text
                            eth["dvlanpri"] = PacketItem.findall('items/item/data/vlans/vlan/data/pri')[1].text
                            eth["dvlancfi"] = PacketItem.findall('items/item/data/vlans/vlan/data/cfi')[1].text
                            eth["dvlan"] = PacketItem.findall('items/item/data/vlans/vlan/data/id')[1].text
                            eth["dvlannum"] = PacketItem.findall('items/item/data/vlans/vlan/data')[1].attrib['num']
                            eth["dvlanloop"] = PacketItem.findall('items/item/data/vlans/vlan/data')[1].attrib['loop']
                            if int(eth['dvlannum'])==0 and int(eth['dvlanloop'])==0:
                                eth["dvlanaction"] = "Fixed"
                            elif int(eth['dvlannum']) > 0:
                                eth["dvlanaction"] = "Increase"
                            else:
                                eth["dvlanaction"] = "Decrease"
                            eth["dvlannum"] = abs(int(eth["dvlannum"]))
                            eth["dvlanloop"] = abs(int(eth["dvlanloop"]))
                    
                    #type
                    eth["ethtype"] =PacketItem.find('items/item/data/ethtype/value').text
    print "getEth"
    print eth
    return eth
def creaeVlanNode(dic):
    tree = doXml2.read_xml(demopath)
    root = tree.getroot()
    vlanss = root.findall('./PacketGroup/PacketItems/vlans')
    if dic["havevlan"]=="dvlan":
        vlans = vlanss[0]
        vlans.find("./morevlans").text = dic["morevlans"]
        vlans.find("./vlan/type").text = dic['svlantype']
        vlans.find("./vlan/data/pri").text = dic['svlanpri']
        vlans.find("./vlan/data/cfi").text = dic['svlancfi']
        vlans.find("./vlan/data/id").text = dic['svlan']
        if dic["svlanaction"]=="Fixed":
            vlans.find('./vlan/data').attrib["num"] = "0"
            vlans.find('./vlan/data').attrib["loop"] = "0"
        elif dic["dmacaction"]=="Increase":
            vlans.find('./vlan/data').attrib["num"] = dic["svlannum"]
            vlans.find('./vlan/data').attrib["loop"] = dic["svlanloop"]
        else:
            vlans.find('./vlan/data').attrib["num"] = "-"+dic["svlannum"]
            vlans.find('./vlan/data').attrib["loop"] = "-"+dic["svlanloop"]
        vlans.findall("./vlan/type")[1].text = dic['dvlantype']
        vlans.findall("./vlan/data/pri")[1].text = dic['dvlanpri']
        vlans.findall("./vlan/data/cfi")[1].text = dic['dvlancfi']
        vlans.findall("./vlan/data/id")[1].text = dic['dvlan']
        if dic["dvlanaction"]=="Fixed":
            vlans.findall('./vlan/data')[1].attrib["num"] = "0"
            vlans.findall('./vlan/data')[1].attrib["loop"] = "0"
        elif dic["dmacaction"]=="Increase":
            vlans.findall('./vlan/data')[1].attrib["num"] = dic["dvlannum"]
            vlans.findall('./vlan/data')[1].attrib["loop"] = dic["dvlanloop"]
        else:
            vlans.findall('./vlan/data')[1].attrib["num"] = "-"+dic["dvlannum"]
            vlans.findall('./vlan/data')[1].attrib["loop"] = "-"+dic["dvlanloop"]
    else:
        vlans = vlanss[1]
        vlans.find("./vlan/type").text = dic['svlantype']
        vlans.find("./vlan/data/pri").text = dic['svlanpri']
        vlans.find("./vlan/data/cfi").text = dic['svlancfi']
        vlans.find("./vlan/data/id").text = dic['svlan']
        if dic["svlanaction"]=="Fixed":
            vlans.find('./vlan/data').attrib["num"] = "0"
            vlans.find('./vlan/data').attrib["loop"] = "0"
        elif dic["smacaction"]=="Increase":
            vlans.find('./vlan/data').attrib["num"] = dic["svlannum"]
            vlans.find('./vlan/data').attrib["loop"] = dic["svlanloop"]
        else:
            vlans.find('./vlan/data').attrib["num"] = "-"+dic["svlannum"]
            vlans.find('./vlan/data').attrib["loop"] = "-"+dic["svlanloop"]
    return vlans
