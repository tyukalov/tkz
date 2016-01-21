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
        param							= ('resist','react','r0','x0')
        if subList(kwargs, param):
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
        param		= ('highvoltage', 'lowvoltage', 'Skz', 'Ikz', 'reactance')
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
        
def initTransformerValidator(func):
    def wrapper(element, **kwargs):
        if 'Sn' in kwargs:
            try:
                kwargs['Sn']		= float(kwargs['Sn'])
                if not('scheme' in kwargs):
                    kwargs['scheme']= 'DY'
                if 'Un' in kwargs:
                    kwargs['Un']	= float(kwargs['Un'])
                else:
                    kwargs['Un']	= 400.0
                if 'Pk' in kwargs:
                    kwargs['Pk']	= float(kwargs['Pk'])
                else:
                    kwargs['Pk']	= 10000.0
                if 'uk' in kwargs:
                    kwargs['uk']	= float(kwargs['uk'])
                else:
                    kwargs['uk']	= 5.5
                if 'r0' in kwargs:
                    kwargs['r0']	= float(kwargs['r0'])
                if 'x0' in kwargs:
                    kwargs['x0']	= float(kwargs['x0'])
                func(element, **kwargs)
            except:
                print 'Invalid argument'
        else:
            print 'Invalid argument'
    return wrapper

def initBusValidator(func):
    def wrapper (element, **kwargs):
        if (subList(('lenght', 'amperage'), kwargs) or subList(('R', 'X', 'r0', 'x0'), kwargs)):
            try:
            	for x in kwargs:
                    if not(x=='amperage'):
                        kwargs[x]	= float(kwargs[x])
                func(element, **kwargs)
            except:
                print 'Invalid argument'
        else:
            print 'Unknown argument'
    return wrapper

### Инициализаторы
@initImpedanceValidator
def initImpedance(element, **kwargs):
    element.R, element.X, element.R0, element.X0 = [kwargs[x] if x in kwargs else 0 for x in element.param]
            
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

@initTransformerValidator
def initTransformer (element, **kwargs):
    element.R		= kwargs['Pk'] * ((kwargs['Un'] / kwargs['Sn'])**2)
    element.X		= ((kwargs['Un']**2)/(kwargs['Sn'] * 100)) * sqrt(kwargs['uk']**2 - (100 * kwargs['Pk'] / kwargs['Sn'])**2)
    if 'r0' in kwargs:
        element.R0=kwargs['r0']
    else:
        element.R0=element.R if kwargs['scheme']=='DY' else 3*element.R
    if 'x0' in kwargs:
        element.X0=kwargs['x0']
    else:
        element.X0=element.X if kwargs['scheme']=='DY' else 3*element.X
        
    
def initCable (element, **kwargs):
    pass

@initBusValidator
def initBus (element, **kwargs):
    if subList(('lenght', 'amperage'), kwargs):
        inquiry		= 'select resistance, reactance, zero_resistance, zero_reactance from bus where amperage="' + kwargs['amperage'] + '"'
        curs.execute(inquiry)
        [var]		= curs.fetchall()
        element.R, element.X, element.R0, element.X0	= [kwargs['lenght']*x for x in var]
    else:
        element.R, element.X, element.R0, element.X0	= [kwargs[x] for x in ('R', 'X', 'r0', 'x0')]

def initAirway (element, **kwargs):
    pass
