# -*- coding: utf-8 -*-
### ===================================== errors.py ========================================
###
### Author:			Igor Tyukalov
### License:		BSD
### Date:			09.02.2016
### ========================================================================================
### Классы исключений
class TkzErrors(Exception):
    def __init__ (self,param,mode='NORMAL'):
        self.param	= param
        self.mode	= mode
class InvalidArgument(TkzErrors):
    def __str__ (self):
        if self.mode=='NORMAL':
            return self.param
        elif self.mode=="FLOATERROR":
            return "Parameter param '" + self.param + "' must be a real number"
        elif self.mode=='INITERROR':
            return "Invalid parameters for the element '" + self.param + "'"
        elif self.mode=='INVARG':
            return "Invalid argument from '" + self.param + "' element"
class DBError(TkzErrors):
    def __str__ (self):
        return "Database error in '" + self.param + "'"
class NetworkError(Exception):
    pass
### ================================= End errors.py ========================================
