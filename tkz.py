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
    result		= Impedance()
    for x in circuit:
        result += x
    return result.fullZ0 / 3
def twoPhase(circuit):
    result		= Impedance()
    for x in circuit:
        result += x
    return (2 / sqrt(3)) * result.fullZ
def threePhase(circuit):
    result		= Impedance()
    for x in circuit:
        result += x
    return  result.fullZ
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
    circuit	= kwargs['network'].getCircuit(kwargs['point'])
    Z				= modeSelector[kwargs['mode']](circuit)
    if kwargs['voltage'] < 1000:
        ### РД 153-34.0-20.527-98
        if kwargs['volume']=='max':
            return  float(kwargs['voltage']) / (sqrt(3) * abs(Z))
        else:
            var			= Impedance()
            for x in circuit:
                var		+= x
            i0			= kwargs['voltage'] / (sqrt(3) * abs(var.Z))
            aZ			= abs(Z)
            Ks			= 0.6 - 2.5 * aZ + 0.114 * sqrt(1000 * aZ) - 0.13 * ((1000 * aZ)**(1 / float(3)))
            Rd			= Impedance(resist=sqrt(abs((((kwargs['voltage'] / (i0 * Ks))**2)/3) - (var.X)**2)) - var.R)
            circuit_d	= [Rd] + circuit
            return kwargs['voltage'] / (sqrt(3) * abs(modeSelector[kwargs['mode']](circuit_d)))
    else:
        c=1.1 if kwargs['volume']=='max' else 1.0
        return c * kwargs['voltage'] / (sqrt(3) * Z.imag)

### ==============================================================================
### ================================ End tkz.py ==================================
### ==============================================================================

if __name__ == '__main__':
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
