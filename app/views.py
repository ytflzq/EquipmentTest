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
import time,datetime,random
import simplejson
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
configpacketpath = os.path.join(BASE_DIR, 'data/configpacket.xml')
demopath = os.path.join(BASE_DIR, 'data/demo.xml')



#*************************************Url函数*******************************************************
def index(request):
    name = request.session.get('name',default=None)
    templateFile = "index/index.html"
    interfaces = request.session.get('interface',default="")
    print 111
    print interfaces
    interfaces = interfaces.split(',')
    print interfaces
    # interfaces = getInterfaces()
    packetGroups = getPacketGroups()
    params={"name":name,"interfaces":interfaces,"packetGroups":packetGroups}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def allIndex(request):
    name = request.session.get('name',default=None)
    templateFile = "index/allIndex.html"
    params={"name":name}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def configApplication(request):
    templateFile = "index/configApplication.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )
def showConfigApplication(request):
    templateFile = "index/showConfigApplication.html"
    params={}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )  

def getConfigApplicationResult(request):
    file_object = open('/tmp/applicationResult')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close()
    stringHtml = str(all_the_text)
    return HttpResponse(json.dumps(stringHtml, ensure_ascii=False))
@csrf_exempt
def doConfigApplication(request):
    url = request.POST["url"]
    ip = request.POST["ip"]
    count = request.POST["count"]
    print url,ip,count
    
    status = "success"
    return HttpResponse(json.dumps(status, ensure_ascii=False))

@csrf_exempt
def getAllRate(request):
    result = []
    interfaces = request.session.get('interface',default="")
    database = Database()
    row = database.select_fetchall("""SELECT portname,totalTxBits,totalRxBits,txCountBits,rxCountBits,txRateMbps,rxRateMbps,txCountFrames,rxCountFrames,txRateFrames,rxRateFrames
        FROM interfaceStatus
         """, [])
    for x in row:
        x['portname'] = getInterfaceByport(x['portname'])
        if x['portname']=='':
            continue
        if interfaces.find(x['portname'])!=-1:
            if x['portname'].find("T")!=-1:
                # print "portname",x['portname'],"txRateFrames",x['txRateFrames']
                x['txRateMbpsPrecent'] = str(round(int(x['txRateMbps'])/10240.00*100,2))+"%"
                x['rxRateMbpsPrecent'] = str(round(int(x['rxRateMbps'])/10240.00*100,2))+"%"
                # x['rxRateFramesPrecent'] = str(round(int(x['txRateFrames'])/10240.00*100,2))+"%"
                # x['rxRateFramesPrecent'] = str(round(int(x['rxRateFrames'])/10240.00*100,2))+"%"
            else:
                x['txRateMbpsPrecent'] = str(round(int(x['txRateMbps'])/1024.00*100,2))+"%"
                x['rxRateMbpsPrecent'] = str(round(int(x['rxRateMbps'])/1024.00*100,2))+"%"
                x['rxRateFramesPrecent'] = str(round(int(x['txRateFrames'])/1024.00*100,2))+"%"
                x['rxRateFramesPrecent'] = str(round(int(x['rxRateFrames'])/1024.00*100,2))+"%"
            result.append(x)
        else:
            continue
    return HttpResponse(simplejson.dumps(result), content_type="application/json; charset=utf-8")
def startRun(request):
    interfacename= request.GET['interfacename']
    interfacename = interfacename.replace('_','/')
    print "after replace",interfacename
    filename= request.GET['filename']
    portname = getPortInterfaceByName(interfacename)
    print portname
    if portname!="":
        now = datetime.datetime.now()
        filenameNew =  time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.mktime(now.timetuple())))+".xml"
        filenameTime = time.strftime('%Y:%m:%d %H:%M:%S',time.localtime(time.mktime(now.timetuple())))
        # username = request.session.get('name',default="")
        username = "yuantingfei"
        saveHistory(filenameNew,filenameTime,username)
        os.system("cp /root/"+filename+".xml"+" /root/onekey/config/"+filenameNew)
        print "commond is:"+"/root/l2fwd_client "+portname+" /root/"+filename
        os.system("/root/l2fwd_client "+portname+" /root/"+filename+".xml > /dev/null 2>&1 &")
        return HttpResponse(simplejson.dumps("ok"), content_type="application/json; charset=utf-8")
    else:
        return HttpResponse(simplejson.dumps("fail"), content_type="application/json; charset=utf-8")
def configHistory(request):
    portname = getPortInterfaceByName(request.GET['interface'])
    filename = request.GET['filename']
    print "request.GET['interface']",request.GET['interface']
    print portname,filename,"/root/l2fwd_client "+portname+" /root/onekey/config/"+filename+" > /dev/null 2>&1 &"
    os.system("/root/l2fwd_client "+portname+" /root/onekey/config/"+filename+" > /dev/null 2>&1 &")
    return HttpResponse(simplejson.dumps("success"), content_type="application/json; charset=utf-8")
def deleteHistory(request):
    filename = request.GET['filename']
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    root  = tree.getroot()
    for x in root.findall("./history/data"):
        if x.attrib['filename']==filename:
            root.find("./history").remove(x)
    tree.write(os.path.join(BASE_DIR, 'data/config.xml'))
    return HttpResponse(simplejson.dumps("success"), content_type="application/json; charset=utf-8")
def saveHistory(filename,filenameTime,username):
    dic = {}
    dic['username'] = username
    dic['filename'] = filename
    dic['time'] = filenameTime
    data = doXml2.create_node("data",dic,"")
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    root  = tree.getroot()
    root.find("./history").append(data)
    tree.write(os.path.join(BASE_DIR, 'data/config.xml'))
    pass
def stopRun(request):
    portname = getPortInterfaceByName(request.GET['interfacename'])
    print 1111,portname
    #sprintf(killstr, "ps x|grep \"%s %s\"|grep -v grep|grep -v gdb|grep -v %d|awk '{print $1}'|xargs kill -9", argv[0], port,pid);
    os.system("""ps x | grep l2fwd_client | grep -w """ + portname + """ | grep -v grep | grep -v gdb | awk '{print $1}' | xargs kill -9 > /dev/null 2>&1""")
    return HttpResponse(simplejson.dumps("success"), content_type="application/json; charset=utf-8")
@csrf_exempt
def getRate(request):
    interface= request.GET['interface']
    interface = getPortInterfaceByName(interface)
    result = []
    dataTimes = []
    txdatas = []
    rxdatas = []
    txRateMbpsPrecent = []
    rxRateMbpsPrecent = []
    now = datetime.datetime.now()
    database = Database()
    row = database.select_fetchall("""SELECT id,portname,txRateMbps,rxRateMbps FROM interfaceStatusHistory where portname=%s ORDER BY id DESC LIMIT 10
         """, [interface])
    i=0
    # print "len(row)",len(row)
    for x in row:
        # print "id:",x['id'],"txRateMbps:",x['txRateMbps'],"rxRateMbps:",x['rxRateMbps']
        x['portname'] = getInterfaceByport(x['portname'])
        if x['portname'].find("T")!=-1:
            txRateMbpsPrecent.append(round(int(x['txRateMbps'])/10240.00*100,2))
            rxRateMbpsPrecent.append(round(int(x['rxRateMbps'])/10240.00*100,2))
        else:
            txRateMbpsPrecent.append(round(int(x['txRateMbps'])/1024.00*100,2))
            rxRateMbpsPrecent.append(round(int(x['rxRateMbps'])/1024.00*100,2))
        dt = now-datetime.timedelta(seconds=20-i) #timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
        # dataTimes.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.mktime(dt.timetuple()))))
        dataTimes.append(time.strftime('%H:%M:%S',time.localtime(time.mktime(dt.timetuple()))))
        txdatas.append(int(x['txRateMbps']))
        rxdatas.append(int(x['rxRateMbps']))
        i = i+1
    if i==0:
        dataTimes.append(0)
        txdatas.append(0)
        rxdatas.append(0)
        txRateMbpsPrecent.append(0)
        rxRateMbpsPrecent.append(0)
    txdatas = list(reversed(txdatas))
    rxdatas = list(reversed(rxdatas))
    txRateMbpsPrecent = list(reversed(txRateMbpsPrecent))
    rxRateMbpsPrecent = list(reversed(rxRateMbpsPrecent))

    result.append(dataTimes)
    result.append(txdatas)
    result.append(rxdatas)
    result.append(txRateMbpsPrecent)
    result.append(rxRateMbpsPrecent)

    return HttpResponse(simplejson.dumps(result), content_type="application/json; charset=utf-8")


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

@csrf_exempt
def insertEthStep2(request):
    status = saveEth(request.POST)
    clearData(request.POST)
    if request.POST["ethtype"]=="0x0806":
        status ="arp"
    else:
        status ="ipv4"
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
    # database = Database()
    # database.execute(""" insert into log(type,user_id,remark,time)values(%s,%s,%s,%s)""",[2,request.session['user_id'],remark,datetime.datetime.now()])
    return HttpResponseRedirect('/login')  #跳转到index界面  

def getHistory():
    data = []
    tree = doXml2.read_xml(os.path.join(BASE_DIR, 'data/config.xml'))
    datas = doXml2.find_nodes(tree, "history/data")
    for x in datas:
        data.append(x.attrib)
    return data
def showHistory(request):
    interface = request.GET['interface']
    templateFile = "index/history.html"
    data = getHistory()
    params={"data":data,"interface":interface}
    return render_to_response(
        templateFile,
        params,
        RequestContext(request)
    )

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
def arp(request):
    packet = request.GET['packet']
    packetGroupName = request.GET['packetGroupName']
    templateFile = "message/arp.html"
    arp=getArp(packet,packetGroupName)
    action = ["Fixed","Increase","Decrease"]
    havevlan =[{"key":"no","text":"No Vlan"},{"key":"svlan","text":"Single Vlan"},{"key":"dvlan","text":"Double Vlan"}]
    pri =[{"key":"0","text":"0(Best Effort)"},{"key":"1","text":"1(Background)"},{"key":"2","text":"2(Spare)"},{"key":"3","text":"3(Excellent Effort)"},\
    {"key":"4","text":"4(Controlled Load)"},{"key":"5","text":"5(Video,小于100ms latency)"},{"key":"6","text":"6(Video,小于10ms latency)"},{"key":"7","text":"7(Network Control)"}]
    vlantype = ["0x8100","0x88a8","0x9100","0x9200"]
    
    params={"packetGroupName":packetGroupName,"packet":packet,"eth":arp,"action":action,"havevlan":havevlan,"pri":pri,"vlantype":vlantype}
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
    print "from web dit:"
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
                    if dic['havevlan']!="no":
                        vlans = createVlanNode(dic)
                        PacketItem.find('items/item/data').append(vlans)
                    #type
                    PacketItem.find('items/item/data/ethtype/value').text = dic["ethtype"]
                    PacketItem.find('items/item/data/ethtype/value').text = dic["ethtype"]
    tree.write(configpacketpath)
    status = "success"
    pass
def getArp(packet,packetGroupName):
    arp = {}
    tree = doXml2.read_xml(configpacketpath)
    root = tree.getroot()
    for PacketGroup in root.findall('./PacketGroup'):
        if PacketGroup.find("name").text==packetGroupName:
            for PacketItem in PacketGroup.findall("./PacketItems/PacketItem"):
                if PacketItem.find("name").text==packet:
                    print len(PacketItem.findall("./items/item")[1].findall("incs/inc"))
                    print PacketItem.findall("./items/item")[1].findall("incs/inc")[0].find("num").text
                    pass
    return arp

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
    print "getEth:"
    print eth
    return eth
def createVlanNode(dic):
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

def clearData(dic):
    tree = doXml2.read_xml(configpacketpath)
    root = tree.getroot()
    if dic['ethtype']=='0x0806':#erp
        for PacketGroup in root.findall('./PacketGroup'):
            if PacketGroup.find("name").text==dic['packetGroupName']:
                for PacketItem in PacketGroup.findall("./PacketItems/PacketItem"):
                    if PacketItem.find("name").text==dic["packet"]:
                        arp = createArpNode()
                        if len(PacketItem.findall("./items/item"))==1:
                            PacketItem.find("./items").append(arp)
                        elif PacketItem.findall("./items/item")[1].find("protocol").text!="1":
                            item = PacketItem.findall("./items/item")[0]
                            PacketItem.find("./items").clear()
                            PacketItem.find("./items").append(item)
                            PacketItem.find("./items").append(arp)
    elif dic['ethtype'] == '':
        pass
    pass
    tree.write(configpacketpath)

def createArpNode():
    tree = doXml2.read_xml(demopath)
    root = tree.getroot()
    arp = root.find('./PacketGroup/PacketItems/arp/item')
    return arp


def downloadFile(request):  
    the_file_name='configpacket.xml'             #显示在弹出对话框中的默认的下载文件名      
    filename=configpacketpath    #要下载的文件路径  
    response=StreamingHttpResponse(readFile(filename))  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)  
    return response  
  
def readFile(filename,chunk_size=512):  
    with open(filename,'rb') as f:  
        while True:  
            c=f.read(chunk_size)  
            if c:  
                yield c  
            else:  
                break 
def getInterfaceByport(port):
    interfacepath = os.path.join(BASE_DIR, 'data/interface_phy.xml')
    tree = doXml2.read_xml(interfacepath)
    root = tree.getroot()
    interfaces = tree.findall("./workif/interface")
    for x in interfaces:
        if x.attrib['port']==port:
            return x.attrib['name']
    return ""

def getPortInterfaceByName(name):
    interfacepath = os.path.join(BASE_DIR, 'data/interface_phy.xml')
    tree = doXml2.read_xml(interfacepath)
    root = tree.getroot()
    interfaces = tree.findall("./workif/interface")
    for x in interfaces:
        if x.attrib['name']==name:
            return x.attrib['port']
    return ""