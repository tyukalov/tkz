# -*- coding: utf-8 -*-
### ================================ models.py ===================================
### В файле описываются "интерфейсные модели" электрических сетей, то есть функции
### обработки представлений электрической сети, которые задаются пользователями
### приложения.
###
###
### Author:			Igor Tyukalov
### License:			BSD
### Date:			29.01.2016
###
### ==============================================================================



import xml.etree.ElementTree as ET
from element import *

### Интерфейс с xml-представлением электрической сети

tags	= {'network':Network, 'impedance':Impedance, 'system':System, 'transformer':Transformer, 'cable':Cable, 'bus':Bus, 'reactor':Reactor}



def getcircuit (filename):
    tree	= ET.parse(filename)
    return	tree.getroot()	

# Валидатор тэгов
def tag_validate (var):
    var0			= var.tag
    if not(var0 in tags):
        result		= False
    else:
        result		= True
    for x in var:
        result		= result and tag_validate(x)
    return result

# Инициализатор класса Network
def initNetwork(filename):
    root		= getcircuit(filename)
    if tag_validate(root):
        [root]	= root
        return initNetworkEx(root)
    else:
        raise NetworkError

def initNetworkEx (root):
    elem	= root.tag
    param	= root.attrib
    if 'name' in param:
        mname	= param.pop('name')
    else:
        mname	= 'Unknown'
    if list(root):
        return Network(tags[elem](**param), name=mname, tail=[initNetworkEx(x) for x in root])
    else:
        return Network(tags[elem](**param), name=mname)

### ==============================================================================
### ================================ End models.py ===============================
### ==============================================================================

if __name__ == '__main__':
    a=initNetwork('test.xml')
    print a
    print a.getCircuit('tam')
    x=0
    for m in a.getCircuit('tam'):
        x=x+m.R
    print x
