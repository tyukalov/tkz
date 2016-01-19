# -*- coding: utf-8 -*-
from math import sqrt, log10
import sqlite3
from service import subList
### Инициализация базы данных

connect_db	= sqlite3.connect('reactance.dat')
curs 		= connect_db.cursor()

### Валидаторы параметров
def initImpedanceValidator(func):
    def wrapper(element, **kwargs):
        if subList(kwargs, ['resist','react','r0','x0']):
            try:
                for x in kwargs:
                    kwargs[x]	= float(kwargs[x])
                func(element, **kwargs)
            except:
                print 'Type of arguments must be float!'
        else:
            print 'Unknown argument!'
    return wrapper

def initSystemValidator(func):
    def wrapper(element, **kwargs):
        param	= ('highvoltage', 'lowvoltage', 'Skz', 'Ikz', 'reactance')
        if subList(kwargs, param):
            for x in param:
                if x in kwargs:
                    try:
                        kwargs[x]	= float(kwargs[x])
                    except:
                        print 'Type of arguments must be float!'
            if not('highvoltage' in kwargs):
                kwargs['highvoltage']	= 10000
            if not('lowvoltage' in kwargs):
                kwargs['lowvoltage']	= 400
            func(element, **kwargs)
        else:
            print 'Unknown argument!'
    return wrapper
        

### Инициализаторы
@initImpedanceValidator
def initImpedance(element, **kwargs):
    param			= ('resist', 'react', 'r0', 'x0')
    element.R, element.X, element.R0, element.X0 = [kwargs[x] if x in kwargs else 0 for x in param]
            
@initSystemValidator
def initSystem (element, **kwargs):
    element.R, element.R0, element.X0	= 0, 0, 0
    if 'reactance' in kwargs:
        element.X						= kwargs['reactance']
    elif 'Skz' in kwargs: 
        element.X						= (kwargs['lowvoltage'] ** 2) / kwargs['Skz']
    elif 'Ikz' in kwargs:
        element.X						= (kwargs['lowvoltage'] ** 2) / (sqrt(3) * kwargs['Ikz'] * kwargs['highvoltage'])
    else:
        element.X						= 0

def initTransformer (element, **kwargs):
    pass

def initCable (element, **kwargs):
    pass

def initBus (element, **kwargs):
    pass

def initAirway (element, **kwargs):
    pass
