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
    param							= ('resist','react','r0','x0')
    R,X,R0,X0,Z,Z0,fullZ, fullZ0	= 8*[None]

    def __init__ (self, **kwargs):
        selector[self.type](self, **kwargs)
        try:
            self.fullZ0	= complex((2 * self.R + self.R0), (2 * self.X + self.X0))
            self.Z0		= abs(self.fullZ0)
            self.fullZ	= complex(self.R, self.X)
            self.Z		= abs(self.fullZ)
        except:
            print 'Initialize error!'
        
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
    param		= ('highvoltage', 'lowvoltage', 'Skz', 'Ikz', 'reactance')


### Класс сопротивления трансформаторов
class Transformer (Impedance):
    """
    Класс сопротивления трансформаторов. Все единицы - собственные.
    Параметры:
    Pk - потери короткого замыкания в трансформаторе, Вт;
    Sn - номинальная мощность трансформатора, Вт;
    Un - номинальное напряжение трансформатора, В;
    uk - напряжение короткого замыкания трансформатора, %;
    scheme - схема соединения обмоток (YY, DY)
    """
    type		= 'Transformer'
    param		= ('Sn', 'Un', 'Pk', 'uk', 'scheme', 'r0', 'x0')
    required	= ('Sn',)


### Класс кабелей
class Cable (Impedance):
    """
    Класс кабелей.
    Параметры:
    lenght - длина, м;
    cross_section - сечение, мм2;
    material - материал, (al, cu)
    types - материал оболочки, (aluminium_shell, plumbum_shell, shell, steel_shell)
    cores - число жил
    R, X - справочные значения удельных сопротивлений, Ом/м;
    """
    type		= 'Cable'
    required	= ('material', 'cross_section', 'lenght')
    param		= ('material', 'cross_section', 'lenght', 'types', 'cores', 'R', 'X', 'r0', 'x0')


### Класс шинопроводов
class Bus (Impedance):
    """
    Класс шинороводов.
    Параметры:
    amperage - расчётный ток, А;
    R, X, r0, x0 - паспортные удельные сопротивления, Ом/м;
    lenght - длина, м;
    """
    type		= 'Bus'


### Класс воздушных линий
class Airway (Impedance):
    """
    Класс воздушных линий.
    Параметры:
    lenght - длина, м;
    cross_section - сечение, мм";
    material - материал, (al, cu);
    a - расстояние между проводниками, м;
    r,x,r0,x0 - справочные данные;
    """
    type		= 'Airway'


### -----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print Cable(material='al', cross_section='2.5', lenght='1000')
    print Cable(material='al', cross_section='2.5', lenght='1000', R='0.009', X='0.0017')
