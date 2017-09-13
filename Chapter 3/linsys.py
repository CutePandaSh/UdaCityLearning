from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane


getcontext().prec = 30

def redprint(str):
    print '\033[1;31;0m{}\033[0m'.format(str)


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        self.planes[row1], self.planes[row2] = self.planes[row2], self.planes[row1]


    def multiply_coefficient_and_row(self, coefficient, row):
        v = self.planes[row].normal_vector.time_scalar(coefficient)
        constant_term = self.planes[row].constant_term * Decimal(coefficient)

        self.planes[row] = Plane(v, constant_term)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        v_original = self.planes[row_to_add].normal_vector.time_scalar(coefficient)
        v = self.planes[row_to_be_added_to].normal_vector.plus(v_original)
        constant_term = self.planes[row_to_add].constant_term * Decimal(coefficient) + self.planes[row_to_be_added_to].constant_term
        self.planes[row_to_be_added_to] = Plane(v,constant_term)


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):

            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices

    def compute_triangular_form(self):
        system = deepcopy(self)
        row = 0
        var_index = 0
        while row < len(system) - 1:
            if system[row].normal_vector[var_index] == 0:
                n = system.find_first_nozero_to_swap(var_index,row)
                if not n == -1:
                    print '\nStart Swap: from {} to {}'.format(n,row)
                    system.swap_rows(row,n)
                else:
                    var_index += 1
                    continue
            k = row + 1
            while k < len(system):
                scalar = - system.planes[k].normal_vector[var_index] / system.planes[row].normal_vector[var_index]
                system.add_multiple_times_row_to_row(scalar,row,k)
                k += 1
            if var_index < system.dimension - 1:
                var_index += 1
            row += 1
        return system

    def find_first_nozero_to_swap(self, vector_dim,plane_index):
        index = plane_index + 1
        while index < len(self):
            if not self[index].normal_vector[vector_dim] == 0:
                return index
            index += 1
        else:
            return -1

    def compute_rref(self):
        triangel_system = self.compute_triangular_form()
        row = len(triangel_system) - 1
        var_index = triangel_system.dimension - 1
        while row > 0 and var_index >= 0:
            if triangel_system[row].normal_vector[var_index] != 0 :
                k = 0
                while k <= row - 1:
                    scale = -triangel_system[k].normal_vector[var_index]/triangel_system[row].normal_vector[var_index]
                    #print "row = {}; k = {}; var_index = {}".format(row,k,var_index)
                    triangel_system.add_multiple_times_row_to_row(scale,row,k)
                    k += 1
                row = row - 1
                var_index = var_index - 1
            else:
                row = row - 1
        print triangel_system
        return triangel_system


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


redprint("\nCase #1")
p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
s = LinearSystem([p1, p2])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='-1') and
                r[1] == p2):
    redprint('test case 1 failed')


redprint("\nCase #2")
p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
s = LinearSystem([p1, p2])
r = s.compute_rref()
if not (r[0] == p1 and
                r[1] == Plane(constant_term='1')):
    print 'test case 2 failed'


redprint("\nCase #3")
p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
s = LinearSystem([p1, p2, p3, p4])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='0') and
                r[1] == p2 and
                r[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
                r[3] == Plane()):
    print 'test case 3 failed'


redprint("\nCase #4")
p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
s = LinearSystem([p1, p2, p3])
r = s.compute_rref()
if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term=Decimal('23') / Decimal('9')) and
                r[1] == Plane(normal_vector=Vector(['0', '1', '0']), constant_term=Decimal('7') / Decimal('9')) and
                r[2] == Plane(normal_vector=Vector(['0', '0', '1']), constant_term=Decimal('2') / Decimal('9'))):
    print 'test case 4 failed'


# p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
# p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
# p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
#
#
# s = LinearSystem([p0,p1,p2,p3])
# s.swap_rows(0,1)
# if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
#     print 'test case 1 failed'
#
# s.swap_rows(1,3)
# if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
#     print 'test case 2 failed'
#
# s.swap_rows(3,1)
# if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
#     print 'test case 3 failed'
#
# s.multiply_coefficient_and_row(1,0)
# if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
#     print 'test case 4 failed'
#
# s.multiply_coefficient_and_row(-1,2)
# if not (s[0] == p1 and
#         s[1] == p0 and
#         s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
#         s[3] == p3):
#     print 'test case 5 failed'
#
# s.multiply_coefficient_and_row(10,1)
# if not (s[0] == p1 and
#         s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
#         s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
#         s[3] == p3):
#     print 'test case 6 failed'
# s.add_multiple_times_row_to_row(0,0,1)
# if not (s[0] == p1 and
#         s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
#         s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
#         s[3] == p3):
#     print 'test case 7 failed'
#
# s.add_multiple_times_row_to_row(1,0,1)
# if not (s[0] == p1 and
#         s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
#         s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
#         s[3] == p3):
#     print 'test case 8 failed'
#
# s.add_multiple_times_row_to_row(-1,1,0)
# if not (s[0] == Plane(normal_vector=Vector(['-10','-10','-10']), constant_term='-10') and
#         s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
#         s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
#         s[3] == p3):
#     print 'test case 9 failed'
# print 'All test passed'
#
# print '\n Start Testing Triangular Form'
#
# p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
# s = LinearSystem([p1,p2])
# t = s.compute_triangular_form()
# print '\nCase #1'
# for each in t.planes:
#     print each.normal_vector
#     print 'constant_term:',each.constant_term
# if not (t[0] == p1 and
#         t[1] == p2):
#     print 'test case 1 failed'
#
# p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
# s = LinearSystem([p1,p2])
# t = s.compute_triangular_form()
#
# redprint("\nCase #3")
# for each in t.planes:
#     print each.normal_vector
#     print 'constant_term:',each.constant_term
# if not (t[0] == p1 and
#         t[1] == Plane(constant_term='1')):
#     print 'test case 2 failed'
#
# p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
# p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
# p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
# s = LinearSystem([p1,p2,p3,p4])
# t = s.compute_triangular_form()
# print '\nCase #3'
# for each in t.planes:
#     print each.normal_vector
#     print 'constant_term:',each.constant_term
# if not (t[0] == p1 and
#         t[1] == p2 and
#         t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
#         t[3] == Plane()):
#     print 'test case 3 failed'
#
# p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
# p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
# s = LinearSystem([p1,p2,p3])
# t = s.compute_triangular_form()
# print '\nCase #4'
# for each in t.planes:
#     print each.normal_vector
#     print 'constant_term:',each.constant_term
# if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
#         t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
#         t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
#     print 'test case 4 failed'

# print s.indices_of_first_nonzero_terms_in_each_row()
# print '{},{},{},{}'.format(s[0],s[1],s[2],s[3])
# print len(s)
# print s
#
# s[0] = p1
# print s
#
# print MyDecimal('1e-9').is_near_zero()
# print MyDecimal('1e-11').is_near_zero()
