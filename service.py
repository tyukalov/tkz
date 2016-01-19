# -*- coding: utf-8 -*-
### ============================== service.py ============================== 

#from directory import *

def list_cmp (lst, ptrn):
    """
    Функция сравнивает списки lst и ptrn, возвращая список элементов
    списка lst, которых нет в ptrn
    """
    result		= []
    for x in lst:
        if not(x in ptrn):
            result.append(x)
    return result

def subList(lst, ptrn):
    for x in lst:
        if not(x in ptrn):
            return False
    return True


# ### Функции, проверяющие корректность передаваемых значений параметров
# def R (param):
#     try:
#         var			= float(param)
#     except ValueError:
#         return False
#     if var < 0:
#         return False
#     else:
#         return True

# highvoltage, lowvoltage, Sn, Un, Pk, resist, react, r0, x0, Skz, Ikz, lenght, X, a = R, R, R, R, R, R, R, R, R, R, R, R, R, R

# def cross_section(param):
#     return param in ('1', '1.5', '2.5', '4', '6', '10', '16', '25', '35', '50', '70', '95', '120', '150', '185', '240')
# def scheme(param):
#     return param in ('DY', 'YY')
# def material(param):
#     return param in ('cu', 'al')
# def types(param):
#     return param in airwayX0X1
# def cores(param):
#     return param in ('3','4')
# def amperage(param):
#     return param in ('250','400', '630', '1250', '1600', '2500', '3200', '4000')
# validattr		= {'amperage':amperage,'a': a, 'react': react, 'r0': r0, 'cores': cores, 'Ikz': Ikz, 'lenght': lenght, 'material': material, 'Skz': Skz, 'resist': resist, 'R': R, 'Un': Un, 'highvoltage': highvoltage, 'X': X, 'types': types, 'Pk': Pk, 'lowvoltage': lowvoltage, 'scheme': scheme, 'x0': x0, 'cross_section': cross_section, 'Sn': Sn}

# #==================================================================================
# # if __name__ == '__main__':
# #     print react('12.2.3')
# #     print a('12,1')
# #     print x0("123.5")
# #     a=list_cmp([1,2,4],[6,5,8,11,1,123,5])
# #     print a
# #     print cross_section('150')
# #     print scheme('DD')
# #     print material('cu')
# #     print types('OCWR')
