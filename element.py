# -*- coding: utf-8 -*-
### ===================================== element.py ========================================
###
### В модуле описаны основные классы элементов электрических цепей
###
### Author:			Igor Tyukalov
### License:		BSD
### Date:			08.05.2015
### ========================================================================================

from interface import *



### Селектор выбора функции-инициализатора. 
selector							= {'Impedance':initImpedance,
                                       'System':initSystem,
                                       'Transformer':initTransformer,
                                       'Cable':initCable,
                                       'Bus':initBus,
                                       'Reactor':initReactor,
                                       'Airway':initAirway}

### Базовый класс электрического сопротивления цепи
class Impedance:
    """
    Класс описывает электрическое сопротивление. Является базовым
    для всех элементов. Содержит атрибуты активного, реактивного
    и полного сопротивления. Атрибут fullZ является внутренним
    (на данном этапе) и используется только в методах класса.
    Методы, изменяющие активное и реактивное сопротивления
    класса приводят к обновлению всех атрибутов. Непосредственное
    изменение атрибута Z на данный момент не предусмотрено. Это
    связано с тем, что базовый класс не предполагается использовать
    непосредственно, а методы дочерних классов определены так,
    что оперировать с абсолютным значением полного сопротивления
    они не будут.
    """
    type							= 'Impedance'
    parent							= 'Impedance'
    R,X,R0,X0,Z,Z0,fullZ, fullZ0	= 8*[None]

    def __init__ (self, **kwargs):
        selector[self.type](self, **kwargs)
        self.fullZ0	= complex((2 * self.R + self.R0), (2 * self.X + self.X0))
        self.Z0		= abs(self.fullZ0)
        self.fullZ	= complex(self.R, self.X)
        self.Z		= abs(self.fullZ)
        
    def __add__ (self, other):
        if self.fullZ and self.fullZ0 and other.fullZ and other.fullZ0:
            var			= self.fullZ + other.fullZ
            var0		= self.fullZ0 + other.fullZ0
            return Impedance(var.real, var.imag, var0.real, var0.imag)
        else:
            print 'Uninizialized instance!'

    def __str__ (self):
        return '<Impedance: R = %s, X = %s, Z = %s, Z0 = %s >'%(self.R, self.X, self.Z, self.Z0)
    
### Класс сопротивления системы
class System(Impedance):
    """
    Класс сопротивления системы.
    Все единицы - собственные (амперы, вольты, омы)
    """
    type		= 'System'


### Класс сопротивления трансформаторов
class Transformer (Impedance):
    type		= 'Transformer'


### Класс кабелей
class Cable (Impedance):
    type		= 'Cable'


### Класс шинопроводов
class Bus (Impedance):
    type		= 'Bus'
    


### Класс воздушных линий
class Airway (Impedance):
    type		= 'Airway'

### Класс реакторов
class Reactor (Impedance):
    type		= 'Reactor'

### Класс электрической сети
class Network:
    """
    Класс описывает радиальную электрическую сеть с одним источником питания.
    Представляет собой головной элемент head типа Impedance (и дочерних)
    и список tail, состоящий из элементов типа Network
    """
    type		= 'Network'

    def __init__ (self, head, **kwargs):
        if head.parent == 'Impedance':
            self.head			= head
        else:
            raise InvalidArgumentType
        if 'name' in kwargs:
            self.name			= kwargs['name']
        else:
            self.name			= 'Unknown'
        if 'tail' in kwargs:
            lst					= kwargs['tail']
            for x in lst:
                if not(x.type == 'Network'):
                    raise InvalidArgumentType
            self.tail			= lst
        else:
            self.tail			= []

    def __add__ (self, other):
        return Network(self.head, tail=[other] + self.tail, name=self.name)

    def getCircuit(self, name):
        if self.name == name:
            return [self.head]
        else:
            for x in self.tail:
                var			= x.getCircuit(name)
                if var:
                    return [self.head] + var
        return False
        
### -----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    a=Network(Impedance(),tail=[Network(Impedance()), Network(Impedance(),tail=[Network(Impedance()), Network(Impedance(),tail=[Network(Impedance(resist='10'), name='tut'), Network(Impedance())])])])
    b=a.getCircuit('tut')
    c=0
    for x in b:
        c=c+x.R
    print c
    # print 'Transformer'
    # print Bus(lenght='10', amperage='1600')
    # print Bus(R='10', X='10', r0='10', x0='10')
    # print 'Reactor'
    # print Reactor(dP='1000', In='1000', X='0.001')
    # print Reactor(dP='1000', In='1000', L='10', M='5')
    # print 'Airway'
    # print Airway(lenght='1000', material='al', a='1', cross_section='35')
    a=initNetwork('test.xml')
    print a
    print a.getCircuit('tam')
