#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:59:44 2017

@author: denniswang
"""

def vector_plus(vector1,vector2):
    assert len(vector1) == len(vector2)
    index = 0
    result = []
    while index < len(vector1):
        result.append(vector1[index] + vector2[index])
        index += 1
    return result

def vector_minus(vector1,vector2):
    assert len(vector1) == len(vector2)
    index = 0
    result = []
    while index<len(vector1):
        result.append(vector1[index]-vector2[index])
        index += 1
    return result

def vector_scalar_multiply(scalar,vector):
    result = []
    for e in vector:
        result.append(scalar * e)
    return result

print vector_plus([8.218,-9.341],[-1.129,2.111])
print vector_minus([7.119,8.215],[-8.223,0.878])
print vector_scalar_multiply(7.41,[1.671,-1.012,-0.318])
        