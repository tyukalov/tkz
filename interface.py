# -*- coding: utf-8 -*-
from math import sqrt, log10, pi
import sqlite3
from service import subList
### Инициализация базы данных

connect_db	= sqlite3.connect('reactance.dat')
curs 		= connect_db.cursor()

### Некоторые параметры
### Соотношения Х0/Х1 для воздушных линий (РД 153-34.0-20.527-98 Табл. 4.2)
airwayX0X1		= {
    'OCWR':3.5,					# Одноцепная линия без заземленных тросов
    'OCSR':3.0,					# То же, со стальными заземленными тросами
    'OCR':2.0,					# То же, с заземленными тросами из хорошопроводящих материалов
    'TCWR':5.5,					# Двухцепная линия без заземленных тросов
    'TCSR':4.7,					# То же, со стальными заземленными тросами
    'TCR':3.0					# То же, с заземленными тросами из хорошопроводящих материалов
    }

### Удельное сопротивление материала (ГОСТ 28240-93 Прил. 3)
ro				= {'cu':0.0178, 'al':0.02994}

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
                kwargs['highvoltage']	= 10000.0
            if not('lowvoltage' in kwargs):
                kwargs['lowvoltage']	= 400.0
            func(element, **kwargs)
        else:
            print 'Unknown argument!'
    return wrapper
        
def initTransformerValidator(func):
    """
    Параметры трансформаторов. Все единицы - собственные.
    Значения:
    Pk - потери короткого замыкания в трансформаторе, Вт;
    Sn - номинальная мощность трансформатора, Вт;
    Un - номинальное напряжение трансформатора, В;
    uk - напряжение короткого замыкания трансформатора, %;
    scheme - схема соединения обмоток (YY, DY)
    """
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
    """
    Параметры:
    amperage - расчётный ток, А;
    R, X, r0, x0 - паспортные удельные сопротивления, Ом/м;
    lenght - длина, м;
    """
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

def initCableValidator(func):
    """
    Параметры:
    lenght - длина, м;
    cross_section - сечение, мм2;
    material - материал, (al, cu)
    types - материал оболочки, (aluminium_shell, plumbum_shell, shell, steel_shell)
    cores - число жил
    R, X - справочные значения удельных сопротивлений, Ом/м;
    """
    def wrapper(element, **kwargs):
        required	= ('material', 'cross_section', 'lenght')
        if subList(required, kwargs):
            try:
                kwargs['lenght']							= float(kwargs['lenght'])
                if not('types' in kwargs): kwargs['types'] 	= 'shell'
                if not('cores' in kwargs): kwargs['cores'] 	= '3'
                if 'R' in kwargs: kwargs['R']				= float(kwargs['R'])
                if 'X' in kwargs: kwargs['X']				= float(kwargs['X'])
                if 'r0' in kwargs: kwargs['r0']				= float(kwargs['r0'])
                if 'x0' in kwargs: kwargs['x0']				= float(kwargs['x0'])
                func(element, **kwargs)
            except:
                print 'Invalid argument'
        else:
            print 'Invalid argument'
    return wrapper

def initAirwayValidator(func):
    """
    Параметры:
    lenght - длина, м;
    cross_section - сечение, мм2";
    material - материал, (al, cu);
    types - тип линии;
    a - расстояние между проводниками, м;
    R,X,r0,x0 - справочные данные;
    """
    def wrapper (element, **kwargs):
        if ('lenght' in kwargs) and (('material' in kwargs) or subList(('R','X','r0','x0'), kwargs)) and (('X' in kwargs) or ('a' in kwargs)):
            if not('types' in kwargs):
                kwargs['types']			= 'TCWR'
            try:
            	for x in ('lenght','cross_section','a','R','X','r0','x0'):
                    if x in kwargs:
                        kwargs[x]		= float(kwargs[x])
                func(element, **kwargs)
            except:
                print 'Invalid argument'
        else:
            print 'Invalid argument'
    return wrapper

def initReactorValidator(func):
    """
    Параметры:
    L - индуктивность, Гн;
    М - взаимная индуктивность, Гн;
    In- номинальный ток, А;
    dP- потери мощности, Вт;
    X - справочное значение
    """
    def wrapper (element, **kwargs):
        if subList(('In', 'dP'), kwargs) and (('X' in kwargs) or subList(('L','M'), kwargs)):
            try:
                for x in kwargs:
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
    element.R, element.X, element.R0, element.X0 = [kwargs[x] if x in kwargs else 0 for x in ('resist','react','r0','x0')]
            
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
        
    
@initCableValidator
def initCable (element, **kwargs):
    param				= ('R','X','r0','x0')
    if not(subList(param, kwargs)):
        try:
            inquiry		= 'select resistance, reactance, zero_resistance, zero_reactance from cable where material="' + kwargs['material'] + '" and type="' + kwargs['types'] + '" and cross_section="' + kwargs['cross_section'] + '" and cores="' + kwargs['cores'] + '"'
            curs.execute(inquiry)
            [var]		= curs.fetchall()
            var			= dict(zip(param,map(lambda x: x / 1000, var)))
        except:
            print 'Invalid argument'
    element.R, element.X, element.R0, element.X0	= [x*kwargs['lenght'] for x in map(lambda x: kwargs[x] if x in kwargs else var[x], param)]
        

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

@initReactorValidator
def initReactor (element, **kwargs):
    element.R					= kwargs['dP'] / (kwargs['In'] ** 2)
    if 'X' in kwargs:
        element.X				= kwargs['X']
    else:
        element.X				= 100 * pi * (kwargs['L'] - kwargs['M'])
    element.R0					= element.R
    element.X0					= element.X
    
@initAirwayValidator
def initAirway (element, **kwargs):
    if 'R' in kwargs:
        R					= kwargs['R']
    else:
        R					= ro[kwargs['material']] / kwargs['cross_section']
    if 'X' in kwargs:
        X					= kwargs['X']
    else:
        X					= 0.000145 * log10(1000 * kwargs['a'] / (sqrt(kwargs['cross_section'] / pi)))
    if 'r0' in kwargs:
        R0					= kwargs['r0']
    else:
        R0					= 0.00015 + R   # РД 153-34.0-20.527-98 п.6.3.2.1
    if 'x0' in kwargs:
        X0					= kwargs['x0']
    else:
        X0					= airwayX0X1[kwargs['types']] * X
    element.R, element.X, element.R0, element.X0	= [kwargs['lenght'] * x for x in (R,X,R0,X0)]
