# -*-coding=UTF-8-*-
import datetime
import time
import os
import xml.etree.cElementTree as ET

#讲一个字典保存进node的属性
def prepareData(node,ditData):
    for  key,value in ditData.items():
        node.set(str(key),str(value))

def saveFive(tree,path):
    tree.write(path)
if __name__ == '__main__':
    try: 
      import xml.etree.cElementTree as ET 
    except ImportError: 
      import xml.etree.ElementTree as ET 
    import sys 
    try: 
      tree = ET.parse("country.xml")     #打开xml文档 
      #root = ET.fromstring(country_string) #从字符串传递xml 
      root = tree.getroot()         #获得root节点  
    except Exception, e: 
      print "Error:cannot parse file:country.xml."
      sys.exit(1) 
    print root.tag, "---", root.attrib  
    for child in root: 
      print child.tag, "---", child.attrib 
      
    print "*"*10
    print root[0][1].text   #通过下标访问 
    print root[0].tag, root[0].text 
    print "*"*10
      
    for country in root.findall('country'): #找到root节点下的所有country节点 
      rank = country.find('rank').text   #子节点下节点rank的值 
      name = country.get('name')      #子节点下属性name的值 
      print name, rank 
         
    #修改xml文件 
    for country in root.findall('country'): 
      rank = int(country.find('rank').text) 
      d = {"name":"a","py":"ccc"}
      prepareData(country,d)
    tree.write('country.xml') 

