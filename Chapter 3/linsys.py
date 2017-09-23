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
            if not MyDecimal(triangel_system[row].normal_vector[var_index]).is_near_zero() :
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

    def cacl_result(self):
        triagel_system = self.compute_rref()
        result = ["#"]
        result = result * self.dimension
        for k, p in enumerate(triagel_system.planes):
            if p.normal_vector.is_zero_vector():
                constant = MyDecimal(p.constant_term)
                print constant
                if constant.is_near_zero():
                    continue
                else:
                    raise Exception("no result1")
            not_zero_count = 0
            not_zero_index = -1
            for i,v in enumerate(p.normal_vector.coordination):
                if not MyDecimal(v).is_near_zero():
                    not_zero_index = i
                    not_zero_count += 1
            if not_zero_count != 1:
                continue
            else:

                if result[not_zero_index] != "#":
                    raise Exception("no result2")
                else:
                    result[not_zero_index] = p.constant_term /  p.normal_vector[not_zero_index]
        if "#" in result:
            raise Exception("unlimit result3")
        else:
            return result




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

def get_plane(v,constant):
    return Plane(normal_vector=Vector(v),constant_term=constant)

redprint("\nCase #1")
p1 = get_plane([5.862,1.178,-10.366],-8.15)
p2 = get_plane([-2.931,-0.589,5.183],-4.075)
s = LinearSystem([p1,p2])
try:
    print s.cacl_result()
except Exception as e:
    print e

redprint("\nCase #2")
p1 = get_plane([8.631,5.112,-1.816],-5.113)
p2 = get_plane([4.315,11.132,-5.27],-6.775)
p3 = get_plane([-2.158,3.01,-1.727],-0.831)
s = LinearSystem([p1,p2,p3])
try:
    print s.cacl_result()
except Exception as e:
    print e



redprint("\nCase #3")
p1 = get_plane([5.262, 2.739, -9.878],-3.441)
p2 = get_plane([5.111, 6.358, 7.638], -2.152)
p3 = get_plane([2.016, -9.924, -1.367], -9.278)
p4 = get_plane([2.167, -13.543, -18.883], -10.567)
s = LinearSystem([p1,p2,p3,p4])
try:
    print s.cacl_result()
except Exception as e:
    print e




# redprint("\nCase #1")
# p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
# s = LinearSystem([p1, p2])
# r = s.compute_rref()
# if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='-1') and
#                 r[1] == p2):
#     redprint('test case 1 failed')
#
#
# redprint("\nCase #2")
# p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
# s = LinearSystem([p1, p2])
# r = s.compute_rref()
# if not (r[0] == p1 and
#                 r[1] == Plane(constant_term='1')):
#     print 'test case 2 failed'
#
#
# redprint("\nCase #3")
# p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
# p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
# p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
# s = LinearSystem([p1, p2, p3, p4])
# r = s.compute_rref()
# if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='0') and
#                 r[1] == p2 and
#                 r[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
#                 r[3] == Plane()):
#     print 'test case 3 failed'
#
#
# redprint("\nCase #4")
# p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
# p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
# p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
# s = LinearSystem([p1, p2, p3])
# r = s.compute_rref()
# if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term=Decimal('23') / Decimal('9')) and
#                 r[1] == Plane(normal_vector=Vector(['0', '1', '0']), constant_term=Decimal('7') / Decimal('9')) and
#                 r[2] == Plane(normal_vector=Vector(['0', '0', '1']), constant_term=Decimal('2') / Decimal('9'))):
#     print 'test case 4 failed'


