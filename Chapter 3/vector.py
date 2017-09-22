import math
from decimal import Decimal,getcontext

getcontext().prec = 30




class Vector:
    TOLERANCE=1e-10

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"

    def __init__(self, coordination):
        try:
            if not coordination:
                raise ValueError
            self.coordination = tuple(Decimal(x) for x in coordination)
            self.dimension = len(coordination)
            self.start = 0
        except ValueError:
            raise ValueError("Coordination must be nonempty")

    def __str__(self):
        return "Vector: {}".format(self.coordination)

    def __eq__(self, other):
        return self.coordination == other.coordination

    def __iter__(self):
        return self

    def next(self):
        if self.start < self.dimension:
            i = self.start
            self.start += 1
            return self.coordination[i]
        else:
            raise StopIteration

    def __getitem__(self, item):
        return  self.coordination[item]

    def __setitem__(self, key, value):
        self.coordination[key] = value

    def plus(self, v):
        new = [x + y for x, y in zip(self.coordination, v.coordination)]
        return Vector(new)

    def minus(self, v):
        new = [x - y for x, y in zip(self.coordination, v.coordination)]
        return Vector(new)

    def time_scalar(self, n):
        new = [Decimal(n) * x for x in self.coordination]
        return Vector(new)

    def magnitude(self):
        c_squarded = [x ** 2 for x in self.coordination]
        return Decimal(math.sqrt(sum(c_squarded)))

    def normalized(self):
        magnitude = self.magnitude()
        try:
            return self.time_scalar(Decimal(1.0)/magnitude)
        except ZeroDivisionError:
            raise Exception("ZeroVector can not be normalized")

    def dot(self, v):
        new = [x * y for x, y in zip(self.coordination, v.coordination)]
        return Decimal(sum(new))

    def angel_with(self, v, in_degree=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            d = u1.dot(u2)
            if d - 1 <= 1e-10:
                d = 1
            angel_with = math.acos(d)
            if in_degree:
                return angel_with * 180. / math.pi
            else:
                return angel_with
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Can not compute an angel with Zero Vector")
            else:
                raise e

    def is_zero_vector(self):
        if self.magnitude() < self.TOLERANCE:
            return True
        else:
            return False

    def is_orthogonal_to(self, v):
        return abs(self.dot(v)) <= self.TOLERANCE

    def is_parallel_to(self, v):
        result = self.is_zero_vector() or v.is_zero_vector() or abs(self.angel_with(v)) <= 1e-3 or self.angel_with(v) == math.pi
        return result

    def projection_to(self, v):
        try:
            u = v.normalized()
            return u.time_scalar(self.dot(u))
        except Exception as e:
            raise e

    def orthogonal_to(self, v):
        try:
            u = self.projection_to(v)
            return self.minus(u)
        except Exception as e:
            raise e

    def cross(self, v):
        if len(self.coordination) > 3 or len(v.coordination) > 3:
            raise Exception("Can not compute the cross of vectors whose dimension ise bigger than 3")
        else:
            u1 = self.get_three_dimension_vector()
            u2 = v.get_three_dimension_vector()
            new = []
            new.append(u1[1] * u2[2] - u1[2] * u2[1])
            new.append(-(u1[0] * u2[2] - u1[2] * u2[0]))
            new.append(u1[0]*u2[1] - u1[1] * u2[0])
            return Vector(new)


    def get_three_dimension_vector(self):
        u = []
        for i in self.coordination:
            u.append(i)
        while len(u) < 3:
            u.append(0)
        return u




# print "\n Cross"
# v = Vector([8.462,7.893,-8.187])
# w = Vector([6.984,-5.975,4.778])
# print v.cross(w)
#
# print "\n#1"
# v = Vector([-8.987,-9.838,5.031])
# w = Vector([-4.268,-1.861,-8.866])
# print v.cross(w).magnitude()
#
# print "\n#2"
# v = Vector([1.5,9.547,3.691])
# w = Vector([-6.007,0.124,5.772])
# print v.cross(w).magnitude()*Decimal(0.5)