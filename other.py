# -*- coding: utf-8 -*-
### ===================================== other.py ========================================
###
### Author:			Igor Tyukalov
### License:		BSD
### Date:			09.02.2016
### ========================================================================================

from math import sqrt, sin, cos, tan, acos
from element import *
from models import initNetwork # УБРАТЬ В РЕЛИЗЕ. Только для теста


def voltageLoss(**kwargs):
    """
    Расчёт потерь напряжения в электрических сетях.
    Параметры:
    network		- экземпляр класса Network;
    point		- расчётная точка;
    voltage		- номинальное напряжение, В;
    amperage	- расчётный ток, А;
    power		- активная мощность потребителя, Вт;
    cos			- коэффициент мощности;
    mode		- режим (onephase, threephase)
    """
    net			= kwargs.get('network')
    cos			= kwargs.get('cos')
    Z			= net.getResistance(kwargs['point'])
    if Z:
        R		= Z.R
        X		= Z.X
    else:
        return False
    amper	= kwargs.get('amperage')
    if amper:
        if kwargs['mode']=='onephase':
            K	= 200 * sqrt(3) * amper / kwargs['voltage']
        elif kwargs['mode']=='threephase':
            K	= 100 * sqrt(3) * amper / kwargs['voltage']
        return K * (R * cos + X * (sin(acos(cos))))
    P			= kwargs.get('power')
    if P:
        Q		= P * tan(acos(cos))
        if kwargs['mode']=='onephase':
            K	= 600.0 / (kwargs['voltage'] ** 2)
        elif kwargs['mode']=='threephase':
            K	= 100.0 / (kwargs['voltage'] ** 2)
        return K * (P * R + Q * X)
    return False

### ================================= End other.py ========================================

if __name__ == '__main__':
    a=initNetwork('test.xml')
    b=voltageLoss(network=a, voltage=380, mode='onephase', cos=0.92, power=1000, point='tut')
    print b
