from decimal import Decimal, getcontext

from Vector1 import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel_to(self, l):
        p = Vector([l.normal_vector[1],-l.normal_vector[0]])
        # print self.normal_vector.dot(p)
        return self.normal_vector.is_parallel_to(l.normal_vector)

    def is_equal_to(self, l):
        if self.is_parallel_to(l):
            u = self.basepoint.minus(l.basepoint)
            return u.is_orthogonal_to(self.normal_vector)
        else:
            return False

    def intersection_with(self, l):
        if self.is_parallel_to(l):
            if self.is_equal_to(l):
                raise Exception("Lines are equal, have unlimited intersections")
            else:
                raise Exception("Lines are parallel have no intersection")
        else:
            a, b, k1 = self.normal_vector[0], self.normal_vector[1], self.constant_term
            c, d, k2 = l.normal_vector[0], l.normal_vector[1], l.constant_term
            intersection = ['0'] * self.dimension
            if a == 0:
                a, b, k1, c, d, k2 = c, d, k2, a, b, k1
            intersection[0] = Decimal(d * k1 - b * k2)/ Decimal(a * d - b * c)
            intersection[1] = Decimal(a * k2 - c * k1)/ Decimal(a * d - b * c)
            return Vector(intersection)





class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

def print_output(l1,l2):
    try:
        print l1
        print l2
        print "intersection: {}".format(l1.intersection_with(l2))
    except Exception as e:
        print e

print "\n#1"
line1 = Line(Vector([4.046,2.836]), 1.21)
line2 = Line(Vector([10.115,7.09]), 3.025)

print_output(line1,line2)


print "\n#2"
line1 = Line(Vector([7.204, 3.182]), 8.68)
line2 = Line(Vector([8.172, 4.114]), 9.883)
print_output(line1,line2)

print "\n#3"
line1 = Line(Vector([1.182, 5.562]), 6.744)
line2 = Line(Vector([1.773, 8.343]), 9.525)
print_output(line1,line2)

print "\n#4"

