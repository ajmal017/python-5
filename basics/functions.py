#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 15:25:52 2020

@author: maximilianstaebler
"""

class Cars():
    
    brands = ('audi', 'mercedes', 'bmw')
    
    def __init__(self, brand, color, ps):
        self.brand = brand
        self.color = color
        self.ps = ps
        self.cars = {}
        self.idx = 0
        
    def __str__(self):
        return('The car is from {}, has {} ps and is {}.'.format(self.brand,\
                                                                  self.ps, \
                                                                  self.color))
    @classmethod
    def audi(cls, color, ps):
        return(cls(cls.brands[0], color, ps))
        
    
    # @classmethod
    # def mercedes(cls, color, ps):
    #     cls.brand = brands[1],
    #     cls.color = color
    #     cls.ps = ps
    
    # @staticmethod
    # def append_cars(car):
    #     self.cars[idx] = {'brand':self.brand, \
    #                       'color':self.color}
        
        
            
            
            
# car = Cars('audi', 'red', 230)
# print(car)

typ = Cars.audi('red', 234)
print(typ)

print(typ.color)