# -*- coding: utf-8 -*-
### ================================ tkz.py ======================================
### В файле собраны функции для расчётов токов короткого замыкания
###
###
### Author:			Igor Tyukalov
### License:			BSD
### Date:			29.01.2016
###
### ==============================================================================

from element import *
from models import initNetwork # УБРАТЬ В РЕЛИЗЕ. Только для теста
from math import sqrt

### ---------------------------------------------------
### Расчётов начального периодического значения тока КЗ
### ---------------------------------------------------

# Служебные функции и данные
def onePhase(circuit):
    return circuit.fullZ0 / 3
def twoPhase(circuit):
    return (2 / sqrt(3)) * circuit.fullZ
def threePhase(circuit):
    return  circuit.fullZ
modeSelector	= {'onephase':onePhase,
                   'twophase':twoPhase,
                   'threephase':threePhase}
    
# Расчётная функция
def ikzBeginPeriod(**kwargs):
    '''
    Параметры:
    voltage - напряжение, В;
    network - объект класса Network;
    mode    - режим, (onephase, twophase, threephase);
    point   - точка КЗ;
    volume  - уровень (min,max)
    '''
    circuit	= kwargs['network'].getResistance(kwargs['point'])
    Z				= modeSelector[kwargs['mode']](circuit)
    if kwargs['voltage'] < 1000:
        ### РД 153-34.0-20.527-98
        if kwargs['volume']=='max':
            return  float(kwargs['voltage']) / (sqrt(3) * Z.Z)
        else:
            i0			= kwargs['voltage'] / (sqrt(3) * Z.Z)
            aZ			= Z.Z
            Ks			= 0.6 - 2.5 * aZ + 0.114 * sqrt(1000 * aZ) - 0.13 * ((1000 * aZ)**(1 / float(3)))
            Rd			= Impedance(resist=sqrt(abs((((kwargs['voltage'] / (i0 * Ks))**2)/3) - (var.X)**2)) - var.R)
            circuit_d	= modeSelector[kwargs['mode']](Rd + circuit)
            return kwargs['voltage'] / (sqrt(3) * circuit_d.Z)
    else:
        c=1.1 if kwargs['volume']=='max' else 1.0
        return c * kwargs['voltage'] / (sqrt(3) * Z.imag)

### ==============================================================================
### ================================ End tkz.py ==================================
### ==============================================================================

if __name__ == '__main__':
    try:
        a=initNetwork('test.xml')
        # print ikzBeginPeriod(voltage=400, volume='max', mode='threephase', point='tam', network=a)
        # print ikzBeginPeriod(voltage=400, volume='max', mode='twophase', point='tam', network=a)
        # print ikzBeginPeriod(voltage=400, volume='max', mode='onephase', point='tam', network=a)
        # print ikzBeginPeriod(voltage=400, volume='min', mode='threephase', point='tam', network=a)
        # print ikzBeginPeriod(voltage=400, volume='min', mode='twophase', point='tam', network=a)
        # print ikzBeginPeriod(voltage=400, volume='min', mode='onephase', point='tam', network=a)

        print ikzBeginPeriod(voltage=10000, volume='max', mode='threephase', point='tam', network=a)
        print ikzBeginPeriod(voltage=10000, volume='max', mode='twophase', point='tam', network=a)
        print ikzBeginPeriod(voltage=10000, volume='max', mode='onephase', point='tam', network=a)
        print ikzBeginPeriod(voltage=10000, volume='min', mode='threephase', point='tam', network=a)
        print ikzBeginPeriod(voltage=10000, volume='min', mode='twophase', point='tam', network=a)
        print ikzBeginPeriod(voltage=10000, volume='min', mode='onephase', point='tam', network=a)
    except InvalidArgument as X:
        print(X)
    except DBError as X:
        print X
