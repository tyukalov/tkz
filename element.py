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
#from errors import *
try:
    from numpy import linalg
except:
    LNLG_FLAG	= False
else:
    LNLG_FLAG	= True



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
        if self.fullZ==None or self.fullZ0==None or other.fullZ==None or other.fullZ0==None:
            print 'Uninizialized instance!'
        else:
            R		= self.R + other.R
            X		= self.X + other.X
            R0		= self.R0 + other.R0
            X0		= self.X0 + other.X0
            return Impedance(resist=R, react=X, r0=R0, x0=X0)

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
            raise InvalidArgument
        if 'name' in kwargs:
            self.name			= kwargs['name']
        else:
            self.name			= 'Unknown'
        if 'tail' in kwargs:
            lst					= kwargs['tail']
            for x in lst:
                if not(x.type == 'Network'):
                    raise InvalidArgument
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
    
    def getResistance(self,point):
        circuit			= self.getCircuit(point)
        if circuit:
            result		= Impedance()
            for x in circuit:
                result		+= x
            return result
        else:
            return False
        

class Branch:
    '''
    Класс ветви электрической сети.
    graph		- последовательность номеров узлов. Определяет направление расчётного тока;
    EMF			- электродвижущая сила;
    resistance	- электрическое сопротивление.
    Единицы измерения не указаны, поскольку зависят от характера сети
    '''
    type						= 'branch'
    
    def __init__(self, ID, graph, resistance=0, EMF=0):
        if len(graph):
            self.graph			= tuple(graph)
        else:
            raise InvalidArgument("In 'branch' init. Invalid argument 'graph'")
        try:
            self.resistance		= float(resistance)
            self.EMF			= float(EMF)
        except:
            raise InvalidArgument('branch', mode='FLOATERROR')
        self.ID				= ID

    def getSign (self, node):
        if node in self.graph:
            return (-1) ** self.graph.index(node) * (-1)	# 1 если "хвост" и -1 если "голова"
        else:
            return 0
        
class General:
    '''
    Параметры:
    circuit	- кортеж контуров. Каждый контур представляет собой
    кортеж из входящих в него ветвей, заданных своими идентификаторами.
    args	- ветви, представленные экземплярами класса Branch
    '''
    type						= 'general'
    def __init__ (self, circuit, *args):
        self.network			= dict(zip(range(len(args))), args)
        var					= ()
        for x in args:
            var				+= x.graph
        nodes				= ()
        for x in var:
            if  x not in nodes:
                nodes			+= (x,)
        self.nodes			= nodes
        var				= len(self.network) - len(self.nodes)
        if len(circuit) < var:
            raise InvalidArgument('Required ' + str(len(circuit)) + ' circuit, given ' + str(var))
        self.circuit			= circuit[:(var-1)]
        
    def solve (self):
        matrix				= []
        column				= []
        if len(self.network) == len(self.nodes) + len(self.circuit):
            for x in self.nodes:
                line			= []
                for y in self.network:
                    line.append(y.getSign(x))
                matrix.append(line)
### ================================= End element.py ========================================
### -----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    a=Network(Impedance(),tail=[Network(Impedance()), Network(Impedance(),tail=[Network(Impedance()), Network(Impedance(),tail=[Network(Impedance(resist='10'), name='tut'), Network(Impedance())])])])
    print a.getResistance('tut')
    # print 'Transformer'
    # print Bus(lenght='10', amperage='1600')
    # print Bus(R='10', X='10', r0='10', x0='10')
    # print 'Reactor'
    # print Reactor(dP='1000', In='1000', X='0.001')
    # print Reactor(dP='1000', In='1000', L='10', M='5')
    # print 'Airway'
    # print Airway(lenght='1000', material='al', a='1', cross_section='35')
