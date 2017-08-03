#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 18:22:18 2017

@author: denniswang
"""
import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector1():
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    def __init__(self,coordination):
        try:
            if not coordination:
                raise ValueError
            self.coordination = tuple([Decimal(x) for x in coordination])
            self.dimension = len(self.coordination)
            
        except ValueError:
            raise ValueError("The coordinates must be nonempty")
        
        
    def __str__(self):
        return "Vector: {}".format(self.coordination)
    
    def __eq__(self,v):
        return self.coordination == v.coordination
    
    def plus(self, v):
        new_coordination = [x+y for x,y in zip(self.coordination,v.coordination)]
        return Vector1(new_coordination)
    
    def minus(self,v):
        new_coordination = [x-y for x,y in zip(self.coordination,v.coordination)]
        return Vector1(new_coordination)
    
    def times_scalar(self,c):
        new_coordination = [Decimal(c)*x for x in self.coordination]
        return Vector1(new_coordination)
    
    def magnitude(self):
        coordinates_squared = [x ** 2 for x in self.coordination]
        return Decimal(math.sqrt(sum(coordinates_squared)))
    
    def normalized(self):
        maginitude = self.magnitude()
        
        try:
            return self.times_scalar(Decimal('1.0')/maginitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            
    def dot_product(self,v):
        new_coordinates = [x*y for x,y in zip(self.coordination, v.coordination)]
        return sum(new_coordinates)
    
    def angle_with(self,v,in_degree=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radius = math.acos(u1.dot_product(u2))
            if in_degree:
                return angle_in_radius * 180. / math.pi
            else:
                return angle_in_radius
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Can not compute an angle with the zero vector')
            else:
                raise e
    
    def parallelism_Orthogonality(self,v,tolerance = 1e-10):
        print ""
        #s_magnitude = self.magnitude()
#        v_magnitude = v.magnitude()
#        dot_product = self.dot_product(v)
#        try:
#            return math.acos(dot_product/(s_magnitude * v_magnitude))
#        except ZeroDivisionError:
#            raise Exception("Zero Vector have no angle")
    def is_orthogonal_to(self,v,tolerance=1e-10):
        return abs(self.dot_product(v)) < tolerance
    
    def is_zero_vector(self,tolerance=1e-10):
        return self.magnitude() < tolerance
    
    def is_parallel_to(self,v):
        return (self.is_zero_vector or v.is_zero_vector or 
                self.angle_with(v) == 0 or 
                self.angle_with(v) == pi)
        
    def projection_to(self,v):
        try:
            u = v.normalized()
            return u.times_scalar(self.dot_product(u))
        except Exception as e:
            raise e
    
    def orthogonality_to(self,v):
        try:
            proj = self.projection_to(v)
            return self.minus(proj)
        except Exception as e:
            raise e
    
    def cross(self,v):
        result = []
        result.append(self.coordination[1]*v.coordination[2]-self.coordination[2]*v.coordination[1])
        result.append(-(self.coordination[0]*v.coordination[2]-self.coordination[2]*v.coordination[0]))
        result.append(self.coordination[0]*v.coordination[1]-self.coordination[1]*v.coordination[0])
        return Vector1(result)
    
v = Vector1([8.218,-9.341])
w = Vector1([-1.129,2.111])
print v.plus(w)

v = Vector1([7.119,8.215])
w = Vector1([-8.223,0.878])
print v.minus(w)

v = Vector1([1.671,-1.012,-0.318])
c = 7.41
print v.times_scalar(c)

v = Vector1([-0.221,7.437])
print round(v.magnitude(),4)

v = Vector1([8.813,-1.331,-6.247])
print round(v.magnitude(),4)

v = Vector1([5.581,-2.136])
print v.normalized()

v = Vector1([1.996,3.108,-4.554])
print v.normalized()

v = Vector1([7.887,4.138])
w = Vector1([-8.802,6.776])
print v.dot_product(w)

v = Vector1([3.183,-7.627])
w = Vector1([-2.668,5.319])
print v.angle_with(w)

v = Vector1([-5.955,-4.904,-1.874])
w = Vector1([-4.496,-8.755,7.103])
print v.dot_product(w)

v = Vector1([7.35,0.221,5.188])
w = Vector1([2.751,8.259,3.985])
print v.angle_with(w) * 180 / math.pi

v = Vector1([-7.579,-7.88])
w = Vector1([22.737,23.64])
print v.parallelism_Orthogonality(w)

v = Vector1([-2.029,9.97,4.172])
w = Vector1([-9.231,-6.639,-7.245])
print v.parallelism_Orthogonality(w)

v = Vector1([-2.328,-7.284,-1.214])
w = Vector1([-1.821,1.072,-2.94])
print v.parallelism_Orthogonality(w)

v = Vector1([2.118,4.827])
w = Vector1([0,0])
print v.parallelism_Orthogonality(w)

v = Vector1([3.039,1.879])
b = Vector1([0.825,2.036])
print v.projection_to(b)

v = Vector1([-9.88,-3.264,-8.159])
b = Vector1([-2.155,-9.353,-9.473])
print v.orthogonality_to(b)

v = Vector1([3.009,-6.172,3.692,-2.51])
b = Vector1([6.404,-9.144,2.759,8.718])
print  v.projection_to(b)
print  v.orthogonality_to(b)

print "\n Cross"
v = Vector1([8.462,7.893,-8.187])
w = Vector1([6.984,-5.975,4.778])
print v.cross(w)

print "\n#1"
v = Vector1([-8.987,-9.838,5.031])
w = Vector1([-4.268,-1.861,-8.866])
print v.cross(w).magnitude()

print "\n#2"
v = Vector1([1.5,9.547,3.691])
w = Vector1([-6.007,0.124,5.772])
print v.cross(w).magnitude()*Decimal(0.5)