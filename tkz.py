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
    '''
    circuit	= kwargs['network'].getCircuit(kwargs['point'])
    if kwargs['voltage'] < 1000:
        return float(kwargs['voltage']) / (sqrt(3) * abs(modeSelector[kwargs['mode']](circuit)))
    else:
        pass # ДОРАБОТАТЬ для высоких напряжений

### ==============================================================================
### ================================ End tkz.py ==================================
### ==============================================================================

if __name__ == '__main__':
    a=initNetwork('test.xml')
    print ikzBeginPeriod(voltage=400, mode='threephase', point='tam', network=a)
    print ikzBeginPeriod(voltage=400, mode='twophase', point='tam', network=a)
    print ikzBeginPeriod(voltage=400, mode='onephase', point='tam', network=a)
